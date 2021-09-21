from unittest import TestCase

from owl.core.decorators import biber_file_line_checker, hinted
from owl.hinting.hint import western_lexical_name_order
from owl.util.bibtex_line_type import *


@biber_file_line_checker(line_type=EntryStartLine)
def correct_indentation_for_start(line: Line, context: Context, test: TestCase):
    test.assertEqual(line.pre_line, '', 'no whitespace allowed before entry specification')


@biber_file_line_checker(line_type=(FieldLine, LastFieldLine))
def correct_indentation_for_field(line: Line, context: Context, test: TestCase):
    test.assertEqual(line.pre_line, ' ' * 4, 'exactly 4 spaces allowed before field specification')


@biber_file_line_checker(line_type=EntryEndLine)
def correct_indentation_for_end(line: Line, context: Context, test: TestCase):
    test.assertEqual(line.pre_line, '', 'no whitespace allowed before closing entry specification')


@biber_file_line_checker(line_type=None)
def no_trailing_spaces(line: Line, context: Context, test: TestCase):
    if type(line) == EmptyLine or type(line) == UnrecognizedLine:
        test.assertIs(line.post_line, None, 'no whitespace allowed after bibtex lines')
    else:
        test.assertEqual(line.post_line, '\n', 'no whitespace allowed after bibtex lines')


@biber_file_line_checker(line_type=EmptyLine)
def no_whitespace_only_lines(line: EmptyLine, context: Context, test: TestCase):
    test.assertEqual(line.raw, '\n', 'empty line should be strictly empty and cannot contains whitespaces')


@biber_file_line_checker(line_type=EmptyLine)
def no_empty_line_inside_entries(line: Line, context: Context, test: TestCase):
    test.assertTrue(context.is_last(line), 'empty line only allowed at the and of context (before entry definitions)')


@biber_file_line_checker(line_type=ClosingFieldLine)
def closing_entry_in_individual_line(line: Line, context: Context, test: TestCase):
    test.fail('entries should be closed in individual lines')


@biber_file_line_checker(line_type=(FieldLine, LastFieldLine))
def single_space_around_equal_sing(line: typing.Union[FieldLine, LastFieldLine], context: Context, test: TestCase):
    test.assertEqual(line.post_name, ' ', 'there should be one and only one space after the name of the field')
    test.assertEqual(line.pre_value, ' ', 'there should be one and only one space before the value of the field')


@biber_file_line_checker(line_type=(FieldLine, LastFieldLine))
def quotemarks_around_values(line: LastFieldLine, context: Context, test: TestCase):
    test.assertNotRegex(line.value, r'^[{].+[}]$', 'do not use {} to enclose string values, use "-mark instead')


@biber_file_line_checker(line_type=(FieldLine, LastFieldLine))
def no_quotemarks_or_braces_around_numerical_value(line: LastFieldLine, context: Context, test: TestCase):
    test.assertNotRegex(line.value, r'^[{"](0|[^0][0-9]+)[}"]$', 'do not enclose number-only values neither with "-mark or with {}')


@biber_file_line_checker(line_type=(FieldLine, LastFieldLine))
def no_abbreviations_in_names(line: LastFieldLine, context: Context, test: TestCase):
    if line.name == 'author':
        for word in [w for w in re.sub('[{}"]', '', line.value).split(' ') if w]:
            test.assertGreater(len(word), 1, f'do not use abbreviations in names, the word "{word}" is only 1 char long')
            test.assertNotIn('.', word, f'the word "{word}" contains a period (.), using abbreviations in names are not allowed')


@hinted(hinter=western_lexical_name_order)
@biber_file_line_checker(line_type=(FieldLine, LastFieldLine))
def name_format(line: LastFieldLine, context: Context, test: TestCase):
    if line.name != 'author':
        return
    names = [n.strip() for n in re.sub('[{}"]', '', line.value).split('and')]
    for name in names:
        test.assertTrue(bool(name), f'the name "{name}" is empty, empty names not allowed')
        parts = name.split(',')
        test.assertLessEqual(
            len(parts), 3,
            f'names should consist at most 3 parts separated with a coma (,), "{name}" has more')
