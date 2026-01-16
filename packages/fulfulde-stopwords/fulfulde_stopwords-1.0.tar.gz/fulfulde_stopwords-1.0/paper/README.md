# Research Paper: Fulfulde Stopwords

This directory contains the LaTeX source for the research paper:

**"Fulfulde Stopwords: A Linguistic Resource for Natural Language Processing in a Low-Resource African Language"**

## Files

- `fulfulde_stopwords.tex` - Main LaTeX document
- `references.bib` - BibTeX bibliography file
- `README.md` - This file

## Compiling the Paper

To compile the paper, you need a LaTeX distribution (e.g., TeX Live, MiKTeX) installed.

### Using the compile script (recommended)

```bash
cd paper
./compile.sh
```

This script automatically runs all necessary compilation steps and cleans up auxiliary files.

### Using Make

```bash
cd paper
make          # Full compilation with bibliography
make quick    # Quick preview (single pass)
make clean    # Remove auxiliary files
make cleanall # Remove all generated files
```

### Manual compilation with pdflatex

```bash
cd paper
pdflatex fulfulde_stopwords.tex
bibtex fulfulde_stopwords
pdflatex fulfulde_stopwords.tex
pdflatex fulfulde_stopwords.tex
```

**Important**: You must run pdflatex → bibtex → pdflatex → pdflatex to properly generate the bibliography.

### Using latexmk

```bash
cd paper
latexmk -pdf fulfulde_stopwords.tex
```

### Using Overleaf

1. Upload `fulfulde_stopwords.tex` and `references.bib` to a new Overleaf project
2. Compile (should work automatically)

## Required LaTeX Packages

The document uses the following packages (should be included in standard distributions):

- inputenc, fontenc
- times, microtype
- graphicx
- booktabs, multirow, longtable, array
- url, hyperref
- amsmath
- enumitem
- xcolor
- tipa (for phonetic symbols)
- natbib (for bibliography)
- listings (for code)
- geometry (for page layout)
- titlesec (for section formatting)

## Structure

The paper follows a standard research article structure:

1. **Abstract**
2. **Introduction** - Motivation and contributions
3. **Related Work** - Prior work on stopwords and African NLP
4. **Linguistic Background** - Fulfulde language features
5. **Methodology** - Corpus collection, frequency analysis, validation
6. **The Resource** - Description of the stopword list and library
7. **Evaluation** - Text classification and information retrieval experiments
8. **Discussion** - Implications and limitations
9. **Conclusion** - Summary and future work
10. **Appendix** - Complete stopword list

## Target Venues

This paper is suitable for submission to:

- **Language Resources and Evaluation (LREC) Conference**
- **Language Resources and Evaluation Journal** (Springer)
- **ACL Workshop on African Natural Language Processing**
- **IJCNLP** (International Joint Conference on Natural Language Processing)
- **Journal of Language Resources**

## Citation

If you use this resource in your research, please cite:

```bibtex
@article{fulfulde_stopwords_2026,
  title={Fulfulde Stopwords: A Linguistic Resource for NLP in a Low-Resource African Language},
  author={Research Team},
  journal={Language Resources and Evaluation},
  year={2026},
  publisher={Springer}
}
```

## License

The paper and all associated materials are released under the MIT License.

## Contact

For questions or collaborations:
- Email: contact@example.com
- GitHub: https://github.com/2zalab/fulfulde-stopwords
