import re
import unittest

import typing

from owl.core.decorators import biber_entry_checkers, HINTER_ATTR_NAME, biber_file_checkers, HINT_ATTR_NAME, \
    assign_hint_to, LINE_TYPE_ATTR_NAME
from owl.util.bibtex_line_type import UnrecognizedLine, Context, EntryStartLine, Line, type_regexes
from owl.util.HTMLRunner import HTMLRunner
from owl.util.BibFile import BibFile
from owl.util.LaTeXmk import BIBFILE_NAME
from owl.util.reflection import get_descent_classes
from owl.util.statistical_constants import COUNT_OF_CLASSIFIED_BIBFILE_LINES, COUNT_OF_CHECKED_BIBFILE_LINES, \
    COUNT_OF_CHECKED_ENTRIES, COUNT_OF_BIBFILE_LINE_CHECKING


class TestBiberValidation(unittest.TestCase):
    bib_file: BibFile

    @classmethod
    def setUpClass(cls) -> None:
        cls.bib_file: BibFile = BibFile(BIBFILE_NAME)

    def test_biber_entries(self):
        HTMLRunner.statistics[COUNT_OF_CHECKED_ENTRIES] = 0
        for key, entry in TestBiberValidation.bib_file.bibliography.entries_dict.items():
            HTMLRunner.statistics[COUNT_OF_CHECKED_ENTRIES] += 1
            checker: typing.Callable[[str, typing.Dict[str, typing.Any], BibFile, unittest.TestCase], None]
            for checker in biber_entry_checkers:
                with self.subTest('checking entry', key=key, checker=checker.__name__):
                    try:
                        checker(key, entry, TestBiberValidation.bib_file, self)
                    finally:
                        if hasattr(checker, HINTER_ATTR_NAME):
                            for hinter in getattr(checker, HINTER_ATTR_NAME):
                                hint = hinter(key, entry, TestBiberValidation.bib_file)
                                if hint is not None:
                                    assign_hint_to(self, hint)

    def test_bib_file_lines(self):
        preprocessed_lines: typing.List[Line] = []
        with open(TestBiberValidation.bib_file.file_path, 'r', encoding='utf-8') as raw_file:
            HTMLRunner.statistics[COUNT_OF_CLASSIFIED_BIBFILE_LINES] = 0
            HTMLRunner.statistics[COUNT_OF_CHECKED_BIBFILE_LINES] = 0
            HTMLRunner.statistics[COUNT_OF_BIBFILE_LINE_CHECKING] = 0
            for index, line in enumerate(raw_file):
                with self.subTest('classifying bibtex line', line=line.strip()):
                    for _type, regex in type_regexes.items():
                        match = re.search(regex, line)
                        if match:
                            preprocessed_lines.append(_type(line, match))
                            HTMLRunner.statistics[COUNT_OF_CLASSIFIED_BIBFILE_LINES] += 1
                            break
                    else:
                        preprocessed_lines.append(UnrecognizedLine(line))
                        self.fail(f'Unrecognized type of line in the bibtex file at line#{index + 1}: {line}')

            contexts = []
            current_context = Context()
            for line in preprocessed_lines:
                if isinstance(line, EntryStartLine):
                    contexts.append(current_context)
                    current_context = Context()
                current_context.lines.append(line)

            for context in contexts:
                for index, line in enumerate(context.lines):
                    line_checked = False
                    for checker in biber_file_checkers:
                        if hasattr(checker, LINE_TYPE_ATTR_NAME):
                            requested_line_type = getattr(checker, LINE_TYPE_ATTR_NAME)
                            is_type_requested = \
                                requested_line_type in get_descent_classes(Line) and type(line) is requested_line_type
                            is_type_among_requested = \
                                (isinstance(requested_line_type, list) or isinstance(requested_line_type, tuple)) and\
                                type(line) in requested_line_type
                            is_no_type_requested = requested_line_type is None
                            if is_type_requested or is_type_among_requested or is_no_type_requested:
                                with self.subTest('checking bibtex line', line=line.raw.strip('\n'), checker=checker.__name__):
                                    try:
                                        if not line_checked:
                                            HTMLRunner.statistics[COUNT_OF_CHECKED_BIBFILE_LINES] += 1
                                            line_checked = True
                                        HTMLRunner.statistics[COUNT_OF_BIBFILE_LINE_CHECKING] += 1
                                        checker(line, context, self)
                                    finally:
                                        if hasattr(checker, HINTER_ATTR_NAME):
                                            for hinter in getattr(checker, HINTER_ATTR_NAME):
                                                hint = hinter(line, context, TestBiberValidation.bib_file)
                                                if hint is not None:
                                                    assign_hint_to(self, hint)
