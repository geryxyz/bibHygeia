import typing

from src.util import BibFile, BibEntry
from src.util.bibtex_line import Line, Context
from src.util.quantifier import Quantifier, Forbidden, Mandatory, AllOf, AtLeastOneOf, MaybeOneOf
from .BibEntryQuantifierPair import BibEntryQuantifierPair
from .CheckCommand import bib_files
from .fields_per_types import fields_per_types


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


def biber_entries_with_field_quantifiers_gen():
    for entry in biber_entries_gen():
        for quantifier in fields_per_types.get(entry.entry_type, ()):
            yield BibEntryQuantifierPair(entry, quantifier)


def line_idfn(prefix: str = "Line"):
    """
    Returns a function that returns an ID for a line in the test.
    """

    def _line_idfn(fixture_value: typing.Any):
        if isinstance(fixture_value, Line):
            return "%s %d" % (prefix, fixture_value.line_number)
        return None

    return _line_idfn


def entry_idfn(entry: BibEntry):
    if isinstance(entry, BibEntry):
        return entry.key
    return None


def quantifier_idfn(quantifier: Quantifier):
    if isinstance(quantifier, (Mandatory, Forbidden)):
        return quantifier.name
    elif isinstance(quantifier, (AllOf, AtLeastOneOf, MaybeOneOf)):
        return "-".join(quantifier.names)

    return None


def biber_entries_with_field_quantifiers_idfn(entry_quantifier: BibEntryQuantifierPair):
    if not isinstance(entry_quantifier, BibEntryQuantifierPair):
        return None

    if isinstance(entry_quantifier.quantifier, (Mandatory, Forbidden)):
        return f"{entry_quantifier.entry.key}_{entry_quantifier.quantifier.__class__.__name__}_{entry_quantifier.quantifier.name}"

    elif isinstance(entry_quantifier.quantifier, (AllOf, AtLeastOneOf, MaybeOneOf)):
        return f"{entry_quantifier.entry.key}_{entry_quantifier.quantifier.__class__.__name__}_" + \
               "-".join(entry_quantifier.quantifier.names)

    return None


def get_entry_by_key(key: str) -> typing.Union[BibEntry, None]:
    """
    Returns the entry with the given key.
    """

    for entry in biber_entries_gen():
        if entry.key == key:
            return entry
    return None
