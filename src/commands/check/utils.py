import typing

from src.util import BibFile, BibEntry

from .CheckCommand import bib_files
from src.util.bibtex_line import Line, Context


def biber_files_gen() -> typing.List[BibFile]:
    """
    Iterates over the bib files and yields the bib files.
    """

    yield from bib_files


def biber_entries_gen() -> typing.List[BibEntry]:
    """
    Iterates over the bib files and yields the biber entries.
    """

    for bib_file in bib_files:
        yield from bib_file.entries


def lines_gen(*line_type: typing.Type[Line]) -> typing.List[Line]:
    """
    Iterates over the bib files and yields the lines.
    """

    for bib_file in bib_files:
        for line in bib_file.preprocessed_lines:
            if len(line_type) == 0 or type(line) in line_type:
                yield line


def contexts_gen() -> typing.List[Context]:
    """
    Iterates over the bib files and yields the contexts.
    """

    for bib_file in bib_files:
        yield from bib_file.contexts


def lines_in_contexts_gen() -> typing.List[Line]:
    """
    Iterates over the contexts and yields the lines.
    """

    for bib_file in bib_files:
        for context in bib_file.contexts:
            yield from context.lines


def line_idfn(prefix: str = "Line"):
    """
    Returns a function that returns an ID for a line in the test.
    """

    def _line_idfn(fixture_value: typing.Any):
        if isinstance(fixture_value, Line):
            return "%s %d" % (prefix, fixture_value.line_number)
        return None
    return _line_idfn
