import unittest
import subprocess
import os
import glob2

from owl.core.decorators import biber_log_checkers, HINTER_ATTR_NAME, HINT_ATTR_NAME, assign_hint_to
from owl.util.HTMLRunner import HTMLRunner
from owl.util.BibFile import BibFile
from owl.util.LaTeXmk import LaTeXmk, BIBFILE_NAME
from owl.util.statistical_constants import COUNT_OF_CHECKED_LOG_LINES


class TestBiberExecution(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bib_file: BibFile = BibFile(BIBFILE_NAME)

    def setUp(self) -> None:
        subprocess.run('latexmk -C', shell=True, capture_output=True)
        for file in glob2.glob('*.bbl') + glob2.glob('*.run.xml'):
            os.remove(file)

    def test_execution_without_error(self):
        self.assertEqual(0, LaTeXmk().return_code, msg="there was some error during the execution of LaTeXmk")

    def test_biber_log(self):
        process = LaTeXmk()
        process.save_logs()
        HTMLRunner.statistics[COUNT_OF_CHECKED_LOG_LINES] = 0
        for line in process.biber_session.split('\n'):
            HTMLRunner.statistics[COUNT_OF_CHECKED_LOG_LINES] += 1
            for checker in biber_log_checkers:
                with self.subTest('checking log line', line=line.strip(), checker=checker.__name__):
                    try:
                        checker(line, self)
                    finally:
                        if hasattr(checker, HINTER_ATTR_NAME):
                            for hinter in getattr(checker, HINTER_ATTR_NAME):
                                hint = hinter(line, TestBiberExecution.bib_file)
                                if hint is not None:
                                    assign_hint_to(self, hint)
