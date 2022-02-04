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
        self.context: typing.Optional[Context] = None


class EmptyLine(Line):
    def __init__(self, raw: str, match: re.Match, line_number: int):
        super().__init__(raw, line_number)


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


# Regexes:
# EmptyLine:        ^\s*$
# EntryStartLine:   ^(?P<pre_line>\s*)@(?P<type>[^\s]+)(?P<post_type>\s*)[{](?P<pre_key>\s*)(?P<key>[^\s]+)(?P<post_key>\s*),(?P<post_line>\s*)$
# FieldLine:        ^(?P<pre_line>\s*)(?P<name>[^\s]+)(?P<post_name>\s*)=(?P<pre_value>\s*)(?P<value>.+)(?P<post_value>\s*),(?P<post_line>\s*)$
# LastFieldLine:    ^(?P<pre_line>\s*)(?P<name>[^\s]+)(?P<post_name>\s*)=(?P<pre_value>\s*)(?P<value>.+)(?P<post_line>\s*)$
# ClosingFieldLine: ^(?P<pre_line>\s*)(?P<name>[^\s]+)(?P<post_name>\s*)=(?P<pre_value>\s*)(?P<value>.+)(?P<post_value>\s*)[}](?P<post_line>\s*)$
# EntryEndLine:     ^(?P<pre_line>\s*)[}](?P<post_line>.*)$

type_regexes = {
    EmptyLine: r'^\s*$',
    EntryStartLine: rf'^{pre("line")}@{part("type")}{post("type")}[{{]{pre("key")}{part("key")}{post("key")},{post("line")}$',
    FieldLine: rf'^{pre("line")}{part("name")}{post("name")}={pre("value")}(?P<value>.+){post("value")},{post("line")}$',
    LastFieldLine: rf'^{pre("line")}{part("name")}{post("name")}={pre("value")}(?P<value>.+){post("line")}$',
    ClosingFieldLine: rf'^{pre("line")}{part("name")}{post("name")}={pre("value")}(?P<value>.+){post("value")}[}}]{post("line")}$',
    EntryEndLine: rf'^{pre("line")}[}}](?P<post_line>.*)$'
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

    def __str__(self):
        return '\n'.join(line.raw for line in self.lines)
