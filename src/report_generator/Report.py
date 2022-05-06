import typing

from src.util import BibEntry
from src.report_generator.failure.CheckFailure import CheckFailure


class Report(object):
    start_time: float
    end_time: float
    entries: typing.Set[BibEntry]
    failures: typing.List[CheckFailure]

    def __init__(self):
        self.entries = set()
        self.failures = []

    def to_dict(self):
        return {
            'start_time': self.start_time,
            'end_time': self.end_time,
            'entries': {
                entry.key: entry.to_dict() for entry in self.entries
            },
            'failures': [
                failure.to_dict() for failure in self.failures
            ]
        }

    def add_entry(self, entry: BibEntry):
        self.entries.add(entry)

    def add_failure(self, failure: CheckFailure):
        self.failures.append(failure)
