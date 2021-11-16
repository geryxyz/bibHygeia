import typing
from argparse import ArgumentParser
from src.Command import Command, bibhygeia_command


@bibhygeia_command(name='dedup', description='Remove duplications from .bib files.')
class DedupCommand(Command):
    """
    This Command removes duplicated BibTeX entries from .bib files.
    """

    def make_parser(self, parser: ArgumentParser) -> None:
        parser.add_argument("-f", "--file", dest="file", help="File to deduplicate", required=True)
        parser.add_argument("-o", "--output", dest="output", help="Output file", required=True)

    def run(self, args: typing.Any) -> None:
        pass
