import re
import bibtexparser


class BibFile(object):
    def __init__(self, file_path: str):
        self.file_path = file_path
        parser = bibtexparser.bparser.BibTexParser(common_strings=True, ignore_nonstandard_types=False)
        with open(file_path, 'r', encoding='utf-8') as bibfile:
            self.bibliography: bibtexparser.bibdatabase.BibDatabase = bibtexparser.load(bibfile, parser)

    def line_of(self, key: str):
        with open(self.file_path, 'r', encoding='utf-8') as bibfile:
            for index, line in enumerate(bibfile):
                line = line.strip()
                if re.match(rf'^@\w+{{{key}', line):
                    return index
        return None
