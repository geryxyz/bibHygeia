import argparse
import copy
import logging
import re
import sys

import bibtexparser

import original
from upgrade import Upgrade

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
logger.addHandler(handler)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="set.py",
        description='bibHygeia Set: re-set values for target property to a fixed value.',
        epilog='Set is part of bibHygeia toolkit.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', type=str, required=True,
                        help='input file to unify')
    parser.add_argument('-t', '--target', type=str, required=False, default='ENTRYTYPE',
                        help='name of the target property. Use "ENTRYTYPE" for type.')
    parser.add_argument('-s', '--subject', type=str, required=False, default='ENTRYTYPE',
                        help='name of the subject property. Use "ENTRYTYPE" for type.')
    parser.add_argument('-p', '--pattern', type=str, required=False, default='electronic',
                        help='regex pattern to match the subject property value.')
    parser.add_argument('-v', '--value', type=str, required=False, default='misc',
                        help='new value of the target property.')
    parser.add_argument('--log', type=str, default='INFO', required=False,
                        help='level of log messages to display')

    args = parser.parse_args()

    logger.setLevel(logging.getLevelName(args.log))

    if original.has_original(args.input):
        logger.error("original file present, remove them")
        sys.exit()
    original_file = original.save_current_state(args.input)

    parser = bibtexparser.bparser.BibTexParser(common_strings=True, ignore_nonstandard_types=False)

    with open(original_file, 'r', encoding="utf8") as bibtex_file:
        old_db = bibtexparser.load(bibtex_file, parser)

    side_effect = Upgrade()

    logger.info('re-setting "{}" to "{}" if {} match to {}'.format(args.target, args.value, args.subject, args.pattern))
    new_db = bibtexparser.bibdatabase.BibDatabase()
    count = 0
    for old_entry in old_db.entries:
        logger.debug('processing entry "{}"'.format(old_entry['ID']))
        new_entry = copy.deepcopy(old_entry)
        if args.subject in old_entry and re.search(args.pattern, old_entry[args.subject]):
            logger.debug('{} = {} ~ {}'.format(args.subject, old_entry[args.subject], args.pattern))
            new_entry[args.target] = args.value
            count += 1
            logger.debug('{} = {} --> {}'.format(args.target, old_entry[args.target], new_entry[args.target]))
        new_db.entries.append(new_entry)

    logger.info('saving new database')
    with open(args.input, 'w', encoding='utf8') as output_file:
        bibtexparser.dump(new_db, output_file)
    logger.info('{} entries was saved, {} ({:.2%}) was changed'.format(
        len(new_db.entries), count, count / len(new_db.entries)))

    side_effect.save('side_effect.set')
    logger.info('side-effect file created for future upgrading your source files')
