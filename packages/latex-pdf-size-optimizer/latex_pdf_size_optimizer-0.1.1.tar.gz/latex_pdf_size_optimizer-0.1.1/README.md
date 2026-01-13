<p align="center">
  <img src="https://raw.githubusercontent.com/lstival/LatedPDFSizeOptimizer/main/icon_latex_optimize.png" alt="LatexPDFSizeOptimizer Icon" width="200"/>
</p>

# LatexPDFSizeOptimizer

A tool to optimize LaTeX projects by converting vector graphics to JPG, pre-compiling TikZ figures, and compressing the final PDF.

## Features
- **Image Conversion**: Recursively converts `.eps` and `.pdf` images to `.jpg` to reduce file size.
- **Dynamic Resizing**: Detects exact dimensions of PDF figures to prevent cropping.
- **Smart Caching**: Skips redundant conversions using hash-based verification.
- **TikZ Optimization**: Extracts `tikzpicture` environments, compiles them, and replaces them in source.
- **Robust Compilation**: Auto-cleans build artifacts to prevent corruption.
- **PDF Compression**: Compresses final output to target size using Ghostscript.

## Installation

```bash
pip install .
```

## Usage

Navigate to your LaTeX project directory and run:

```bash
latex-pdf-size-optimizer
```

(Settings are loaded from `latex-pdf-size-optimizer.toml` or CLI arguments)

### Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `path` | Path to project root | `.` |
| `--main-tex` | Main LaTeX file | `thesis.tex` |
| `--max-size` | Target PDF size in MB | `5.0` |
| `--dpi` | Image resolution | `200` |
| `--compression` | Ghostscript setting (`/screen`, `/ebook`) | `/ebook` |
| `--exclude` | Files to exclude | `[]` |
| `--dry-run` | Preview actions without changes | `False` |

### Example

```bash
latex-pdf-size-optimizer --dry-run
```
