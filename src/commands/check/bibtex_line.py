import re
import typing


def pre(name: str):
    return rf'(?P<pre_{name}>\s*)'


def post(name: str):
    return rf'(?P<post_{name}>\s*)'


def part(name: str):
    return rf'(?P<{name}>[^\s]+)'


class Line(object):
    def __init__(self, raw: str, line_number: int):
        self.raw: str = raw
        self.pre_line: typing.Optional[str] = None
        self.post_line: typing.Optional[str] = None
        self.line_number: int = line_number


class EmptyLine(Line):
    def __init__(self, raw: str, match: re.Match, line_number: int):
        super().__init__(raw, line_number)


class CommentLine(Line):
    def __init__(self, raw: str, match: re.Match, line_number: int):
        super().__init__(raw, line_number)
        self.pre_line: str = match.group('pre_line')
        self.comment: str = match.group('comment')
        self.line_number: int = line_number


class EntryStartLine(Line):
    def __init__(self, raw: str, match: re.Match, line_number: int):
        super().__init__(raw, line_number)
        self.pre_line: str = match.group('pre_line')
        self.type: str = match.group('type')
        self.post_type: str = match.group('post_type')
        self.pre_key: str = match.group('pre_key')
        self.key: str = match.group('key')
        self.post_key: str = match.group('post_key')
        self.post_line: str = match.group('post_line')


class FieldLine(Line):
    def __init__(self, raw: str, match: re.Match, line_number: int):
        super().__init__(raw, line_number)
        self.pre_line: str = match.group('pre_line')
        self.name: str = match.group('name')
        self.post_name: str = match.group('post_name')
        self.pre_value: str = match.group('pre_value')
        self.value: str = match.group('value')
        self.post_value: str = match.group('post_value')
        self.post_line: str = match.group('post_line')


class LastFieldLine(Line):
    def __init__(self, raw: str, match: re.Match, line_number: int):
        super().__init__(raw, line_number)
        self.pre_line: str = match.group('pre_line')
        self.name: str = match.group('name')
        self.post_name: str = match.group('post_name')
        self.pre_value: str = match.group('pre_value')
        self.value: str = match.group('value')
        self.post_line: str = match.group('post_line')


class ClosingFieldLine(Line):
    def __init__(self, raw: str, match: re.Match, line_number: int):
        super().__init__(raw, line_number)
        self.pre_line: str = match.group('pre_line')
        self.name: str = match.group('name')
        self.post_name: str = match.group('post_name')
        self.pre_value: str = match.group('pre_value')
        self.value: str = match.group('value')
        self.post_value: str = match.group('post_value')
        self.post_line: str = match.group('post_line')


class EntryEndLine(Line):
    def __init__(self, raw: str, match: re.Match, line_number: int):
        super().__init__(raw, line_number)
        self.pre_line: str = match.group('pre_line')
        self.post_line: str = match.group('post_line')


class UnrecognizedLine(Line):
    def __init__(self, raw: str, line_number: int):
        super().__init__(raw, line_number)


type_regexes = {
    EmptyLine: r'^\s*$',
    CommentLine: rf'^{pre("line")}%(?P<comment>.*)$',
    EntryStartLine: rf'^{pre("line")}@{part("type")}{post("type")}[{{]{pre("key")}{part("key")}{post("key")},{post("line")}$',
    FieldLine: rf'^{pre("line")}{part("name")}{post("name")}={pre("value")}(?P<value>.+){post("value")},{post("line")}$',
    LastFieldLine: rf'^{pre("line")}{part("name")}{post("name")}={pre("value")}(?P<value>.+){post("line")}$',
    ClosingFieldLine: rf'^{pre("line")}{part("name")}{post("name")}={pre("value")}(?P<value>.+){post("value")}[}}]{post("line")}$',
    EntryEndLine: rf'^{pre("line")}[}}](?P<post_line>.*)$'  # ^(?P<pre_line>\s*)[}](?P<post_line>.*)$
}
