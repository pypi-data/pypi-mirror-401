import argparse
import os
import sys
from .core import check_gs, convert_images, extract_and_convert_tikz, update_tex_references, compile_thesis, compress_pdf

# Try importing tomllib (Python 3.11+) or fall back to tomli
try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None

def load_config(root_dir):
    """Load config from latex-optimizer.toml or pyproject.toml."""
    if tomllib is None:
        return {}

    config = {}
    
    # 1. Check latex-pdf-size-optimizer.toml
    config_path = os.path.join(root_dir, "latex-pdf-size-optimizer.toml")
    if os.path.exists(config_path):
        try:
            with open(config_path, "rb") as f:
                data = tomllib.load(f)
                if "tool" in data and "latex-pdf-size-optimizer" in data["tool"]:
                    config = data["tool"]["latex-pdf-size-optimizer"]
                else:
                    config = data
                print(f"Loaded config from {config_path}")
        except Exception as e:
            print(f"Warning: Failed to parse {config_path}: {e}")
            
    # 2. Check pyproject.toml if no specific config found (or merge?)
    if not config:
        pyproject_path = os.path.join(root_dir, "pyproject.toml")
        if os.path.exists(pyproject_path):
            try:
                with open(pyproject_path, "rb") as f:
                    pyproject = tomllib.load(f)
                    if "tool" in pyproject and "latex-pdf-size-optimizer" in pyproject["tool"]:
                        config = pyproject["tool"]["latex-pdf-size-optimizer"]
                        print(f"Loaded config from {pyproject_path} [tool.latex-pdf-size-optimizer]")
            except Exception as e:
                print(f"Warning: Failed to parse {pyproject_path}: {e}")
    
    return config

def main():
    parser = argparse.ArgumentParser(description="Optimize LaTeX projects by converting images and compressing PDFs.")
    
    # We parse known args first to get the path, then load config, then set defaults
    parser.add_argument("path", nargs="?", default=".", help="Root directory of the LaTeX project (default: .)")
    parser.add_argument("--main-tex", help="Main LaTeX file")
    parser.add_argument("--max-size", type=float, help="Target PDF size in MB")
    parser.add_argument("--dpi", type=int, help="DPI for image conversion")
    parser.add_argument("--compression", help="Ghostscript PDF settings (e.g. /ebook)")
    parser.add_argument("--gs-cmd", help="Ghostscript executable command")
    parser.add_argument("--no-clean", action="store_true", help="Skip cleaning build artifacts before compilation")
    parser.add_argument("--skip-tikz", action="store_true", help="Skip TikZ extraction and conversion")
    parser.add_argument("--exclude", nargs="*", help="List of files to exclude from conversion")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without modifying files")

    args = parser.parse_args()
    
    root_dir = os.path.abspath(args.path)
    if not os.path.exists(root_dir):
        print(f"Error: Directory '{root_dir}' does not exist.")
        sys.exit(1)
        
    os.chdir(root_dir)
    print(f"Project Root: {root_dir}")
    
    # Load config and merge
    file_config = load_config(root_dir)
    
    # Default values
    defaults = {
        "main_tex": "thesis.tex",
        "max_size": 5.0,
        "dpi": 200,
        "compression": "/ebook",
        "gs_cmd": "gswin64c",
        "exclude": []
    }
    
    # Priority: CLI Args (not None) > Config File > Defaults
    
    main_tex = args.main_tex if args.main_tex else file_config.get("main_tex", defaults["main_tex"])
    max_size = args.max_size if args.max_size is not None else file_config.get("max_size", defaults["max_size"])
    dpi = args.dpi if args.dpi is not None else file_config.get("dpi", defaults["dpi"])
    compression = args.compression if args.compression else file_config.get("compression", defaults["compression"])
    gs_cmd = args.gs_cmd if args.gs_cmd else file_config.get("gs_cmd", defaults["gs_cmd"])
    
    # Booleans are trickier with store_true. If CLI is False (default), check config.
    # Note: args.no_clean is False by default. If config has "no_clean" = True, we should respect it.
    no_clean = args.no_clean or file_config.get("no_clean", False)
    skip_tikz = args.skip_tikz or file_config.get("skip_tikz", False)
    
    # Exclude list merge? Or override? Let's override for simplicity, or append if desired. 
    # Usually CLI overrides relevant list.
    exclude = args.exclude if args.exclude is not None else file_config.get("exclude", defaults["exclude"])
    
    if not check_gs(gs_cmd):
        sys.exit(1)
        
    if args.dry_run:
        print("--- DRY RUN MODE ACTIVATED ---")
        
    # Ignore the main result PDF and the source main PDF to avoid attempted conversion
    main_pdf = os.path.splitext(main_tex)[0] + ".pdf"
    output_pdf = os.path.splitext(main_tex)[0] + "_compressed.pdf"
    ignore_files = [main_tex, main_pdf, output_pdf] + exclude
    
    # 1. Convert Images
    convert_images(root_dir, dpi=dpi, gs_cmd=gs_cmd, ignore_files=ignore_files, dry_run=args.dry_run)
    
    # 2. Extract and pre-compile TikZ
    if not skip_tikz:
        extract_and_convert_tikz(root_dir, dpi=dpi, gs_cmd=gs_cmd, dry_run=args.dry_run)
    
    # 3. Update TeX files
    update_tex_references(root_dir, dry_run=args.dry_run)
    
    # 4. Compile
    compile_thesis(main_tex, clean_first=not no_clean, dry_run=args.dry_run)
    
    # 5. Compress
    compress_pdf(main_pdf, output_pdf, gs_cmd=gs_cmd, pdf_settings=compression, target_size_mb=max_size, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
