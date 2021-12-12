import os
import re
import typing

import bibtexparser
import glob2


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
        self.file_path: str = file_path
        self.bibliography: bibtexparser.bibdatabase.BibDatabase

        parser = bibtexparser.bparser.BibTexParser(common_strings=True, ignore_nonstandard_types=False)
        with open(file_path, "r", encoding="utf-8") as bibfile:
            self.bibliography: bibtexparser.bibdatabase.BibDatabase = bibtexparser.load(bibfile, parser)

    def line_of(self, key: str) -> typing.Union[int, None]:
        """
        :param key: The key of the entry.
        :return: The line index of the entry or None if the entry is not found.
        """

        with open(self.file_path, "r", encoding="utf-8") as bibfile:
            for index, line in enumerate(bibfile):
                line = line.strip()
                if re.match(rf"^@\w+{{{key}", line):
                    return index
        return None

    def __str__(self) -> str:
        return f"BibFile(path='{self.file_path}', {len(self.bibliography.entries)} entries)"
