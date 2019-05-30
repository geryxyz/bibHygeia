import glob2
import os
import sys
import re
import bibtexparser
import functools
import pdb

root_dir = sys.argv[1]
exclude_pattern = None
if len(sys.argv) > 2:
    exclude_pattern = sys.argv[2]
bibtex_files = glob2.glob(os.path.join(root_dir, '**', '*.bib'))
dbs = {}
for current_file in bibtex_files:
    if exclude_pattern is not None and re.search(exclude_pattern, current_file):
        continue
    print("processing {}".format(current_file))
    with open(current_file, 'r', encoding="utf8") as bibtex_file:
        dbs[current_file] = bibtexparser.load(bibtex_file)

merged = bibtexparser.bibdatabase.BibDatabase()
for file, db in dbs.items():
    print(file)
    entry_count = len(db.entries)
    for i, entry in enumerate(db.entries):
        print("{:.2%}".format(i / entry_count))
        merged.entries.append(entry)


@functools.lru_cache()
def parts_of(title):
    return [part for part in re.split(r'\W', title) if part != '']


@functools.lru_cache()
def jaccard_of(title, other_title):
    title_parts = parts_of(title)
    other_title_parts = parts_of(other_title)
    common_parts = [part for part in title_parts if part in other_title_parts]
    return len(common_parts) / (len(title_parts) + len(other_title_parts) - len(common_parts))


deduped = bibtexparser.bibdatabase.BibDatabase()
entry_count = len(merged.entries)
for i, entry in enumerate(merged.entries):
    id = entry['ID']
    title = entry['title']
    print("{:.2%} ({})".format(i / entry_count, len(deduped.entries)))
    if entry in deduped.entries:
        continue
    if deduped.entries:
        jaccard_title = max([jaccard_of(title, other_entry['title']) for other_entry in deduped.entries])
        if jaccard_title < .6:
            deduped.entries.append(entry)
    else:
        deduped.entries.append(entry)

with open('merged.bib', 'w', encoding='utf8') as deduped_file:
    bibtexparser.dump(deduped, deduped_file)