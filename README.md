# bibHygeia Bibtex Toolkit

<img src="/media/bibHygeia.png" alt="logo" width="200"/>

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

## Restore - handle saved state

This tool can be used to restore or remove saved state stored in original files.

### Usage
```
usage: restore.py [-h] -i INPUT_FOLDER [--drop_original DROP_ORIGINAL]
                  [--log LOG]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_FOLDER, --input_folder INPUT_FOLDER
                        input folder to searching original files recursively
                        (default: None)
  --drop_original DROP_ORIGINAL
                        remove all original files (default: False)
  --log LOG             level of log messages to display (default: INFO)
```

## Show - display details

This tool allow the user to inspect various items in supported files.

```
usage: show.py [-h] -i INPUT [--id ID] [--log LOG]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input file or folder to inspect (default: None)
  --id ID               Regular expression to select BibTeX id for the entry
                        to inspect (default: None)
  --log LOG             level of log messages to display (default: INFO)
```

## Unify - regenerate properties and ids

Unify allow the user to regenerate any target property including ids based other properties in the same entry.

```
usage: unify.py [-h] -i INPUT [-t TARGET] [-p PATTERN]
                [--remove_special_chars REMOVE_SPECIAL_CHARS]
                [--remove_unresolved_refs REMOVE_UNRESOLVED_REFS]
                [--ignore_unresolved_refs IGNORE_UNRESOLVED_REFS] [--log LOG]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input file to unify (default: None)
  -t TARGET, --target TARGET
                        name of the target property. Use "ID" for id.
                        (default: ID)
  -p PATTERN, --pattern PATTERN
                        pattern to change the property value. Use
                        "@{property}" for values of other properties (default:
                        @{ID})
  --remove_special_chars REMOVE_SPECIAL_CHARS
                        if true, all special chars (\W) will be removed from
                        substituted properties value (default: True)
  --remove_unresolved_refs REMOVE_UNRESOLVED_REFS
                        if true, all unresolved property reference will be
                        removed from new value (default: True)
  --ignore_unresolved_refs IGNORE_UNRESOLVED_REFS
                        if true, all unresolved property reference will be
                        ignored (default: False)
  --log LOG             level of log messages to display (default: INFO)
```

For sample usage to regenerate ids consider pattern `@{author}:@{year}:@{title}` if you are using entries (resources) without `year` or `author` properties, like webpages.
You could use `@{author}:@{year}` for a more "traditional" id for academic papers and books.
Please note that all unresolved (pointing to non-existing properties) references will be removed by default,
but you are able to override this behaviour.