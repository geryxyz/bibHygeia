import pytest

from src.report_generator import ReportGenerator
from src.util import Hint


def pytest_configure(config: pytest.Config):
    report_generator = ReportGenerator()
    config.pluginmanager.register(report_generator, "report_generator")


@pytest.fixture
def store_hint(request: pytest.FixtureRequest, record_property):
    def _store_hint(hint: Hint):
        hints = getattr(request.node, "hints", [])
        request.node.hints = hints + [hint]

    return _store_hint
