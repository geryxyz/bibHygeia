import os
import typing
from argparse import ArgumentParser
from uuid import uuid4

import pytest

from src.commands.Command import Command, bibhygeia_command
from src.commands.check.HintCollector import HintCollector
from src.util import *
from src.util.constants import DEFAULT_CHECK_TEST_RESULTS_XML, DEFAULT_CHECK_TEST_HINTS_XML

bib_files: typing.List[BibFile] = []
run_id: str


def run_tests(test_results_file: str) -> None:
    global run_id

    file_dir_path = os.path.dirname(os.path.realpath(__file__))
    config_file_path = os.path.join(file_dir_path, "pytest.ini")

    # Generate random GUID to match test results with hints
    run_id = str(uuid4())

    # -s is for printing out the program outputs
    pytest.main([file_dir_path, "-s", f"--junitxml={test_results_file}", "-c", config_file_path,
                 "-o", f"junit_suite_name={run_id}"])


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
        parser.add_argument("--results-file", metavar="RESULTS_FILE",
                            help=f"Path to the test results xml file. Default: {DEFAULT_CHECK_TEST_RESULTS_XML}",
                            default=DEFAULT_CHECK_TEST_RESULTS_XML)
        parser.add_argument("--hints-file", metavar="HINTS_FILE",
                            help=f"Path to the hints xml file. Default: {DEFAULT_CHECK_TEST_HINTS_XML}",
                            default=DEFAULT_CHECK_TEST_HINTS_XML)
        parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    def run(self, args: typing.Any) -> None:
        global bib_files
        global run_id

        # Read .bib files
        self.bib_files = BibFile.read_bib_files(args.path)
        bib_files = self.bib_files

        # Run tests
        run_tests(args.results_file)

        # Collect hints
        hint_collector = HintCollector()
        hint_collector.write_hints_to_xml(args.hints_file, run_id)
