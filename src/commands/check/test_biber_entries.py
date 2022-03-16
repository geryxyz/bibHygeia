import re

import pytest

from src.util.BibEntry import BibEntry
from src.util.constants import DUPLICATION_THRESHOLD, IGNORE_DUPLICATION_PROPERTY_NAME
from src.util.text import TranscriptionFunctions, jaccard_similarity
from .BibEntryQuantifierPair import BibEntryQuantifierPair
from .fields_per_types import fields_per_types
# noinspection PyUnresolvedReferences
from .hint_biber_entries import hint_remove_invalid_characters_from_key, hint_normalize_characters_in_key, \
    hint_readable_key, hint_valid_entry_type, hint_similar_entry_type
from .utils import biber_entries_gen, get_entry_by_key, entry_idfn, \
    biber_entries_with_field_quantifiers_idfn, biber_entries_with_field_quantifiers_gen


@pytest.mark.parametrize("entry", biber_entries_gen(), ids=entry_idfn)
def test_characters_in_key(entry: BibEntry, hint_remove_invalid_characters_from_key, hint_normalize_characters_in_key):
    assert re.match(rf"^[a-zA-Z0-9_-]+$", entry.key) is not None


@pytest.mark.parametrize("entry", biber_entries_gen(), ids=entry_idfn)
def test_readable_key(entry: BibEntry, hint_readable_key):
    if entry['title'] is None:
        return

    clean_title = TranscriptionFunctions.lower(TranscriptionFunctions.drop_specials(entry["title"]))
    assert re.match(rf"^{clean_title}", entry.key), \
        'Key "%s" should start with an easy to read version of the title' % entry.key


@pytest.mark.parametrize("entry", biber_entries_gen(), ids=entry_idfn)
def test_entry_type(entry: BibEntry, hint_valid_entry_type, hint_similar_entry_type):
    assert entry.entry_type in fields_per_types.keys(), 'Entry type "%s" is not valid' % entry.entry_type


@pytest.mark.parametrize("entry_quantifier", biber_entries_with_field_quantifiers_gen(),
                         ids=biber_entries_with_field_quantifiers_idfn)
def test_field_type(entry_quantifier: BibEntryQuantifierPair):
    entry_quantifier.quantifier.check(entry_quantifier.entry.key, entry_quantifier.entry)


@pytest.mark.parametrize("entry", biber_entries_gen(), ids=entry_idfn)
@pytest.mark.parametrize("other_entry", biber_entries_gen(), ids=entry_idfn)
def test_no_duplication(entry: BibEntry, other_entry: BibEntry):
    if entry is other_entry:
        return

    entry_ignored_keys = entry.fields.get(IGNORE_DUPLICATION_PROPERTY_NAME, '').split(',')
    if other_entry.key in entry_ignored_keys:
        return

    other_entry_ignored_keys = other_entry.fields.get(IGNORE_DUPLICATION_PROPERTY_NAME, '').split(',')
    if entry.key in other_entry_ignored_keys:
        return

    similarity = jaccard_similarity(entry["title"], other_entry["title"])

    assert similarity < DUPLICATION_THRESHOLD, \
        "Entries '%s' (line %d) and '%s' (line %d) are potentially duplicates, similarity = %.2f" \
        % (entry.key, entry.line_number, other_entry.key, other_entry.line_number, similarity)


@pytest.mark.parametrize("entry", biber_entries_gen(), ids=entry_idfn)
def test_right_use_of_noduplication(entry: BibEntry):
    ignored_keys = [k for k in entry.fields.get(IGNORE_DUPLICATION_PROPERTY_NAME, '').split(',') if k != '']
    for ignored_key in ignored_keys:
        assert get_entry_by_key(ignored_key), \
            'Unknown key "%s" specified as %s in entry "%s"' % (ignored_key, IGNORE_DUPLICATION_PROPERTY_NAME, entry.key)

        _entry = get_entry_by_key(ignored_key)
        similarity = jaccard_similarity(entry["title"], _entry["title"])

        assert similarity >= DUPLICATION_THRESHOLD, \
            'Entry "%s" and entry "%s" (specified in "%s") are not real duplicates, similarity = %.2f' \
            % (entry.key, ignored_key, entry.key, similarity)

        _ignored_keys = [k for k in _entry.fields.get(IGNORE_DUPLICATION_PROPERTY_NAME, '').split(',') if k != '']
        assert entry.key in _ignored_keys, \
            'Key "%s" is missing among "%s" references in entry "%s"' \
            % (entry.key, IGNORE_DUPLICATION_PROPERTY_NAME, ignored_key)
