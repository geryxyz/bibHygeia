import typing
from argparse import ArgumentParser

from src.Command import Command, bibhygeia_command


@bibhygeia_command(name='unify', description='Unifies BibTeX records')
class UnifyCommand(Command):
    """
    This Command unifies BibTeX records.
    """

    def make_parser(self, parser: ArgumentParser) -> None:
        pass

    def run(self, args: typing.Any) -> None:
        pass
