import glob2
import os
import sys
import re
import bibtexparser
import functools
import argparse
import logging

import pdb

parser = argparse.ArgumentParser(
    prog="bibHygeia DeDup",
    description='Filtering duplicated entries based on Jaccard similarity by words.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-i', '--input_folder', type=str, required=True,
                    help='input folder to searching *.bib files recursively')
parser.add_argument('-o', '--output_file', type=str, required=True,
                    help='input folder to searching *.bib files recursively')
parser.add_argument('-e', '--exclude_pattern', type=str, default=None, required=False,
                    help='regular expression to exclude irrelevant sub-folder')

args = parser.parse_args()
print(args.accumulate(args.integers))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
logger.addHandler(handler)

root_dir = sys.argv[1]
exclude_pattern = None
output_path = 'merged.bib'
inspected_property = 'title'
similarity_limit = .6

if len(sys.argv) > 2:
    exclude_pattern = sys.argv[2]
logger.info('searching Bibtex files in "{}", excluding "{}"'.format(root_dir, exclude_pattern))
bibtex_files = glob2.glob(os.path.join(root_dir, '**', '*.bib'))
dbs = {}
for current_file in bibtex_files:
    if exclude_pattern is not None and re.search(exclude_pattern, current_file):
        continue
    logger.debug('loading {}'.format(current_file))
    with open(current_file, 'r', encoding="utf8") as bibtex_file:
        dbs[current_file] = bibtexparser.load(bibtex_file)
logger.info('{} files are loaded'.format(len(dbs)))

logger.info('reading entries')
merged = bibtexparser.bibdatabase.BibDatabase()
for file, db in dbs.items():
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


logger.info('filtering duplicated entries inspecting: similarity("{}") < {}'.format(inspected_property, similarity_limit))
deduped = bibtexparser.bibdatabase.BibDatabase()
entry_count = len(merged.entries)
filtered_count = 0
for i, entry in enumerate(merged.entries):
    id = entry['ID']
    value = entry[inspected_property]
    logger.debug("{:.2%} ({})".format(i / entry_count, len(deduped.entries)))
    if entry in deduped.entries:
        continue
    if deduped.entries:
        similarity = max([jaccard_of(value, other_entry[inspected_property]) for other_entry in deduped.entries])
        if similarity < similarity_limit:
            deduped.entries.append(entry)
        else:
            filtered_count += 1
    else:
        deduped.entries.append(entry)
logger.info('{} ({:.2%}) entries are skipped'.format(filtered_count, filtered_count / entry_count))

logger.info('saving debuped database into "{}"'.format(output_path))
with open(output_path, 'w', encoding='utf8') as deduped_file:
    bibtexparser.dump(deduped, deduped_file)