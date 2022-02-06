import pytest

from src.util import Hint, BibEntry
from src.util.text import TranscriptionFunctions


@pytest.fixture()
def hint_readable_id(entry: BibEntry, request, record_hint):
    yield
    if not request.node.rep_call.failed:
        return

    clean_title = TranscriptionFunctions.lower(TranscriptionFunctions.drop_specials(entry['title']))
    hint: Hint = Hint('title-based key',
                      f'Change the key of "{entry.id}" to (at least starts with) "{clean_title}" in line {entry.line_number}.',
                      'Most of the editor will offer suggestions and prefill the keys;'
                      ' furthermore these keys are easier to read during writting.',
                      'title_as_key')
    record_hint(hint)
