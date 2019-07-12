import argparse
import logging
import os
import re
import sys
import bibtexparser
import copy
import pdb

import original
from upgrade import Upgrade, Replacement, Regenerated
import util

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
logger.addHandler(handler)


def drop_special_chars(value: str):
    curly_dropped = value.replace('{', '').replace('}', '')
    diacritic_dropped = curly_dropped\
        .replace('\\`', '')\
        .replace('\\\'', '')\
        .replace('\\^', '')\
        .replace('\\"', '')\
        .replace('\\H', '')\
        .replace('\\~', '')\
        .replace('\\c', '')\
        .replace('\\k', '')\
        .replace('\\l', '')\
        .replace('\\=', '')\
        .replace('\\b', '')\
        .replace('\\.', '')\
        .replace('\\d', '')\
        .replace('\\r', '')\
        .replace('\\u', '')\
        .replace('\\v', '')\
        .replace('\\t', '')\
        .replace('\\o', 'o')
    other_special_chars = re.sub(r'\W+', '_', diacritic_dropped)
    return other_special_chars.strip('_')


class TranscriptionFunction:
    def __init__(self, action, name, description):
        self.action = action
        self.name = name
        self.description = description

    def apply(self, value):
        return self.action(value)


def enclose(open: str, close: str, text: str):
    levels = util.level_of(open, close, text)
    if (0, 1) == levels[0] and (1, 0) == levels[-1] and not util.in_in(0, levels[1:-1]):
        return text
    else:
        return open + text + close


def unloose(open: str, close: str, text: str):
    levels = util.level_of(open, close, text)
    if (0, 1) == levels[0] and (1, 0) == levels[-1] and not util.in_in(0, levels[1:-1]):
        return text[1:-1]
    else:
        return text


