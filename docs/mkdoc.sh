#!/bin/bash
pdflatex -halt-on-error rct_manual.tex -output-directory .
makeglossaries rct_manual
pdflatex -halt-on-error rct_manual.tex -output-directory .
makeglossaries rct_manual
pdflatex -halt-on-error rct_manual.tex -output-directory .
rm *.aux *.glg *.glo *.gls *.ist *.log *.toc *.out
