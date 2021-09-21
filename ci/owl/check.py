# PyCharm cannot resolve the usage via decorators and unittest exploration
# noinspection PyUnresolvedReferences
from owl.core.biber_execution import *
# noinspection PyUnresolvedReferences
from owl.core.biber_validation import *
# noinspection PyUnresolvedReferences
from owl.checking.biber_entry_checking import *
# noinspection PyUnresolvedReferences
from owl.checking.biber_file_checking import *
# noinspection PyUnresolvedReferences
from owl.checking.biber_log_checking import *
from owl.util.HTMLRunner import HTMLRunner

if __name__ == '__main__':
    for log_file in glob2.glob('*.lg'):
        os.remove(log_file)
    for log_file in glob2.glob('*.html'):
        os.remove(log_file)
    # there is actually no TestRunner base class but PyCharm somehow infers it
    # noinspection PyTypeChecker
    test_program = unittest.main(exit=False, testRunner=HTMLRunner())
    print("tests executed")
    if not (hasattr(test_program.result, 'is_succeeded') and getattr(test_program.result, 'is_succeeded')):
        exit(1)
