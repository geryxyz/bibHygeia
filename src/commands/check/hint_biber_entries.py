import re

import pytest
from Levenshtein import ratio
from unidecode import unidecode

from src.util import BibEntry, Hint
from src.util.text import TranscriptionFunctions
from .fields_per_types import fields_per_types


@pytest.fixture()
def hint_remove_invalid_characters_from_key(entry: BibEntry, store_hint):
    clean_key = re.sub(r'[^a-zA-Z0-9_-]', '', entry.key)
    if entry.key != clean_key:
        store_hint(Hint(title='Valid BibTeX key',
                        recommendation=f'Change the entry key to "{clean_key}".',
                        reason='The entry key contains characters that are not allowed in BibTeX keys.',
                        phase='remove_invalid_characters_from_key'))


@pytest.fixture()
def hint_normalize_characters_in_key(entry: BibEntry, store_hint):
    normalized_key = re.sub(r'[^a-zA-Z0-9_-]', '', unidecode(entry.key))
    if entry.key != normalized_key:
        store_hint(Hint(title='Valid BibTeX key',
                        recommendation=f'Change the entry key to "{normalized_key}".',
                        reason='The entry key contains characters that are not allowed in BibTeX keys.',
                        phase='normalize_characters_in_key'))


@pytest.fixture()
def hint_readable_key(entry: BibEntry, store_hint):
    if entry['title'] is None:
        return

    clean_title = TranscriptionFunctions.lower(TranscriptionFunctions.drop_specials(entry['title']))
    if entry['title'] != clean_title:
        store_hint(Hint(title='Title based key',
                        recommendation=f'Change the key of "{entry.key}" to (at least starts with) "{clean_title}".',
                        reason='Most of the editor will offer suggestions and prefill the keys;'
                               ' furthermore these keys are easier to read during writing.',
                        phase='readable_key'))


@pytest.fixture()
def hint_similar_entry_type(entry: BibEntry, store_hint):
    for entry_type in fields_per_types.keys():
        if entry.entry_type == entry_type:
            continue

        rat = ratio(entry.entry_type, entry_type)
        if rat >= 0.75:
            store_hint(Hint(title='Similar BibTeX entry type',
                            recommendation=f'Change the entry type to "{entry_type}".',
                            reason='The type of the entry is similar to a valid type.',
                            phase='similar_entry_type'))


@pytest.fixture()
def hint_valid_entry_type(entry: BibEntry, store_hint):
    if entry.entry_type not in fields_per_types.keys():
        store_hint(Hint(title='Valid BibTeX entry type',
                        recommendation='Please use a valid BibTeX entry type.',
                        reason='We use the types specified at https://en.wikipedia.org/wiki/BibTeX#Entry_types',
                        phase='valid_entry_type'))
