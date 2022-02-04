import os
import typing
import pytest
from argparse import ArgumentParser

from src.commands.Command import Command, bibhygeia_command
from src.util import *

bib_files: typing.List[BibFile] = []


def run_tests() -> None:
    file_dir_path = os.path.dirname(os.path.realpath(__file__))
    config_file_path = "''"  # Ignore other config files

    # -s is for printing out the program outputs
    pytest.main([file_dir_path, "-s", "--junitxml=test_results.xml", "-c", config_file_path])


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
        global bib_files

        self.bib_files = BibFile.read_bib_files(args.path)
        bib_files = self.bib_files

        run_tests()