transcription_functions = {
    'nop': TranscriptionFunction(
        lambda x: x,
        'no-operation', 'It does nothing.'),
    'lower': TranscriptionFunction(
        lambda x: x.lower(),
        'lower case', 'It converts the value to its lower case equivalent.'),
    'upper': TranscriptionFunction(
        lambda x: x.upper(),
        'upper case', 'It converts the value to its upper case equivalent.'),
    'drop_specials': TranscriptionFunction(
        drop_special_chars,
        'remove non-alphanumeric chars', 'It removes or substitute non-alphanumeric characters with underscore (_).'),
    'pre_formatted': TranscriptionFunction(
        lambda x: enclose('{', '}', x),
        'mark as pre-formatted', 'It marks all values (if not already marked) as pre-formatted casing,'
                                 ' enclosing it inside curly braces ({ }).'),
    'post_formatted': TranscriptionFunction(
        lambda x: unloose('{', '}', x),
        'mark as post-formatted', 'It marks all values (if not already marked) as post-formatted casing,'
                                  ' removing any top level curly braces ({ }).')
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="unify.py",
        description='bibHygeia Unify: Generate unified values for target property based on other properties.',
        epilog='Unify is part of bibHygeia toolkit.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='input file to unify')
    parser.add_argument('-t', '--target', type=str, required=False, default='ID',
                        help='name of the target property. Use "ID" for id.')
    parser.add_argument('-p', '--pattern', type=str, required=False, default='@{ID:drop_specials}',
                        help='pattern to change the property value. Use "@{property}" for values of other properties')
    parser.add_argument('--remove_unresolved_refs', type=util.bool_switch, default=True, required=False,
                        help='if true, all unresolved property reference will be removed from new value')
    parser.add_argument('--ignore_unresolved_refs', type=util.bool_switch, default=False, required=False,
                        help='if true, all unresolved property reference will be ignored')
    parser.add_argument('--list_functions', action='store_true',
                        help='list all the available transcription functions')
    parser.add_argument('--log', type=str, default='INFO', required=False,
                        help='level of log messages to display')

    args = parser.parse_args()

    logger.setLevel(logging.getLevelName(args.log))

    if args.list_functions:
        for function_id, function in transcription_functions.items():
            logger.info('ID: {} name: {}\n{}'.format(function_id, function.name, function.description))
        sys.exit()

    if args.ignore_unresolved_refs and args.remove_unresolved_refs:
        logger.error("can not remove and ignore unresolved references at the same time")
        sys.exit()
    if args.remove_unresolved_refs:
        logger.warning("unresolved references will be removed")
    if args.ignore_unresolved_refs:
        logger.warning("unresolved references will be ignored")

    if original.has_original(args.input):
        logger.error("original file present, remove them")
        sys.exit()
    original_file = original.save_current_state(args.input)

    parser = bibtexparser.bparser.BibTexParser(common_strings=True)

    with open(original_file, 'r', encoding="utf8") as bibtex_file:
        old_db = bibtexparser.load(bibtex_file, parser)

    side_effect = Upgrade()

    new_ids = set()
    logger.info('regenerating "{}" based on "{}"'.format(args.target, args.pattern))
    new_db = bibtexparser.bibdatabase.BibDatabase()
    for old_entry in old_db.entries:
        logger.debug('processing entry "{}"'.format(old_entry['ID']))
        new_target_value: str = args.pattern

        property_pattern = r'@[{](?P<property>\w+)(:(?P<functions>[\w,]+))?[}]'
        replacement_map = {}

        for match in re.finditer(property_pattern, new_target_value):
            property_name = match.group('property')
            functions = match.group('functions')
            functions = [func for func in functions.split(',') if func != '']
            function_processed_value = old_entry.get(property_name, '')
            for function_name in functions:
                function = transcription_functions.get(function_name, transcription_functions['nop'])
                new_function_processed_value = function.apply(function_processed_value)
                if function_name not in transcription_functions:
                    logger.warning(
                        'function "{}" is unknown, will be substituted with "no-operation"'.format(function_name))
                else:
                    logger.debug('applying "{}({})" = "{}"'.format(
                        function_name,
                        function_processed_value,
                        new_function_processed_value))
                function_processed_value = new_function_processed_value
            replacement_map[match.group(0)] = function_processed_value
        for replacement_pattern, replacement_value in replacement_map.items():
            if replacement_pattern in new_target_value:
                logger.debug('resolving "{}"'.format(replacement_pattern))
                new_target_value = new_target_value.replace(replacement_pattern, replacement_value)
        new_entry = copy.deepcopy(old_entry)
        if re.search(r'@\{[^{}]+\}', new_target_value):
            if not args.ignore_unresolved_refs:
                if args.remove_unresolved_refs:
                    new_target_value = re.sub(r'@\{[^{}]+\}', '', new_target_value)
                else:
                    logger.error('there are unresolved references in "{}" while processing "{}"'.format(new_target_value, old_entry['ID']))
                    sys.exit()
        new_entry[args.target] = new_target_value
        new_db.entries.append(new_entry)
        if args.target == 'ID':
            if new_target_value not in new_ids:
                new_ids.add(new_target_value)
                if old_entry[args.target] != new_entry[args.target]:
                    side_effect.add_if_not_present(Replacement(
                        old_entry[args.target], new_entry[args.target],
                        reason=Regenerated(args.pattern, old_entry, new_entry)))
            else:
                logger.error('conflicting id "{}" detected while processing "{}"'.format(new_target_value, old_entry['ID']))
                sys.exit()
        logger.debug('"{}" value of "{}" was replaced with "{}"'.format(old_entry[args.target], args.target, new_target_value))

    logger.info('saving unified database')
    with open(args.input, 'w', encoding='utf8') as output_file:
        bibtexparser.dump(new_db, output_file)
    logger.info('{} entries was unified'.format(len(new_db.entries)))

    side_effect.save('side_effect.unify')
    logger.info('side-effect file created for future upgrading your source files')
