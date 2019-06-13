# bibHygeia Bibtex Toolkit

This toolkit allows to automate some housekeeping around Bibtex files.

## DeDup - duplication finder and database merger

Filtering duplicated entries based on [Jaccard similarity](https://en.wikipedia.org/wiki/Jaccard_index) by words.

### Usage
```
usage: dedup.py [-h] -i INPUT_FOLDER [-o OUTPUT_FILE] [-e EXCLUDE_PATTERN]
                [-p INSPECTED_PROPERTY] [-l SIMILARITY_LIMIT] [--log LOG]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FOLDER, --input_folder INPUT_FOLDER
                        input folder to searching *.bib files recursively
                        (default: None)
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        input folder to searching *.bib files recursively
                        (default: merged.bib)
  -e EXCLUDE_PATTERN, --exclude_pattern EXCLUDE_PATTERN
                        regular expression to exclude irrelevant sub-folder
                        (default: None)
  -p INSPECTED_PROPERTY, --inspected_property INSPECTED_PROPERTY
                        the property of the entries to check for similarity
                        (default: title)
  -l SIMILARITY_LIMIT, --similarity_limit SIMILARITY_LIMIT
                        lower limit for similarity between entries which
                        considered equal (default: 0.6)
  --log LOG             level of log messages to display (default: INFO)
```

## Upgrade - upgrade your LaTex files after BibTex database changes

This tool will use the log of other tools to upgrade LaTeX files. It will replace any occurrences of the old ID with the new one for any changed entry. Every other thing left unchanged.

### Usage
```
upgrade.py [-h] -u UPGRADE_FILE -i INPUT_FOLDER [-e EXCLUDE_PATTERN]
                  [--log LOG]

optional arguments:
  -h, --help            show this help message and exit
  -u UPGRADE_FILE, --upgrade_file UPGRADE_FILE
                        file containing the action (side-effects) of other
                        tool (default: None)
  -i INPUT_FOLDER, --input_folder INPUT_FOLDER
                        input folder to searching *.tex files recursively
                        (default: None)
  -e EXCLUDE_PATTERN, --exclude_pattern EXCLUDE_PATTERN
                        regular expression to exclude irrelevant sub-folder
                        (default: None)
  --log LOG             level of log messages to display (default: INFO)
```