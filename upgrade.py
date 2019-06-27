import argparse
import logging
import os
import re
import sys

import glob2
import jsonpickle

import original


class Replacement:
    def __init__(self, original, new, reason=None):
        super().__init__()
        self.original = original
        self.new = new
        self.reason = reason


class Upgrade(list):
    VERSION = 1

    def __init__(self):
        super().__init__()
        self.version = Upgrade.VERSION

    def save(self, path):
        with open(path + '.ugr', 'w', encoding='utf8') as output:
            output.write(jsonpickle.encode(self))

    @staticmethod
    def load(path):
        with open(path, 'r', encoding='utf8') as inpath:
            content = inpath.read()
            data = jsonpickle.decode(content)
            if data.version == Upgrade.VERSION:
                return data
            else:
                raise TypeError("invalid upgrade file version")

    def add_if_not_present(self, replacement):
        if (replacement.original, replacement.new) not in [(r.original, r.new) for r in self]:
            self.append(replacement)


class Similar:
    def __init__(self, saved, dropped, property, degree):
        self.saved = saved
        self.dropped = dropped
        self.property = property
        self.degree = degree

    def human_readable(self):
        return "'{}' (dropped) is {:.2%} similar to '{}' (saved)".format(
            self.dropped[self.property],
            self.degree,
            self.saved[self.property])


logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
logger.addHandler(handler)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="upgrade.py",
        description='bibHygeia Upgrade: Upgrade all existing citation keys based on action of other tools.',
        epilog='Upgrade is part of bibHygeia toolkit.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-u', '--upgrade_file', type=str, required=True,
                        help='file containing the action (side-effects) of other tool')
    parser.add_argument('-i', '--input_folder', type=str, required=True,
                        help='input folder to searching *.tex files recursively')
    parser.add_argument('-e', '--exclude_pattern', type=str, default=None, required=False,
                        help='regular expression to exclude irrelevant sub-folder')
    parser.add_argument('--log', type=str, default='INFO', required=False,
                        help='level of log messages to display')

    args = parser.parse_args()

    logger.setLevel(logging.getLevelName(args.log))

    upgrade: Upgrade = Upgrade.load(args.upgrade_file)
    logger.info('{} replacements loaded'.format(len(upgrade)))

    tex_files = []
    for file in glob2.glob(os.path.join(args.input_folder, '**', '*.tex')):
        if args.exclude_pattern is not None and re.search(args.exclude_pattern, file):
            continue
        tex_files.append(file)
    logger.info('{} LaTeX files found'.format(len(tex_files)))
    if original.originals_in(args.input_folder):
        logger.error("original files present, remove them")
        sys.exit()
    for file in tex_files:
        original.save_current_state(file)
    logger.info('original files are created to back-up if before changes')

    action_count = 0
    for replacement in upgrade:
        logger.debug('replacing {} with {}'.format(replacement.original, replacement.new))
        for file in tex_files:
            out_file_path = file
            in_file_path = file + '.original'
            with open(in_file_path, 'r', encoding='utf8') as in_file, open(out_file_path, 'w', encoding='utf8') as out_file:
                line: str
                for line_number, line in enumerate(in_file):
                    new_line = line
                    if replacement.original in line:
                        logger.debug('old cite found in {} at line#{}'.format(file, line_number))
                        action_count += 1
                        new_line = line.replace(replacement.original, replacement.new)
                    out_file.write(new_line)
    logger.info('{} cites were updated'.format(action_count))