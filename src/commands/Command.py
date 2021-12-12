from abc import ABC, abstractmethod
from argparse import ArgumentParser
import typing


class Command(ABC):
    """
    Base class for commands in the bibHygeia application.

    :param name: The name of the command.
    :param description: The description of the command.
    """

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def make_parser(self, parser: ArgumentParser) -> None:
        pass

    @abstractmethod
    def run(self, args: typing.Any) -> None:
        pass


registered_commands: typing.List[Command] = []


def bibhygeia_command(name: str, description: str) -> type(Command):
    """
    Decorator for registering a command.

    :param name: The name of the command.
    :param description: The description of the command.
    """

    def inner(command_class: type(Command)) -> type(Command):
        registered_commands.append(command_class(name, description))
        return command_class

    return inner
