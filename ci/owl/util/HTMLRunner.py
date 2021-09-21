from __future__ import annotations

import datetime
import traceback
import unittest
import typing
from enum import Enum
from types import TracebackType

from owl.core.decorators import HINT_ATTR_NAME, biber_log_checkers, biber_file_checkers, biber_entry_checkers
from owl.util.TestStatus import TestStatus
from owl.util.Hint import Hint
from owl.util.statistical_constants import COUNT_OF_EXECUTED_SUBTESTS, COUNT_OF_EXECUTED_TESTS, \
    COUNT_OF_AVERAGE_SUBTESTS_PER_TEST, COUNT_OF_LOG_CHECKERS, COUNT_OF_ENTRY_CHECKERS, COUNT_OF_BIBFILE_LINE_CHECKERS, \
    COUNT_OF_AVERAGE_BIBFILE_LINE_CHECKING_PER_LINES, COUNT_OF_BIBFILE_LINE_CHECKING, COUNT_OF_CHECKED_BIBFILE_LINES
from owl.util.text import shorten_end, html_line_breaks

_SysExcInfoType = typing.Tuple[type, BaseException, TracebackType]


class TestCaseResult(object):
    def __init__(self, test: unittest.case.TestCase):
        self.test: unittest.case.TestCase = test
        self._outcome: typing.Optional[_SysExcInfoType] = None
        self.status: typing.Optional[TestStatus] = None
        self.subtests: typing.List[TestCaseResult] = []

    def __str__(self):
        return f'{self.test.id()}: {self.status}'

    @property
    def outcome(self) -> typing.Optional[_SysExcInfoType]:
        return self._outcome

    @outcome.setter
    def outcome(self, value: typing.Optional[_SysExcInfoType]):
        self._outcome = value
        if self._outcome is None:
            self.status = TestStatus.PASSED
        elif isinstance(self._outcome[1], AssertionError):
            self.status = TestStatus.FAILED
        else:
            self.status = TestStatus.ERROR

    @property
    def worst_substatus(self) -> TestStatus:
        for subtest in self.subtests:
            if subtest.status == TestStatus.ERROR:
                return TestStatus.ERROR
        for subtest in self.subtests:
            if subtest.status == TestStatus.FAILED:
                return TestStatus.FAILED
        return TestStatus.PASSED

    def subtest_distribution(self) -> typing.Dict[TestStatus, typing.List[TestCaseResult]]:
        distribution = {}
        for subtest in self.subtests:
            distribution[subtest.status] = distribution.get(subtest.status, []) + [subtest]
        return distribution


class HTMLResult(unittest.TestResult):
    def __init__(self):
        super().__init__()
        self.executedTests: typing.Dict[str, typing.Union[TestCaseResult, None]] = {}

    @property
    def is_succeeded(self) -> bool:
        for test in self.executedTests.values():
            if test.status in [TestStatus.FAILED, TestStatus.ERROR]:
                return False
            for subtest in test.subtests:
                if subtest.status in [TestStatus.FAILED, TestStatus.ERROR]:
                    return False
        return True

    def _get_current_result(self, test: unittest.case.TestCase) -> TestCaseResult:
        if test.id() not in self.executedTests:
            self.executedTests[test.id()] = TestCaseResult(test)
        return self.executedTests[test.id()]

    def startTest(self, test: unittest.case.TestCase) -> None:
        print(f"{test.id()} ...")
        self.executedTests[test.id()] = TestCaseResult(test)

    def addSubTest(self, test: unittest.case.TestCase, subtest: unittest.case._SubTest,
                   outcome: typing.Optional[_SysExcInfoType]) -> None:
        print(f'\t{subtest.id()}')
        subtest_result = TestCaseResult(subtest)
        subtest_result.outcome = outcome
        self._get_current_result(test).subtests.append(subtest_result)

    def stopTest(self, test: unittest.case.TestCase) -> None:
        print("done")

    def addSuccess(self, test: unittest.case.TestCase) -> None:
        print('Passed!')
        self._get_current_result(test).outcome = None

    def addFailure(self, test: unittest.case.TestCase, err: _SysExcInfoType) -> None:
        print('Failed!')
        self._get_current_result(test).outcome = err

    def addError(self, test: unittest.case.TestCase, err: _SysExcInfoType) -> None:
        print('Error!')
        self._get_current_result(test).outcome = err

    def addUnexpectedSuccess(self, test: unittest.case.TestCase) -> None:
        print('Failed!')
        raise NotImplementedError()


