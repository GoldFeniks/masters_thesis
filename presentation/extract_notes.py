#!/usr/bin/python

import re
import os
import argparse

parser = argparse.ArgumentParser(description=r'Extract \note macro from LaTeX file')
parser.add_argument('input', help='Path to input file', type=str)
parser.add_argument('output', help='Path to ouptut directory', type=str)
args = parser.parse_args()

os.makedirs(args.output, exist_ok=True)

preamble = r'''\documentclass{fefu}
\usepackage{nicefrac}

\newcounter{slide}
\setlength{\parindent}{0cm}
\newcommand{\slide}{\stepcounter{slide}\par\noindent\textbf{Слайд №\theslide}\par\noindent}

\newcommand{\pa}[1]{\left(#1\right)}

\setstretch{1}

\begin{document}'''

data = open(args.input).read()
data = re.sub(r'^%.*$', '', data, flags=re.MULTILINE)

print(preamble, *(f'    \\slide\n    {i.strip()}' for i in re.findall(r'\\note{((?:[^{}]+?|{[^{}]+?})*?)}', data, flags=re.DOTALL)), r'\end{document}', sep='\n', file=open(os.path.join(args.output, 'document.tex'), 'w'))
