import json
import os
import re
import time
import typing

import pytest

from src.util import Hint
from src.util.BibEntry import BibEntry
from src.util.Singleton import Singleton
from src.util.bibtex_line import Line
from src.report_generator.failure.EntryCheckFailure import EntryCheckFailure
from src.report_generator.failure.FileLineCheckFailure import FileLineCheckFailure
from src.report_generator.Report import Report


class ReportGenerator(object, metaclass=Singleton):
    """
    Collects all reports and generates a report.
    This class is a pytest plugin.
    """

    report: Report

    def __init__(self):
        self.report = Report()

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        # https://docs.pytest.org/en/latest/example/simple.html#making-test-result-information-available-in-fixtures
        outcome = yield
        report = outcome.get_result()

        setattr(item, "report_" + report.when, report)

        if report.when == "call" and report.failed:
            call_params: dict = item.callspec.params
            failure_message = report.longrepr.reprcrash.message

            entry: BibEntry = call_params.get("entry", None)
            line: Line = call_params.get("line", None)

            # Get the failure message from the long assertion error message
            # Pytest will print additional information after the error message,
            # e.g. `assert val == expected, "Failure message"`
            if match := re.search(r"^AssertionError: (.*?)(\n|$)", failure_message):
                failure_message = match.group(1)

            # TODO: create decorator or fixture to determine the type of failure
            if isinstance(entry, BibEntry):
                hints: typing.List[Hint] = getattr(item, "hints", [])
                self._add_entry_check_failure(entry, failure_message, hints)
            elif isinstance(line, Line):
                self._add_file_line_check_failure(line, failure_message)
            # else:
            #     self._add_simple_failure(failure_message)

    def pytest_sessionstart(self, session: pytest.Session):
        self.report.start_time = time.time()

    def pytest_sessionfinish(self, session: pytest.Session):
        self.report.end_time = time.time()
        self._write_report()

    def _add_entry_check_failure(self, entry: BibEntry, failure: str, hints: typing.List[Hint]):
        self.report.add_entry(entry)  # TODO: Add every entry, not just the affected one
        self.report.add_failure(EntryCheckFailure(entry, failure, hints))

    def _add_file_line_check_failure(self, line: Line, failure_message: str):
        self.report.add_failure(FileLineCheckFailure(line.file_path, line.line_number, failure_message))

    def _write_report(self):
        """ Write reports to the report directory. """

        report_base_path = os.path.join(os.getcwd(), "report")

        if not os.path.exists(report_base_path):
            os.makedirs(report_base_path)

        # Dump reports to a javascript file
        with open(os.path.join(report_base_path, "report_data.js"), "w") as report_fp:
            report_json = json.dumps(self.report.to_dict())
            report_fp.write(f"var report = {report_json};\n")

        resource_files = ["report.html", "main.js", "styles.css"]

        # Write resource files to report directory
        for resource_file in resource_files:
            with open(os.path.join(os.path.dirname(__file__), "resources", resource_file), "r") as resource_fp:
                resource_data = resource_fp.read()

            with open(os.path.join(report_base_path, resource_file), "w") as target_fp:
                target_fp.write(resource_data)
