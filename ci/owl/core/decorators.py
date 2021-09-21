import re
import typing
import unittest
import bibtexparser

from owl.util.bibtex_line_type import Line, Context
from owl.util.BibFile import BibFile
from owl.util.reflection import get_descent_classes

biber_log_checkers: typing.List[typing.Callable[[str, unittest.TestCase], None]] = []


def biber_log_checker(func: typing.Callable[[str, unittest.TestCase], None]):
    biber_log_checkers.append(func)
    return func


biber_file_checkers: typing.List[typing.Callable[[Line, Context, unittest.TestCase], None]] = []
LINE_TYPE_ATTR_NAME = 'line_type'


def biber_file_line_checker(line_type: typing.Optional = None) -> typing.Callable:
    if line_type is not None:
        if isinstance(line_type, list) or isinstance(line_type, tuple):
            for _type in line_type:
                if _type not in get_descent_classes(Line):
                    raise TypeError('line_type filter expect to be a set of subclasses (not an instance) of Line')
        elif line_type not in get_descent_classes(Line):
            raise TypeError('line_type filter expect to be a subclass (not an instance) of Line')

    def _inner(func: typing.Callable[[Line, Context, unittest.TestCase], None]):
        func.line_type = line_type
        biber_file_checkers.append(func)
        return func
    return _inner


biber_entry_checkers: typing.List[typing.Callable[[str, typing.Dict[str, typing.Any], BibFile, unittest.TestCase], None]] = []


def biber_entry_checker(func: typing.Callable[[str, typing.Dict[str, typing.Any], BibFile, unittest.TestCase], None]):
    biber_entry_checkers.append(func)
    return func


HINTER_ATTR_NAME = 'hinters'
HINT_ATTR_NAME = 'hints'


def hinted(hinter: typing.Callable) -> typing.Callable:
    def _hinted(func: typing.Callable):
        if not hasattr(func, HINTER_ATTR_NAME):
            func.hinters = []
        func.hinters.append(hinter)
        return func
    return _hinted


def assign_hint_to(container, hint):
    if hasattr(container, '_subtest') and container._subtest is not None:
        context = container._subtest
    else:
        context = container
    if not hasattr(context, HINT_ATTR_NAME):
        setattr(context, HINT_ATTR_NAME, [])
    getattr(context, HINT_ATTR_NAME).append(hint)
