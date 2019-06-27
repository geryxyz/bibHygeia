import glob2
import os
import sys
import re
import bibtexparser
import functools
import argparse
import logging
from upgrade import Upgrade, Replacement, Similar
import copy

import pdb


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="dedup.py",
        description='bibHygeia DeDup: Filtering duplicated entries based on Jaccard similarity by words.',
        epilog='DeDup is part of bibHygeia toolkit.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input_folder', type=str, required=True,
                        help='input folder to searching *.bib files recursively')
    parser.add_argument('-o', '--output_file', type=str, default='merged.bib', required=False,
                        help='input folder to searching *.bib files recursively')
    parser.add_argument('-e', '--exclude_pattern', type=str, default=None, required=False,
                        help='regular expression to exclude irrelevant sub-folder')
    parser.add_argument('-p', '--inspected_property', type=str, default='title', required=False,
                        help='the property of the entries to check for similarity')
    parser.add_argument('-l', '--similarity_limit', type=float, default=.6, required=False,
                        help='lower limit for similarity between entries which considered equal')
    parser.add_argument('--log', type=str, default='INFO', required=False,
                        help='level of log messages to display')

    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.getLevelName(args.log))
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
    logger.addHandler(handler)

    logger.info('searching Bibtex files in "{}", excluding "{}"'.format(args.input_folder, args.exclude_pattern))
    bibtex_files = glob2.glob(os.path.join(args.input_folder, '**', '*.bib'))

    parser = bibtexparser.bparser.BibTexParser(common_strings=True)

    dbs = {}
    for current_file in bibtex_files:
        if args.exclude_pattern is not None and re.search(args.exclude_pattern, current_file):
            continue
        logger.debug('loading {}'.format(current_file))
        with open(current_file, 'r', encoding="utf8") as bibtex_file:
            dbs[current_file] = bibtexparser.load(bibtex_file, parser)
    logger.info('{} files are loaded'.format(len(dbs)))

    logger.info('reading entries')
    already_added = set()
    merged = bibtexparser.bibdatabase.BibDatabase()
    for file, db in dbs.items():
        if db in already_added:
            continue
        already_added.add(db)
        logger.debug('reading entries form {}'.format(file))
        entry_count = len(db.entries)
        for i, entry in enumerate(db.entries):
            logger.debug("{:.2%}".format(i / entry_count))
            merged.entries.append(entry)
    logger.info('{} entries load from {} databases'.format(len(merged.entries), len(dbs)))


    @functools.lru_cache()
    def parts_of(value):
        return [part for part in re.split(r'\W', value) if part != '']


    @functools.lru_cache()
    def jaccard_of(value, other_value):
        parts = parts_of(value)
        other_parts = parts_of(other_value)
        common_parts = [part for part in parts if part in other_parts]
        return len(common_parts) / (len(parts) + len(other_parts) - len(common_parts))


    side_effect = Upgrade()
    logger.info(
        'filtering duplicated entries inspecting: similarity("{}") < {}'.format(args.inspected_property,
                                                                                args.similarity_limit))
    deduped = bibtexparser.bibdatabase.BibDatabase()
    entry_count = len(merged.entries)
    filtered_count = 0
    for i, entry in enumerate(merged.entries):
        value = entry[args.inspected_property]
        logger.debug("{:.2%} ({})".format(i / entry_count, len(deduped.entries)))
        if entry in deduped.entries:
            continue
        if deduped.entries:
            similarity, other_entry = max(
                [(jaccard_of(value, other_entry[args.inspected_property]), other_entry) for other_entry in deduped.entries],
                key=lambda e: e[0]
            )
            if similarity < args.similarity_limit:
                deduped.entries.append(entry)
            else:
                filtered_count += 1
                if other_entry['ID'] != entry['ID']:
                    replacement = Replacement(
                        other_entry['ID'], entry['ID'],
                        Similar(other_entry, entry, args.inspected_property, similarity))
                    side_effect.add_if_not_present(replacement)
        else:
            deduped.entries.append(entry)
    logger.info('{} ({:.2%}) entries are skipped'.format(filtered_count, filtered_count / entry_count))
    side_effect.save('side_effect')
    logger.info('side-effect file created for future upgrading your source files')

    logger.info('saving debuped database into "{}"'.format(args.output_file))
    with open(args.output_file, 'w', encoding='utf8') as deduped_file:
        bibtexparser.dump(deduped, deduped_file)
