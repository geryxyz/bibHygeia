import os
import typing
import pytest
from argparse import ArgumentParser

from src.commands.Command import Command, bibhygeia_command
from src.util import *

bibs: typing.List[BibFile] = []


def run_tests() -> None:
    file_dir_path = os.path.dirname(os.path.realpath(__file__))

    # -s is for printing out the program outputs
    pytest.main([file_dir_path, "-s", "--junitxml=test_results.xml"])


def input_bib_files() -> typing.List[BibFile]:
    """
    Iterates over the bib files and yields the bib files.
    """

    for bib_file in bibs:
        yield bib_file


def input_biber_entries() -> typing.List[typing.Dict[str, typing.Any]]:
    """
    Iterates over the bib files and yields the biber entries.
    """

    for bib_file in bibs:
        for db in bib_file.bibliography.entries:
            yield db


@bibhygeia_command(name="check", description="Checks BibTeX entries in the given path.")
class CheckCommand(Command):
    """
    This Command checks BibTeX entries in the given path.
    """

    def __init__(self, name: str, description: str) -> None:
        super().__init__(name, description)
        self.bib_files: typing.List[BibFile] = []

    def make_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument("path", metavar="PATH", help="Path to check for .bib files recursively")
        parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    def run(self, args: typing.Any) -> None:
        global bibs

        self.bib_files = BibFile.read_bib_files(args.path)
        bibs = self.bib_files

        run_tests()
