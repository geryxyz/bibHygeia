import functools
import re

import typing

latex_diacritics = {
    '\\`': '',
    '\\\'': '',
    '\\^': '',
    '\\"': '',
    '\\H': '',
    '\\~': '',
    '\\c': '',
    '\\k': '',
    '\\l': '',
    '\\=': '',
    '\\b': '',
    '\\.': '',
    '\\d': '',
    '\\r': '',
    '\\u': '',
    '\\v': '',
    '\\t': '',
    '\\o': 'o',
    '\\i': 'i'
}

hungarian_diacritics = {
    'á': 'a',
    'é': 'e',
    'í': 'i',
    'ó': 'o',
    'ö': 'o',
    'ő': 'o',
    'ú': 'u',
    'ü': 'u',
    'ű': 'u'
}

OMISSION_CHAR = '-'
AND = ' and '


def replace_all(original: str, replacements: typing.Dict[str, str]) -> str:
    result = original
    for key, value in replacements.items():
        result = result.replace(key, value)
    return result


def drop_special_chars(value: str):
    curly_dropped = value.replace('{', '').replace('}', '')
    diacritic_dropped = replace_all(replace_all(curly_dropped, latex_diacritics), hungarian_diacritics)
    other_special_chars = re.sub(r'[^a-zA-Z0-9]+', OMISSION_CHAR, diacritic_dropped)
    return other_special_chars.strip(OMISSION_CHAR)


def in_in(what, containers):
    for container in containers:
        if what in container:
            return True
    return False


def level_of(open: str, close: str, text: str):
    if len(open) > 1 or len(close) > 1:
        raise ValueError('only single char allowed')
    current_level = 0
    levels = []
    for char in text:
        if char == open:
            current_level += 1
            levels.append((current_level - 1, current_level))
        elif char == close:
            current_level -= 1
            levels.append((current_level + 1, current_level))
        else:
            levels.append((current_level,))
    return levels


def enclose(open: str, close: str, text: str):
    levels = level_of(open, close, text)
    if (0, 1) == levels[0] and (1, 0) == levels[-1] and not in_in(0, levels[1:-1]):
        return text
    else:
        return open + text + close


def unloose(open: str, close: str, text: str):
    levels = level_of(open, close, text)
    if (0, 1) == levels[0] and (1, 0) == levels[-1] and not in_in(0, levels[1:-1]):
        return text[1:-1]
    else:
        return text


global_index = 0


def index_if(x, check) -> str:
    global global_index
    global_index += 1
    if check(x):
        return 'no.' + str(global_index)
    else:
        return x


def first_author_of(x: str):
    if x and AND in x:
        return x.split(AND)[0]
    else:
        return x


class TranscriptionFunction:
    def __init__(self, action, name, description):
        self.action = action
        self.name = name
        self.description = description

    def __call__(self, *args, **kwargs):
        return self.action(args[0])


class TranscriptionFunctions(object):
    nop = TranscriptionFunction(
        lambda x: x,
        'no-operation', 'It does nothing.')

    lower = TranscriptionFunction(
        lambda x: x.lower(),
        'lower case', 'It converts the value to its lower case equivalent.')

    upper = TranscriptionFunction(
        lambda x: x.upper(),
        'upper case', 'It converts the value to its upper case equivalent.')

    drop_specials = TranscriptionFunction(
        drop_special_chars,
        'remove non-alphanumeric chars', 'It removes or substitute non-alphanumeric characters with underscore (_).')

    pre_formatted = TranscriptionFunction(
        lambda x: enclose('{', '}', x),
        'mark as pre-formatted', 'It marks all values (if not already marked) as pre-formatted casing,'
                                 ' enclosing it inside curly braces ({ }).')

    post_formatted = TranscriptionFunction(
        lambda x: unloose('{', '}', x),
        'mark as post-formatted', 'It marks all values (if not already marked) as post-formatted casing,'
                                  ' removing any top level curly braces ({ }).')

    abbr = TranscriptionFunction(
        lambda x: re.sub(r'[^A-Z]', '', x),
        'abbreviation', 'It removes all characters expect upper case letters.')

    index_if_empty = TranscriptionFunction(
        lambda x: index_if(x, lambda y: y == ''),
        'index if empty', 'It resolves the pattern as an increasing index if the value is empty.')

    first_author = TranscriptionFunction(
        first_author_of,
        'first author only', 'It returns the first name in the list if the list contains the "and" keyword.')


@functools.lru_cache()
def parts_of(value):
    return [TranscriptionFunctions.drop_specials(part.lower()) for part in re.split(r'\W', value) if part != '']


@functools.lru_cache()
def jaccard_similarity(value, other_value):
    parts = set(parts_of(value))
    other_parts = set(parts_of(other_value))
    intersection = parts.intersection(other_parts)
    return len(intersection) / (len(parts) + len(other_parts) - len(intersection))


SHORT_MSG_LENGTH = 2000


def shorten_start(text: str) -> str:
    if len(text) > SHORT_MSG_LENGTH:
        return '...' + text[len(text) - SHORT_MSG_LENGTH:]
    else:
        return text


def shorten_end(text: str) -> str:
    if len(text) > SHORT_MSG_LENGTH:
        return text[:SHORT_MSG_LENGTH] + '...'
    else:
        return text


def html_line_breaks(text: str) -> str:
    return text.replace('\n', '<br />')
