import typing

from src.util import BibEntry, Hint
from src.report_generator.failure.CheckFailure import CheckFailure


class EntryCheckFailure(CheckFailure):
    """
    A failure that occurred while checking an entry.
    """

    def __init__(self, entry: BibEntry, message: str, hints: typing.List[Hint]):
        """
        Initializes a new EntryCheckFailure.

        :param entry: The entry that failed.
        :type entry: BibEntry
        :param message: The message of the failure.
        :type message: str
        """
        super().__init__(message)
        self.entry = entry
        self.hints: typing.List[Hint] = hints

    def to_dict(self):
        return {
            "type": self.type,
            "entry_key": self.entry.key,
            "file_path": self.entry.file_path,
            "line_number": self.entry.line_number,
            "message": self.message,
            "hints": [hint.to_dict() for hint in self.hints],
        }
