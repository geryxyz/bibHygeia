import typing
from argparse import ArgumentParser

from src.Command import Command, bibhygeia_command


@bibhygeia_command(name='check', description='Checks BibTeX entries in the given path.')
class CheckCommand(Command):
    """
    This Command checks BibTeX entries in the given path.
    """

    def make_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument("path", help="Path to check for .bib files")
        parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    def run(self, args: typing.Any) -> None:
        pass
