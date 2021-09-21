import unittest

from owl.core.decorators import biber_log_checker, hinted
from owl.hinting.hint import warn_about_month_field


@biber_log_checker
@hinted(hinter=warn_about_month_field)
def no_warnings(line: str, case: unittest.TestCase):
    case.assertNotRegex(line, r'^WARN', line)