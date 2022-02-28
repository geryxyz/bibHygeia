import pytest
from _pytest.fixtures import FixtureRequest

from src.commands.check.HintCollector import HintCollector
from src.util import Hint


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[None]):
    # https://docs.pytest.org/en/latest/example/simple.html#making-test-result-information-available-in-fixtures
    outcome = yield
    report = outcome.get_result()

    setattr(item, "report_" + report.when, report)


@pytest.fixture
def store_hint(request: FixtureRequest, record_property):
    hint_collector = HintCollector()

    def _store_hint(hint: Hint):
        test_id = request.node.nodeid
        hint_collector.add_hint(test_id, hint)

    return _store_hint
