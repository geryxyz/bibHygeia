import glob2
import os
import sys
import re
import bibtexparser
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
        id = entry['ID']
        title = entry['title']
        title_parts = [part for part in re.split(r'\W', title) if part != '']
        print("{:.2%}".format(i / entry_count))
        if merged.entries:
            for other_entry in merged.entries:
                other_title = other_entry['title']
                other_title_parts = [part for part in re.split(r'\W', other_title) if part != '']
                common_parts = [part for part in title_parts if part in other_title_parts]
                jaccard_title = len(common_parts) / (len(title_parts) + len(other_title_parts) - len(common_parts))
                if jaccard_title < .6:
                    merged.entries.append(entry)
                # else:
                #     print("already added")
                #     print("  merged:  {}".format(other_title))
                #     print("  current: {}".format(title))
        else:
            merged.entries.append(entry)

pdb.set_trace()