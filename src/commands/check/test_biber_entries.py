import re
import pytest

from src.util.text import OMISSION_CHAR, TranscriptionFunctions
from src.util.BibEntry import BibEntry
from .fields_per_types import fields_per_types
from .CheckCommand import input_biber_entries


@pytest.mark.parametrize("entry", input_biber_entries(), ids=lambda entry: entry.id)
def test_characters_in_id(entry: BibEntry):
    assert re.match(rf"^[a-zA-Z0-9_{OMISSION_CHAR}]+$", entry.id) is not None, \
        "ID '%s' should contain a-z, A-Z, 0-9 or %s only" % (entry.id, OMISSION_CHAR)


@pytest.mark.parametrize("entry", input_biber_entries(), ids=lambda entry: entry.id)
def test_readable_id(entry: BibEntry):
    clean_title = TranscriptionFunctions.lower(TranscriptionFunctions.drop_specials(entry["title"]))
    assert re.match(rf"^{clean_title}", entry.id), \
        "ID '%s' should start with an easy to read version of the title" % entry.id


@pytest.mark.parametrize("entry", input_biber_entries(), ids=lambda entry: entry.id)
def test_entry_type(entry: BibEntry):
    assert entry.entry_type in fields_per_types


@pytest.mark.parametrize("entry", input_biber_entries(), ids=lambda entry: entry.id)
def test_field_type(entry: BibEntry):
    for quantifier in fields_per_types.get(entry.entry_type, ()):
        quantifier.check(entry.id, entry)

