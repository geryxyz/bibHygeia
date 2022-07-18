import os
import re
import typing

import bibtexparser
import glob2

from src.util.bibtex_line import Line, type_regexes, UnrecognizedLine, EntryStartLine, Context, ClosingFieldLine, \
    EntryEndLine, FieldLine, LastFieldLine
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

        if os.path.isfile(path):
            return [BibFile(path)]

        bib_file_names: typing.List[str] = glob2.glob(os.path.join(path, "**", "*.bib"), recursive=is_recursive)
        bib_files: typing.List["BibFile"] = []

        for file in bib_file_names:
            bib_files.append(BibFile(file))

        return bib_files

    def __init__(self, file_path: str):
        self._file_path = file_path
        self._bibliography: bibtexparser.bibdatabase.BibDatabase
        self._entries: typing.List[BibEntry] = []
        self._preprocessed_lines: typing.List[Line] = []
        self._contexts: typing.List[Context] = []

        # Parse .bib file
        parser = bibtexparser.bparser.BibTexParser(common_strings=True, ignore_nonstandard_types=False)
        with open(file_path, "r", encoding="utf-8") as bibfile:
            self._bibliography: bibtexparser.bibdatabase.BibDatabase = bibtexparser.load(bibfile, parser)

        # Create BibEntry objects
        for entry in self._bibliography.entries:
            entry_line_number = self.line_of(entry["ID"])
            if entry_line_number:
                self._entries.append(BibEntry(entry, file_path, entry_line_number))

        # Preprocess lines
        self._preprocess_lines()
        self._preprocess_contexts()

    @property
    def file_path(self) -> str:
        return self._file_path

    @property
    def entries(self) -> typing.List[BibEntry]:
        return self._entries

    @property
    def preprocessed_lines(self) -> typing.List[Line]:
        return self._preprocessed_lines

    @property
    def contexts(self) -> typing.List[Context]:
        return self._contexts

    def __iter__(self):
        return iter(self._entries)

    def __getitem__(self, item) -> BibEntry:
        return self._entries[item]

    def __str__(self) -> str:
        return f"BibFile(path='{self._file_path}', {len(self._entries)} entries)"

    def line_of(self, key: str) -> typing.Union[int, None]:
        """
        :param key: The key of the entry.
        :return: The line number of the entry or None if the entry is not found.
        """

        # TODO: Optimization: Use a dictionary to map keys to line numbers in the init method.
        with open(self._file_path, "r", encoding="utf-8") as bibfile:
            for index, line in enumerate(bibfile):
                line = line.strip()
                if re.match(rf"^\s*@\w+{{{key}", line):
                    return index + 1
        return None

    def _preprocess_lines(self):
        """
        Preprocesses the lines of the BibTeX file.
        """

        self._preprocessed_lines: typing.List[Line] = []
        is_in_entry: bool = False

        with open(self._file_path, 'r', encoding='utf-8') as raw_file:
            for index, line in enumerate(raw_file):
                for _type, regex in type_regexes.items():
                    match = re.search(regex, line)
                    if match:
                        # Store line as UnrecognizedLine if it is not in an entry
                        if not is_in_entry and _type in [FieldLine, LastFieldLine, ClosingFieldLine, EntryEndLine]:
                            self._preprocessed_lines.append(UnrecognizedLine(line, self.file_path, index + 1))
                            break

                        preprocessed_line: Line = _type(line, match, self.file_path, index + 1)
                        if isinstance(preprocessed_line, EntryStartLine):
                            is_in_entry = True
                        elif isinstance(preprocessed_line, (ClosingFieldLine, EntryEndLine)):
                            is_in_entry = False

                        self._preprocessed_lines.append(preprocessed_line)
                        break
                else:
                    self._preprocessed_lines.append(UnrecognizedLine(line, self.file_path, index + 1))

    def _preprocess_contexts(self):
        """
        Preprocesses the contexts of the BibTeX file.
        """

        context: typing.Optional[Context] = None
        for line in self._preprocessed_lines:
            if isinstance(line, EntryStartLine):
                if context:
                    self._contexts.append(context)
                context = Context()

            if context:
                context.lines.append(line)
                line.context = context
                if isinstance(line, (EntryEndLine, ClosingFieldLine)):
                    self._contexts.append(context)
                    context = None
