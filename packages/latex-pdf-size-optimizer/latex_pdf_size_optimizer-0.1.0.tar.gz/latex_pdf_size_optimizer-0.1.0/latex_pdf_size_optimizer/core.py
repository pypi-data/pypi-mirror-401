import os
import re
import subprocess
import shutil
import sys
import hashlib
import json

CACHE_FILE = ".latex_pdf_size_optimizer_cache.json"

def calculate_file_hash(filepath):
    """Calculate SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def load_cache():
    """Load cache from JSON file."""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_cache(cache):
    """Save cache to JSON file."""
    try:
        with open(CACHE_FILE, "w") as f:
            json.dump(cache, f, indent=4)
    except Exception as e:
        print(f"Warning: Failed to save cache: {e}")

def check_gs(gs_cmd="gswin64c"):
    """Check if Ghostscript is available."""
    try:
        subprocess.run([gs_cmd, "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        # print(f"Ghostscript found: {gs_cmd}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"Error: Ghostscript ({gs_cmd}) not found. Please install it or provide the correct executable name.")
        return False

def get_pdf_dimensions(pdf_path, dpi, gs_cmd="gswin64c"):
    """Calculate pixel dimensions for PDF based on bounding box."""
    cmd = [
        gs_cmd, "-sDEVICE=bbox", "-dNOPAUSE", "-dBATCH", "-dSAFER", "-q",
        pdf_path
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        
        width_pt = 0
        height_pt = 0
        
        for line in result.stderr.splitlines():
            if line.startswith("%%HiResBoundingBox:"):
                parts = line.split()[1:]
                if len(parts) >= 4:
                    llx, lly, urx, ury = map(float, parts)
                    width_pt = urx - llx
                    height_pt = ury - lly
                    break
            elif line.startswith("%%BoundingBox:") and width_pt == 0:
                parts = line.split()[1:]
                if len(parts) >= 4:
                    llx, lly, urx, ury = map(float, parts)
                    width_pt = urx - llx
                    height_pt = ury - lly
                    
        if width_pt > 0 and height_pt > 0:
            w_px = int(width_pt / 72.0 * dpi)
            h_px = int(height_pt / 72.0 * dpi)
            return w_px, h_px
            
    except Exception as e:
        print(f"  Warning: Could not detect PDF dimensions: {e}")
    
    return None, None

def convert_images(root_dir, dpi=200, gs_cmd="gswin64c", ignore_files=None, dry_run=False):
    """Convert .eps and .pdf images to .jpg."""
    if ignore_files is None:
        ignore_files = []
    
    cache = load_cache()
    updated_cache = cache.copy()
    
    print("--- Converting Images ---")
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith(('.eps', '.pdf')):
                if file in ignore_files:
                    continue
                if "tikz_extracted" in file:
                    continue

                full_path = os.path.normpath(os.path.join(subdir, file))
                base_name = os.path.splitext(full_path)[0]
                jpg_path = base_name + ".jpg"

                # Calculate hash using relative path as key
                rel_path = os.path.relpath(full_path, root_dir)
                current_hash = calculate_file_hash(full_path)
                
                # Check cache: if hash matches AND output exists, skip
                if rel_path in cache and cache[rel_path] == current_hash and os.path.exists(jpg_path):
                    # print(f"Skipping (cached): {rel_path}")
                    updated_cache[rel_path] = current_hash # Ensure we keep it
                    continue

                print(f"Converting: {full_path} -> {jpg_path}")
                
                if dry_run:
                    print(f"  [Dry Run] Would run Ghostscript conversion for {file}")
                    updated_cache[rel_path] = current_hash # Pretend we updated it
                    continue

                cmd = [
                    gs_cmd,
                    "-dNOPAUSE", "-dBATCH", "-dSAFER",
                    "-sDEVICE=jpeg",
                    f"-dTextAlphaBits=4", f"-dGraphicsAlphaBits=4",
                    f"-r{dpi}",
                ]
                
                if file.lower().endswith('.eps'):
                    cmd.append("-dEPSCrop")
                elif file.lower().endswith('.pdf'):
                    w, h = get_pdf_dimensions(full_path, dpi, gs_cmd)
                    if w and h:
                        print(f"  Dynamic sizing for PDF: {w}x{h}")
                        cmd.append(f"-g{w}x{h}")
                        cmd.append("-dPDFFitPage") 
                        cmd.append("-dUseCropBox")
                    
                cmd.extend([
                    f"-sOutputFile={jpg_path}",
                    full_path
                ])
                
                try:
                    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
                    updated_cache[rel_path] = current_hash
                except subprocess.CalledProcessError as e:
                    print(f"Failed to convert {full_path}: {e}")
    
    if not dry_run:
        save_cache(updated_cache)

def extract_and_convert_tikz(root_dir, dpi=200, gs_cmd="gswin64c", dry_run=False):
    """Extract TikZ environments, compile them, and convert to JPG."""
    print("--- Processing TikZ Figures ---")
    
    preamble = r"""
