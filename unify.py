import argparse
import logging
import os
import re
import sys
import bibtexparser
import copy

import original

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
logger.addHandler(handler)

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
    parser.add_argument('-p', '--pattern', type=str, required=False, default='${ID}',
                        help='pattern to change the property value. Use "${property}" for values of other properties')
    parser.add_argument('--remove_special_chars', type=bool, default=True, required=False,
                        help='if true, all special chars (\\W) will be removed from substituted properties value')
    parser.add_argument('--log', type=str, default='INFO', required=False,
                        help='level of log messages to display')

    args = parser.parse_args()

    logger.setLevel(logging.getLevelName(args.log))

    if original.has_original(args.input):
        logger.error("original file present, remove them")
        sys.exit()
    original_file = original.save_current_state(args.input)

    parser = bibtexparser.bparser.BibTexParser(common_strings=True)

    if args.remove_special_chars:
        logger.warning("special chars will be removed")

    with open(original_file, 'r', encoding="utf8") as bibtex_file:
        old_db = bibtexparser.load(bibtex_file, parser)

    new_db = bibtexparser.bibdatabase.BibDatabase()
    for old_entry in old_db.entries:
        logger.debug('processing entry "{}"'.format(old_entry['ID']))
        new_value: str = args.pattern
        for name, value in old_entry.items():
            var_pattern = '${{{}}}'.format(name)
            if var_pattern in new_value:
                logger.debug('resolving "{}"'.format(name))
                if args.remove_special_chars:
                    logger.debug('removing special chars')
                    new_value = new_value.replace(var_pattern, re.sub(r'\W+', r'_', value))
                else:
                    new_value = new_value.replace(var_pattern, value)
        new_entry = copy.deepcopy(old_entry)
        new_entry[args.target] = new_value
        new_db.entries.append(new_entry)
        logger.debug('"{}" value of "{}" was replaced with "{}"'.format(old_entry[args.target], args.target, new_value))

    logger.info('saving unified database')
    with open(args.input, 'w', encoding='utf8') as output_file:
        bibtexparser.dump(new_db, output_file)
