# Wan Shi Tong

A repo for Biber files used during the research of software testing.  
Lore of naming: https://avatar.fandom.com/wiki/Wan_Shi_Tong

## Video Tutorials

https://youtube.com/playlist?list=PLvh2Ik9PEvSkyj1l6keYGjrFP8DlASZ-w

## Usage Notes for Biber and BibLaTeX

+ CTAN Biber: https://ctan.org/pkg/biber
+ CTAN BibLaTeX: https://ctan.org/pkg/biblatex
+ Overleaf guides: https://www.overleaf.com/learn/latex/Articles/Getting_started_with_BibLaTeX


+ BibLaTeX Cheat Sheet: http://tug.ctan.org/info/biblatex-cheatsheet/biblatex-cheatsheet.pdf
+ Tame the BeaST, The B to X of BibTEX: https://mirror.szerverem.hu/ctan/info/bibtex/tamethebeast/ttb_en.pdf (We use biber and not bibtex, but their file format are almost identical)

## Dependencies

### For Usage during Writting
+ Some LaTeX distribution with [LaTeXmk](https://www.ctan.org/pkg/latexmk), recommended: [MikTeX](https://miktex.org/) for Windows or [TeXLive](http://tug.org/texlive/) for Linux
+ Perl distribution (for LaTeXmk), recommended: [Active Perl](https://www.activestate.com/products/perl/)

### For Executing Tests Locally
+ [Python](https://www.python.org/) 3.9 or newer
+ [Pip](https://pypi.org/project/pip/) (usually part of Python distributions)
+ glob2 (`python3 -m pip install glob2`) and bibtexparser (`python3 -m pip install bibtexparser`) packages
+ Optional: Python development environment or editor, recommended: [JetBrains PyCharm](https://www.jetbrains.com/pycharm/)

## How to Execute Tests Locally

1. Clone the repository.
2. Open the root directory in PyCharm.
3. Create a new Run/Debug configuration for `owl/check.py`.  
   *Script path:* `owl/check.py`  
   *Parameters:* none  
   *Working directory:* working copy root  
   *Add content roots to PYTHONPATH:* true  
   *Add source roots to PYTHONPATH:* true
4. Execute the configuration.
5. Inspect report.html or the execution log.