def log_test(entry: TestCaseResult, report_file: typing.TextIO, parent: TestCaseResult = None):
    if entry.status == TestStatus.PASSED:
        return

    headers = {}
    if entry.test._testMethodName != 'runTest':
        headers['method'] = entry.test._testMethodName
    if hasattr(entry.test, '_message'):
        headers['message'] = getattr(entry.test, "_message")
    if parent is not None:
        headers['parent method'] = parent.test._testMethodName
    if hasattr(entry.test, 'params'):
        params = dict(getattr(entry.test, 'params'))
        if 'checker' in params:
            headers['checker'] = params['checker']

    report_file.write('<div>')

    report_file.write(f'<h2>{"; ".join(sorted(headers.values()))}</h2>')

    report_file.write('<table class="header">')
    for name, value in headers.items():
        report_file.write(f'<tr><th>{name}</th><th>=</th><td>{value}</td></tr>')
    report_file.write('</table>')

    report_file.write('<table>')
    report_file.write(f'<tr><th>Id</th><td>{entry.test.id()}</td></tr>')
    if entry.status is None:
        report_file.write(f'<tr><th>Result</th><td>{str(entry.status).lower()}</td></tr>')
    else:
        report_file.write(f'<tr><th>Result</th><td><span class="{entry.status.name.lower()}">{entry.status.name.lower()}</span></td></tr>')
    if entry.outcome is not None:
        pretty_exc = "<br/>".join(traceback.format_exception(entry.outcome[0], entry.outcome[1], entry.outcome[2]))
        message = entry.outcome[1].args[0]
        exception_name = entry.outcome[0].__name__
        report_file.write(f'<tr><th>Message</th><td>{shorten_end(str(message))}</td></tr>')
        if entry.status == TestStatus.FAILED:
            report_file.write(f'<tr><th>Assertion</th><td>{exception_name}</td></tr>')
        elif entry.status == TestStatus.ERROR:
            report_file.write(f'<tr><th>Error</th><td>{exception_name}</td></tr>')
            report_file.write(f'<tr><th>Traceback</th><td>{pretty_exc}</td></tr>')
        for index, value in enumerate(entry.outcome[1].args):
            report_file.write(f'<tr><th>argument#{index}</th><td>{shorten_end(str(value))}</td></tr>')
    report_file.write('</table>')

    report_file.write('<h3>Hints</h3>')
    report_file.write('<p>These hints are presented as guidelines or suggestions. '
                      'By the best of intention it cannot be granted '
                      'that the test will passed if you follow all of them.</p>')
    if hasattr(entry.test, HINT_ATTR_NAME):
        hints = getattr(entry.test, HINT_ATTR_NAME)
        log_hints(hints, report_file)

    report_file.write('</div>')


def log_tests(entries: typing.List[TestCaseResult], report_file: typing.TextIO):
    for entry in entries:
        log_test(entry, report_file)
        for subentry in entry.subtests:
            log_test(subentry, report_file, entry)


def log_hints(hints: typing.List[Hint], report_file: typing.TextIO):
    for hint in hints:
        log_hint(hint, report_file)


def log_hint(hint: Hint, report_file: typing.TextIO):
    report_file.write(f'<div class="hint">')
    report_file.write(f'<span class="title">{hint.title}</span>')
    report_file.write(f'<br/><span class="subtitle">Hint from {hint.phase}</span>')
    report_file.write(f'<p>{html_line_breaks(hint.recommendation)}</p>')
    report_file.write(f'<p>Why? {html_line_breaks(hint.reason)}</p>')
    report_file.write('</div>')


class HTMLRunner(object):
    statistics: typing.Dict[str, typing.Union[int, float]] = {}

    def __init__(self):
        self._last_run_time = None

    def run(self, test: typing.Union[unittest.TestCase, unittest.TestSuite]):
        result = HTMLResult()
        HTMLRunner.hints = []
        self._last_run_time = datetime.datetime.now()
        test.run(result)
        self._save_test_report(result)
        return result

    def _save_test_report(self, result: HTMLResult):
        with open('report.html', 'w', encoding='utf-8') as report_file:
            report_file.write(f'<html><head><style>')
            with open('style.css', 'r', encoding='utf-8') as css_file:
                report_file.write(css_file.read())
            HTMLRunner.statistics[COUNT_OF_EXECUTED_SUBTESTS] = sum([len(test.subtests) for test in result.executedTests.values()])
            HTMLRunner.statistics[COUNT_OF_EXECUTED_TESTS] = len(result.executedTests)
            HTMLRunner.statistics[COUNT_OF_AVERAGE_SUBTESTS_PER_TEST] =\
                HTMLRunner.statistics[COUNT_OF_EXECUTED_SUBTESTS] / HTMLRunner.statistics[COUNT_OF_EXECUTED_TESTS]
            HTMLRunner.statistics[COUNT_OF_LOG_CHECKERS] = len(biber_log_checkers)
            HTMLRunner.statistics[COUNT_OF_ENTRY_CHECKERS] = len(biber_entry_checkers)
            HTMLRunner.statistics[COUNT_OF_BIBFILE_LINE_CHECKERS] = len(biber_file_checkers)
            HTMLRunner.statistics[COUNT_OF_AVERAGE_BIBFILE_LINE_CHECKING_PER_LINES] =\
                HTMLRunner.statistics[COUNT_OF_BIBFILE_LINE_CHECKING] / HTMLRunner.statistics[COUNT_OF_CHECKED_BIBFILE_LINES]
            report_file.write(f'''</style><title>Test Report</title>
                    </head>
                    <body>
                        <h1>Test Report from the Spirit Library</h1>
                        <p>Checked at {self._last_run_time}.</p>''')
            report_file.write('<table class="header">')
            for name, value in HTMLRunner.statistics.items():
                report_file.write(f'<tr><th>{name}:</th><td>{value}</td></tr>')
            report_file.write('</table>')
            log_tests(list(result.executedTests.values()), report_file)
            report_file.write(f'''
                    </body>
                </html>''')
