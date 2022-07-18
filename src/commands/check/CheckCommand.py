import os
import sys
import typing
from argparse import ArgumentParser

import pytest

from src.commands.Command import Command, register_command
from src.util import *

bib_files: typing.List[BibFile] = []


def run_tests() -> None:
    print("Running checks...")
    file_dir_path = os.path.dirname(os.path.realpath(__file__))

    # -s is for printing out the program outputs

    pytest_exit = pytest.main([file_dir_path,
                               "--tb=no",  # no traceback
                               "-c=''",  # prevent pytest from reading pytest.ini from root directory
                               "--no-header", "--no-summary", "-q"])

    sys.exit(pytest_exit)


@register_command(name="check", description="Checks BibTeX entries in the given path.")
class CheckCommand(Command):
    """
    This Command checks BibTeX entries in the given path.
    """

    def __init__(self, name: str, description: str) -> None:
        super().__init__(name, description)
        self.bib_files: typing.List[BibFile] = []

    def make_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument("path", metavar="PATH", help="Path to check for .bib files recursively")

    def run(self, args: typing.Any) -> None:
        global bib_files

        # Read .bib files
        self.bib_files = BibFile.read_bib_files(args.path)
        bib_files = self.bib_files

        # Run tests
        run_tests()