\documentclass[preview]{standalone}
\usepackage{tikz}
\usepackage{pgfplots}
\usepackage{amsmath,amssymb}
\pgfplotsset{compat=1.17}
\usetikzlibrary{shapes,arrows,positioning,calc}
\begin{document}
"""
    
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".tex"):
                full_path = os.path.join(subdir, file)
                
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                matches = list(re.finditer(r'(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})', content, re.DOTALL))
                
                if not matches:
                    continue
                
                # We skip detailed dry-run logs for every tikz find to avoid spam, unless we find them
                if dry_run:
                    print(f"  [Dry Run] Found {len(matches)} TikZ figures in {file} to extract.")
                    # We can't easily simulate extraction without modifying files in dry run, 
                    # so we just skip the logic loop for safety/simplicity in dry run
                    continue

                print(f"Found {len(matches)} TikZ figures in {file}")
                
                new_content = content
                offset = 0
                
                for i, match in enumerate(matches):
                    tikz_code = match.group(1)
                    
                    rel_dir = os.path.relpath(subdir, root_dir)
                    safe_rel_dir = rel_dir.replace(os.sep, "_").replace(".", "")
                    base_name = os.path.splitext(file)[0]
                    fig_name = f"tikz_{safe_rel_dir}_{base_name}_{i}"
                    tex_filename = f"{fig_name}.tex"
                    pdf_filename = f"{fig_name}.pdf"
                    jpg_filename = f"{fig_name}.jpg"
                    
                    with open(tex_filename, 'w', encoding='utf-8') as tf:
                        tf.write(preamble + tikz_code + "\n\\end{document}")
                    
                    try:
                        subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_filename], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
                    except subprocess.CalledProcessError:
                        print(f"Warning: Failed to compile TikZ figure {tex_filename}. Keeping original code.")
                        continue
                        
                    if os.path.exists(pdf_filename):
                        cmd = [
                            gs_cmd, "-dNOPAUSE", "-dBATCH", "-dSAFER",
                            "-sDEVICE=jpeg", f"-r{dpi}", "-dEPSCrop",
                            f"-sOutputFile={jpg_filename}", pdf_filename
                        ]
                        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
                    
                    include_graphics_cmd = f"\\includegraphics[width=\\linewidth]{{{jpg_filename}}}"
                    
                    start, end = match.span()
                    actual_start = start + offset
                    actual_end = end + offset
                    
                    new_content = new_content[:actual_start] + include_graphics_cmd + new_content[actual_end:]
                    
                    offset += len(include_graphics_cmd) - (end - start)
                    
                    for ext in ['.aux', '.log', '.tex', '.pdf']:
                        if os.path.exists(fig_name + ext):
                            os.remove(fig_name + ext)
                
                if new_content != content:
                    print(f"Updating {full_path} with TikZ replacements")
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

def update_tex_references(root_dir, dry_run=False):
    """Update .tex files to use .jpg instead of .eps/.pdf."""
    print("--- Updating TeX References ---")
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".tex"):
                full_path = os.path.join(subdir, file)
                
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                def replacement(match):
                    full_match = match.group(0)
                    cmd = match.group(1) 
                    opts = match.group(2) 
                    filename = match.group(3) 
                    
                    if filename.lower().endswith(('.eps', '.pdf')):
                        new_filename = os.path.splitext(filename)[0] + ".jpg"
                        return f"{cmd}{opts}{{{new_filename}}}"
                    return full_match

                pattern = r"(\\includegraphics)(\[[^\]]*\])?\{([^}]+)\}"
                
                new_content = re.sub(pattern, replacement, content)
                
                if content != new_content:
                    print(f"Updating references in {full_path}")
                    if dry_run:
                        print(f"  [Dry Run] Would update {file}")
                    else:
                        with open(full_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)

def compile_thesis(main_tex, clean_first=True, dry_run=False):
    """Compile the thesis using latexmk."""
    if clean_first:
        print("--- Cleaning LaTeX Build Artifacts ---")
        if dry_run:
            print("  [Dry Run] Would run latexmk -C")
        else:
            try:
                subprocess.run(["latexmk", "-C", main_tex], check=False)
            except Exception as e:
                print(f"Warning during clean: {e}")

    print("--- Compiling Thesis ---")
    cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", main_tex]
    if dry_run:
        print(f"  [Dry Run] Would execute: {' '.join(cmd)}")
    else:
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Compilation failed: {e}")

def compress_pdf(input_pdf, output_pdf, gs_cmd="gswin64c", pdf_settings="/ebook", target_size_mb=5.0, dry_run=False):
    """Compress the PDF using Ghostscript."""
    print(f"--- Compressing {input_pdf} -> {output_pdf} ---")
    
    if not dry_run and not os.path.exists(input_pdf):
        print(f"Input PDF {input_pdf} not found.")
        return

    cmd = [
        gs_cmd,
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={pdf_settings}", 
        "-dNOPAUSE", "-dQUIET", "-dBATCH",
        f"-sOutputFile={output_pdf}",
        input_pdf
    ]
    
    if dry_run:
        print(f"  [Dry Run] Would execute Ghostscript compression on {input_pdf}")
    else:
        try:
            subprocess.run(cmd, check=True)
            
            size = os.path.getsize(output_pdf) / (1024 * 1024)
            print(f"Compressed size: {size:.2f} MB")
            
            if size > target_size_mb:
                print(f"Warning: File size ({size:.2f} MB) is still > {target_size_mb}MB. You might need to reduce DPI or use /screen.")
                
        except subprocess.CalledProcessError as e:
            print(f"Compression failed: {e}")
