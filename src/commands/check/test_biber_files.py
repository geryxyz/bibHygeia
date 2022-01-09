import typing
import re
import pytest

from .bibtex_line import Line, EntryStartLine, EntryEndLine, LastFieldLine, FieldLine, EmptyLine, ClosingFieldLine
from .CheckCommand import input_biber_files


def input_lines(*line_type: typing.Type[Line]) -> typing.List[Line]:
    for bibfile in input_biber_files():
        for line in bibfile.preprocessed_lines:
            if len(line_type) == 0 or type(line) in line_type:
                yield line


@pytest.mark.parametrize("line", input_lines(EntryStartLine), ids=lambda line: "Line %d" % line.line_number)
def test_correct_indentation_for_start(line: EntryStartLine):
    assert line.pre_line == '', 'no whitespace allowed before entry specification'


@pytest.mark.parametrize("line", input_lines(FieldLine, LastFieldLine), ids=lambda line: "Line %d" % line.line_number)
def test_correct_indentation_for_field(line: typing.Union[FieldLine, LastFieldLine]):
    assert line.pre_line == ' ' * 4, 'exactly 4 spaces allowed before field specification'


@pytest.mark.parametrize("line", input_lines(EntryEndLine), ids=lambda line: "Line %d" % line.line_number)
def test_correct_indentation_for_end(line: EntryEndLine):
    assert line.pre_line == '', 'no whitespace allowed before closing entry specification'


@pytest.mark.parametrize("line", input_lines(EntryStartLine, FieldLine, LastFieldLine, ClosingFieldLine, EntryEndLine),
                         ids=lambda line: "Line %d" % line.line_number)
def test_no_trailing_spaces(line: typing.Union[EntryStartLine, FieldLine, LastFieldLine, ClosingFieldLine, EntryEndLine]):
    print("Debug post line:", "|", line.post_line, "|")
    assert line.post_line in ('\n', ''), \
        'no whitespace allowed after starting/closing entry specification or field specification'


@pytest.mark.parametrize("line", input_lines(EmptyLine), ids=lambda line: "Line %d" % line.line_number)
def test_no_whitespace_only_lines(line: EmptyLine):
    assert line.raw == '\n', 'empty line should be strictly empty and cannot contains whitespaces'


@pytest.mark.parametrize("line", input_lines(FieldLine, LastFieldLine), ids=lambda line: "Line %d" % line.line_number)
def test_single_space_around_equal_sing(line: typing.Union[FieldLine, LastFieldLine]):
    assert line.post_name == ' ', 'there should be one and only one space after the name of the field'
    assert line.pre_value == ' ', 'there should be one and only one space before the value of the field'


@pytest.mark.parametrize("line", input_lines(FieldLine, LastFieldLine), ids=lambda line: "Line %d" % line.line_number)
def test_quotemarks_around_values(line: typing.Union[FieldLine, LastFieldLine]):
    assert not re.match(r'^[{].+[}]$', line.value), 'do not use {} to enclose string values, use "-mark instead'


@pytest.mark.parametrize("line", input_lines(FieldLine, LastFieldLine), ids=lambda line: "Line %d" % line.line_number)
def test_no_quotemarks_or_braces_around_numerical_value(line: typing.Union[FieldLine, LastFieldLine]):
    assert not re.match(r'^[{"](0|[^0][0-9]+)[}"]$', line.value), \
        'do not enclose number-only values neither with "-mark or with {}'


@pytest.mark.parametrize("line", input_lines(FieldLine, LastFieldLine), ids=lambda line: "Line %d" % line.line_number)
def test_no_abbreviations_in_names(line: typing.Union[FieldLine, LastFieldLine]):
    if line.name != 'author':
        return

    words = [w for w in re.sub('[{}"]', '', line.value).split(' ') if w]
    for word in words:
        assert len(word) > 1, f'do not use abbreviations in names, the word "{word}" is only 1 char long'
        assert '.' not in word, \
            f'the word "{word}" contains a period (.), using abbreviations in names are not allowed'


@pytest.mark.parametrize("line", input_lines(FieldLine, LastFieldLine), ids=lambda line: "Line %d" % line.line_number)
def test_name_format(line: typing.Union[FieldLine, LastFieldLine]):
    if line.name != 'author':
        return

    names = [n.strip() for n in re.sub('[{}"]', '', line.value).split('and')]
    for name in names:
        assert bool(name), f'the name "{name}" is empty, empty names not allowed'
        parts = name.split(',')
        assert len(parts) <= 3, f'names should consist at most 3 parts separated with a coma (,), "{name}" has more'
