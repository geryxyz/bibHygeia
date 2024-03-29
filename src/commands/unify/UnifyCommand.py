import typing
from argparse import ArgumentParser

from src.commands.Command import Command, register_command


@register_command(name="unify", description="Unifies BibTeX records")
class UnifyCommand(Command):
    """
    This Command unifies BibTeX records.
    """

    def make_parser(self, parser: ArgumentParser) -> None:
        pass

    def run(self, args: typing.Any) -> None:
        pass
