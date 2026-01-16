#!/bin/bash
# Script to compile the Fulfulde Stopwords LaTeX paper

set -e

PAPER="fulfulde_stopwords"

echo "==========================================="
echo "Compiling Fulfulde Stopwords Research Paper"
echo "==========================================="

# Check if pdflatex is available
if ! command -v pdflatex &> /dev/null; then
    echo "Error: pdflatex not found. Please install a LaTeX distribution."
    exit 1
fi

# Check if bibtex is available
if ! command -v bibtex &> /dev/null; then
    echo "Error: bibtex not found. Please install a LaTeX distribution."
    exit 1
fi

# Navigate to paper directory if not already there
cd "$(dirname "$0")"

echo ""
echo "Step 1/4: First pdflatex pass..."
pdflatex -interaction=nonstopmode "$PAPER.tex" > /dev/null || {
    echo "Error in first pdflatex pass. Check the log file."
    exit 1
}

echo "Step 2/4: Running bibtex..."
bibtex "$PAPER" > /dev/null || {
    echo "Error in bibtex. Check the bibliography."
    exit 1
}

echo "Step 3/4: Second pdflatex pass..."
pdflatex -interaction=nonstopmode "$PAPER.tex" > /dev/null || {
    echo "Error in second pdflatex pass. Check the log file."
    exit 1
}

echo "Step 4/4: Final pdflatex pass..."
pdflatex -interaction=nonstopmode "$PAPER.tex" > /dev/null || {
    echo "Error in final pdflatex pass. Check the log file."
    exit 1
}

echo ""
echo "==========================================="
echo "✓ Compilation successful!"
echo "PDF created: $PAPER.pdf"
echo "==========================================="

# Clean auxiliary files
echo ""
echo "Cleaning auxiliary files..."
rm -f *.aux *.log *.bbl *.blg *.out *.toc *.synctex.gz *.fdb_latexmk *.fls 2>/dev/null || true

echo "✓ Done!"
