import os
import re
import typing

import bibtexparser
import glob2

from src.commands.check.bibtex_line import Line, type_regexes, UnrecognizedLine, EntryStartLine, FieldLine, \
    LastFieldLine
from src.util.BibEntry import BibEntry


class BibFile(object):
    """
    Class for reading BibTeX files.

    :param file_path: Path to the BibTeX file.
    """

    @staticmethod
    def read_bib_files(path: str, is_recursive: bool = True) -> typing.List["BibFile"]:
        """
        Reads all BibTeX files in the given path.

        :param path: The path to the BibTeX files.
        :param is_recursive: Whether to search recursively. (optional)
        :return: A list of BibFile objects.
        """

        bib_file_names: typing.List[str] = glob2.glob(os.path.join(path, "**", "*.bib"), recursive=is_recursive)
        bib_files: typing.List["BibFile"] = []

        for file in bib_file_names:
            bib_files.append(BibFile(file))

        return bib_files

    def __init__(self, file_path: str):
        self._file_path: str = file_path
        self._bibliography: bibtexparser.bibdatabase.BibDatabase
        self._entries: typing.List[BibEntry] = []
        self._preprocessed_lines: typing.List[Line] = []

        # Parse .bib file
        parser = bibtexparser.bparser.BibTexParser(common_strings=True, ignore_nonstandard_types=False)
        with open(file_path, "r", encoding="utf-8") as bibfile:
            self._bibliography: bibtexparser.bibdatabase.BibDatabase = bibtexparser.load(bibfile, parser)

        # Create BibEntry objects
        for entry in self._bibliography.entries:
            entry_line_number = self.line_of(entry["ID"])
            if entry_line_number:
                self._entries.append(BibEntry(entry, entry_line_number))

        # Preprocess lines
        self._preprocess_lines()

    @property
    def file_path(self) -> str:
        return self._file_path

    @property
    def entries(self) -> typing.List[BibEntry]:
        return self._entries

    @property
    def preprocessed_lines(self) -> typing.List[Line]:
        return self._preprocessed_lines

    def __iter__(self):
        return iter(self._entries)

    def __getitem__(self, item) -> BibEntry:
        return self._entries[item]

    def __str__(self) -> str:
        return f"BibFile(path='{self._file_path}', {len(self._entries)} entries)"

    def line_of(self, key: str) -> typing.Union[int, None]:
        """
        :param key: The key of the entry.
        :return: The line index of the entry or None if the entry is not found.
        """

        with open(self._file_path, "r", encoding="utf-8") as bibfile:
            for index, line in enumerate(bibfile):
                line = line.strip()
                if re.match(rf"^\s*@\w+{{{key}", line):
                    return index
        return None

    def _preprocess_lines(self):
        """
        Preprocesses the lines of the BibTeX file.
        """

        self._preprocessed_lines: typing.List[Line] = []
        with open(self._file_path, 'r', encoding='utf-8') as raw_file:
            for index, line in enumerate(raw_file):
                for _type, regex in type_regexes.items():
                    match = re.search(regex, line)
                    if match:
                        if len(self._preprocessed_lines) > 0 \
                                and type(self._preprocessed_lines[-1]) not in [EntryStartLine, FieldLine, LastFieldLine] \
                                and _type in [FieldLine, LastFieldLine] and match:
                            self._preprocessed_lines.append(UnrecognizedLine(line, index + 1))
                            break
                        self._preprocessed_lines.append(_type(line, match, index + 1))
                        break
                else:
                    self._preprocessed_lines.append(UnrecognizedLine(line, index + 1))

        # Debug lines
        # TODO: Remove
        for line in self._preprocessed_lines:
            print("Line", line.line_number, ":", type(line).__name__, line.raw, end="")
