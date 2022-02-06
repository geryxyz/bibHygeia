import pytest

from src.util import Hint


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # https://docs.pytest.org/en/latest/example/simple.html#making-test-result-information-available-in-fixtures
    outcome = yield
    rep = outcome.get_result()

    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture()
def record_hint(record_property):
    def _record_hint(hint: Hint):
        record_property("hint_title", hint.title)
        record_property("hint_recommendation", hint.recommendation)
        record_property("hint_reason", hint.reason)
        record_property("hint_phase", hint.phase)
    return _record_hint
