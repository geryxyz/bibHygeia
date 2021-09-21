import typing
import unittest

from owl.checking.fields_per_types import fields_per_types
from owl.core.decorators import biber_entry_checker, hinted
from owl.hinting.hint import title_as_key, field_definitions
from owl.util.BibFile import BibFile
from owl.util.constants import ENTRYTYPE_PROPERTY_NAME
from owl.util.text import OMISSION_CHAR, jaccard_of, TranscriptionFunctions


@biber_entry_checker
def characters_in_id(key: str, entry: typing.Dict[str, typing.Any], bib_file, test: unittest.TestCase):
    test.assertNotRegex(key, rf'[^a-zA-Z0-9{OMISSION_CHAR}]', f'key should contain a-z, A-Z, 0-9 or {OMISSION_CHAR} only')


@biber_entry_checker
@hinted(hinter=title_as_key)
def readable_key(key: str, entry: typing.Dict[str, typing.Any], bib_file, test: unittest.TestCase):
    clean_title = TranscriptionFunctions.lower(TranscriptionFunctions.drop_specials(entry['title']))
    test.assertRegex(key, rf'^{clean_title}', 'key should start with an easy to read version of the title')


IGNORE_DUPLICATION_PROPERTY_NAME = "noduplication"
DUPLICATION_LIMIT = .8


@biber_entry_checker
def no_duplication(key: str, entry: typing.Dict[str, typing.Any], bib_file: BibFile, test: unittest.TestCase):
    key_line = None
    _key_line = None
    for _key, _entry in bib_file.bibliography.entries_dict.items():
        if key == _key:
            continue
        ignored_keys = entry.get(IGNORE_DUPLICATION_PROPERTY_NAME, '').split(',')
        if _key in ignored_keys:
            continue
        _ignored_keys = _entry.get(IGNORE_DUPLICATION_PROPERTY_NAME, '').split(',')
        if key in _ignored_keys:
            continue
        similarity = jaccard_of(entry['title'], _entry['title'])
        if similarity >= DUPLICATION_LIMIT:
            _key_line = bib_file.line_of(_key)
            key_line = bib_file.line_of(key)
        test.assertLess(
            similarity,
            DUPLICATION_LIMIT,
            f'entry "{key}" (line {key_line}) and "{_key}" (line {_key_line}) are possible duplicates, similarity = {similarity}')


@biber_entry_checker
def right_use_of_noduplication(key: str, entry: typing.Dict[str, typing.Any], bib_file: BibFile, test: unittest.TestCase):
    ignored_keys = [k for k in entry.get(IGNORE_DUPLICATION_PROPERTY_NAME, '').split(',') if k != '']
    for ignored_key in ignored_keys:
        test.assertIn(
            ignored_key,
            bib_file.bibliography.entries_dict,
            f'unknown key "{ignored_key}" specified as {IGNORE_DUPLICATION_PROPERTY_NAME} in entry "{key}"')
        _entry = bib_file.bibliography.entries_dict.get(ignored_key, None)
        similarity = jaccard_of(entry['title'], _entry['title'])
        test.assertGreaterEqual(
            similarity,
            DUPLICATION_LIMIT,
            f'entry "{key}" and entry "{ignored_key}" (specified in "{key}") are not real duplicates,'
            f' similarity = {similarity}')
        _ignored_keys = [k for k in _entry.get(IGNORE_DUPLICATION_PROPERTY_NAME, '').split(',') if k != '']
        test.assertIn(
            key,
            _ignored_keys,
            f'key {key} is missing among {IGNORE_DUPLICATION_PROPERTY_NAME} references in entry "{ignored_key}"')


@biber_entry_checker
def entry_type_checker(key: str, entry: typing.Dict[str, typing.Any], bib_file: BibFile, test: unittest.TestCase):
    test.assertIn(entry[ENTRYTYPE_PROPERTY_NAME], fields_per_types)


@biber_entry_checker
@hinted(hinter=field_definitions)
def entry_field_checker(key: str, entry: typing.Dict[str, typing.Any], bib_file: BibFile, test: unittest.TestCase):
    entry_type = entry[ENTRYTYPE_PROPERTY_NAME]
    for quantifier in fields_per_types.get(entry_type, ()):
        quantifier.check(key, entry, test)
