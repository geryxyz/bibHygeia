import re
from enum import Enum

import typing


def pre(name: str):
    return rf'(?P<pre_{name}>\s*)'


def post(name: str):
    return rf'(?P<post_{name}>\s*)'


def part(name: str):
    return rf'(?P<{name}>[^\s]+)'


class Line(object):
    def __init__(self, raw: str):
        self.raw: str = raw
        self.pre_line: typing.Optional[str] = None
        self.post_line: typing.Optional[str] = None


class EmptyLine(Line):
    def __init__(self, raw: str, match: re.Match):
        super().__init__(raw)


class EntryStartLine(Line):
    def __init__(self, raw: str, match: re.Match):
        super().__init__(raw)
        self.pre_line: str = match.group('pre_line')
        self.type: str = match.group('type')
        self.post_type: str = match.group('post_type')
        self.pre_key: str = match.group('pre_key')
        self.key: str = match.group('key')
        self.post_key: str = match.group('post_key')
        self.post_line: str = match.group('post_line')


class LastFieldLine(Line):
    def __init__(self, raw: str, match: re.Match):
        super().__init__(raw)
        self.pre_line: str = match.group('pre_line')
        self.name: str = match.group('name')
        self.post_name: str = match.group('post_name')
        self.pre_value: str = match.group('pre_value')
        self.value: str = match.group('value')
        self.post_line: str = match.group('post_line')


class FieldLine(LastFieldLine):
    def __init__(self, raw: str, match: re.Match):
        super().__init__(raw, match)
        self.post_value: str = match.group('post_value')


class ClosingFieldLine(FieldLine):
    pass


class EntryEndLine(Line):
    def __init__(self, raw: str, match: re.Match):
        super().__init__(raw)
        self.pre_line: str = match.group('pre_line')
        self.post_line: str = match.group('post_line')


class UnrecognizedLine(Line):
    def __init__(self, raw: str):
        super().__init__(raw)


type_regexes = {
    EmptyLine: r'^\s*$',
    EntryStartLine: rf'^{pre("line")}@{part("type")}{post("type")}[{{]{pre("key")}{part("key")}{post("key")},{post("line")}$',
    FieldLine: rf'^{pre("line")}{part("name")}{post("name")}={pre("value")}(?P<value>.+){post("value")},{post("line")}$',
    LastFieldLine: rf'^{pre("line")}{part("name")}{post("name")}={pre("value")}(?P<value>.+){post("line")}$',
    ClosingFieldLine: rf'^{pre("line")}{part("name")}{post("name")}={pre("value")}(?P<value>.+){post("value")}[}}]{post("line")}$',
    EntryEndLine: rf'^{pre("line")}[}}]{post("line")}$'
}


class Context(object):
    def __init__(self):
        self.lines: typing.List[Line] = []

    def index_of(self, line: Line) -> typing.Optional[int]:
        return self.lines.index(line)

    def is_last(self, line: Line) -> bool:
        return self.lines and self.lines[-1] == line

    def is_first(self, line: Line) -> bool:
        return self.lines and self.lines[0] == line
