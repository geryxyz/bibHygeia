import re

import typing

from owl.checking.fields_per_types import fields_per_types
from owl.util.BibFile import BibFile
from owl.util.Hint import Hint
from owl.util.bibtex_line_type import Context, LastFieldLine
from owl.util.constants import ENTRYTYPE_PROPERTY_NAME
from owl.util.text import TranscriptionFunctions

name_of_month_in_english = {
    1: ['january', 'jan'],
    2: ['february', 'feb'],
    3: ['march', 'mar'],
    4: ['april', 'apr'],
    5: ['may'],
    6: ['june', 'jun'],
    7: ['july', 'jul'],
    8: ['august', 'aug'],
    9: ['september', 'sept'],
    10: ['october', 'oct'],
    11: ['november', 'nov'],
    12: ['december', 'dec'],
}


def month_name_to_index(name: str):
    for month_index, names in name_of_month_in_english.items():
        if name.lower() in names:
            return month_index
    return None


def warn_about_month_field(line: str, bib_file: BibFile) -> typing.Union[Hint, None]:
    non_number_month_match = re.match(r'^WARN - month field \'(?P<month>.+)\' in entry \'(?P<key>.+)\' is not an integer', line)
    if non_number_month_match:
        key = non_number_month_match.group('key')
        month = non_number_month_match.group('month')
        month_index = month_name_to_index(month)
        line_number = bib_file.line_of(key)
        if month_index is not None:
            recommendation = f'Replace the month field of entry \'{key}\' at line {line_number} with {month_index}'
        else:
            recommendation = f'Sorry, but I do not know which month is \'{month}\' in entry \'{key}\' at line {bib_file.line_of(key)}'
        return Hint(
            'Non-integer month',
            recommendation,
            'An integer is easier to sort and fits better into multilingual environment.',
            'warn_about_month_field')
    else:
        return None


def title_as_key(key: str, entry: typing.Dict[str, typing.Any], bib_file: BibFile) -> typing.Optional[Hint]:
    clean_title = TranscriptionFunctions.lower(TranscriptionFunctions.drop_specials(entry['title']))
    if key.startswith(clean_title):
        line_number = bib_file.line_of(key)
        return Hint('title-based key',
                    f'Change the key of "{key}" to (at least starts with) "{clean_title}" in line {line_number}.',
                    'Most of the editor will offer suggestions and prefill the keys;'
                    ' furthermore these keys are easier to read during writting.',
                    'title_as_key')


def western_lexical_name_order(line: LastFieldLine, context: Context, bibfile: BibFile):
    if line.name == 'author':
        return Hint('expected name format',
                    'It is mandatory to use the following version of so-called "western lexical name order". '
                    'A name consists of 3 parts separated with comas (,):'
                    ' (1) the family name, (2) the first given name following with additional middle or third names,'
                    ' finally (3) the English equivalent of any academic and professional titles, if mentioned. '
                    'For example: Smith, Jhon William Oscar, MD PhD. '
                    'Do not use any abbreviation and do not put a period (.) after the titles.',
                    'This format support alphabetic ordering and made it easier to construct '
                    'the appropriate addressing in the case of personal communication and mentioning.',
                    'expected_name_format')


def field_definitions(key: str, entry: typing.Dict[str, typing.Any], bib_file: BibFile) -> typing.Optional[Hint]:
    entry_type = entry[ENTRYTYPE_PROPERTY_NAME]
    definition = '\n'.join(map(str, fields_per_types[entry_type]))
    return Hint(
        f'definition for {entry_type}',
        f'Please verify that the entry satisfies the followings.\n{definition}',
        'We use the types specified at https://en.wikipedia.org/wiki/BibTeX#Entry_types',
        'field_definitions'
    )