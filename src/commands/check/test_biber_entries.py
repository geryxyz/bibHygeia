import typing
import re
import pytest

from src.util.text import OMISSION_CHAR, TranscriptionFunctions
from .fields_per_types import fields_per_types
from .CheckCommand import input_biber_entries


@pytest.mark.parametrize("entry", input_biber_entries(), ids=lambda x: x["ID"])
def test_characters_in_id(entry: typing.Dict[str, typing.Any]):
    assert re.match(rf"^[a-zA-Z0-9_{OMISSION_CHAR}]+$", entry['ID']) is not None, \
        "ID '%s' should contain a-z, A-Z, 0-9 or %s only" % (entry['ID'], OMISSION_CHAR)


@pytest.mark.parametrize("entry", input_biber_entries(), ids=lambda x: x["ID"])
def test_readable_id(entry: typing.Dict[str, typing.Any]):
    clean_title = TranscriptionFunctions.lower(TranscriptionFunctions.drop_specials(entry["title"]))

    assert re.match(rf"^{clean_title}", entry["ID"]), \
        "ID '%s' should start with an easy to read version of the title" % entry['ID']


@pytest.mark.parametrize("entry", input_biber_entries(), ids=lambda x: x["ID"])
def test_entry_type(entry: typing.Dict[str, typing.Any]):
    assert entry["ENTRYTYPE"] in fields_per_types


@pytest.mark.parametrize("entry", input_biber_entries(), ids=lambda x: x["ID"])
def test_field_type(entry: typing.Dict[str, typing.Any]):
    entry_type = entry["ENTRYTYPE"]
    for quantifier in fields_per_types.get(entry_type, ()):
        quantifier.check(entry["ID"], entry)

