# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('../src'))

project = 'htrdrPy'
copyright = '2026, Anthony Arfaux'
author = 'Anthony Arfaux'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
        'sphinx.ext.napoleon',  # Add napoleon to the extensions list
        'sphinx.ext.autodoc',
        'sphinx.ext.viewcode',
        'myst_parser',
        'sphinx_rtd_theme'      # Add the Read The Docs theme
        ]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

templates_path = ['_templates']
exclude_patterns = []

autoclass_content = 'both'

# -- Options for LATEX output -------------------------------------------------
latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '10pt',
    'preamble': r'''
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{textcomp}
\usepackage{enumitem}
\setlistdepth{9}
\renewlist{itemize}{itemize}{9}
\setlist[itemize]{label=\textbullet}
\setlist[itemize,1]{label=\textbullet}
\setlist[itemize,2]{label=\textbullet}
\setlist[itemize,3]{label=\textbullet}
\setlist[itemize,4]{label=\textbullet}
\setlist[itemize,5]{label=\textbullet}
\setlist[itemize,6]{label=\textbullet}
\setlist[itemize,7]{label=\textbullet}
\setlist[itemize,8]{label=\textbullet}
\setlist[itemize,9]{label=\textbullet}

\let\oldsphinxtableofcontents\sphinxtableofcontents
\renewcommand{\sphinxtableofcontents}{%
    \setcounter{tocdepth}{6}%
    \oldsphinxtableofcontents%
}
    ''',
    'tocdepth': '6',
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
