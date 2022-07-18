import typing

import pytest

from src.util.BibEntry import BibEntry
from src.util.quantifier import Quantifier, Mandatory


def mandatory_quantifiers() -> typing.List[Mandatory]:
    for i in ["A"]:
        yield Mandatory(i)


test_entry_good = BibEntry({
    "ID": "test",
    "ENTRYTYPE": "article",
    "title": "Test",
    "A": "A",
}, 0)

test_entry_bad = BibEntry({
    "ID": "test",
    "ENTRYTYPE": "article",
    "title": "Test",
}, 0)


@pytest.mark.parametrize("quantifier", mandatory_quantifiers())
def test_mandatory_check_should_not_raise_assertion_error(quantifier: Mandatory):
    try:
        quantifier.check(test_entry_good.key, test_entry_good)
    except AssertionError:
        pytest.fail("Mandatory quantifier should not raise assertion error if field is present")


@pytest.mark.parametrize("quantifier", mandatory_quantifiers())
def test_mandatory_check_should_raise_assertion_error(quantifier: Mandatory):
    with pytest.raises(AssertionError) as e:
        quantifier.check(test_entry_bad.key, test_entry_bad)

    assert "is mandatory in entry" in str(e.value), \
        "Mandatory quantifier should raise assertion error if field is missing"
