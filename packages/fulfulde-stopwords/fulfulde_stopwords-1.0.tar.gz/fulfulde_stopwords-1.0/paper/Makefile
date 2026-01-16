# Makefile for compiling the Fulfulde Stopwords research paper

# Variables
PAPER = fulfulde_stopwords
TEX = $(PAPER).tex
PDF = $(PAPER).pdf
BIB = references.bib

# Default target
all: $(PDF)

# Compile PDF
$(PDF): $(TEX) $(BIB)
	@echo "Compiling $(PAPER)..."
	pdflatex $(TEX)
	bibtex $(PAPER)
	pdflatex $(TEX)
	pdflatex $(TEX)
	@echo "Done! PDF created: $(PDF)"

# Quick compile (single pass, for quick previews)
quick:
	pdflatex $(TEX)

# Clean auxiliary files
clean:
	rm -f *.aux *.log *.bbl *.blg *.out *.toc *.synctex.gz *.fdb_latexmk *.fls

# Clean everything including PDF
cleanall: clean
	rm -f $(PDF)

# View PDF (requires a PDF viewer)
view: $(PDF)
	@if command -v xdg-open > /dev/null; then \
		xdg-open $(PDF); \
	elif command -v open > /dev/null; then \
		open $(PDF); \
	else \
		echo "Please open $(PDF) manually"; \
	fi

# Help
help:
	@echo "Makefile for Fulfulde Stopwords paper"
	@echo ""
	@echo "Usage:"
	@echo "  make          - Compile the paper (full compilation with bibliography)"
	@echo "  make quick    - Quick compile (single pass, no bibliography)"
	@echo "  make clean    - Remove auxiliary files"
	@echo "  make cleanall - Remove all generated files including PDF"
	@echo "  make view     - Open the PDF"
	@echo "  make help     - Show this help message"

.PHONY: all quick clean cleanall view help
