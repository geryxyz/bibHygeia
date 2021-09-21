def count_of_prefix(name: str) -> str:
    return f'count of {name}'


def average_of_prefix(name: str) -> str:
    return f'average of {name}'


COUNT_OF_CHECKED_LOG_LINES = count_of_prefix('checked log lines')
COUNT_OF_LOG_CHECKERS = count_of_prefix('log line checkers')

COUNT_OF_ENTRY_CHECKERS = count_of_prefix('entry checkers')
COUNT_OF_CHECKED_ENTRIES = count_of_prefix('checked entries')


COUNT_OF_CLASSIFIED_BIBFILE_LINES = count_of_prefix('classified bib-file lines')
COUNT_OF_CHECKED_BIBFILE_LINES = count_of_prefix('checked bib-file lines')
COUNT_OF_BIBFILE_LINE_CHECKERS = count_of_prefix('bib-file line checkers')
COUNT_OF_BIBFILE_LINE_CHECKING = count_of_prefix('bib-file line checking')
COUNT_OF_AVERAGE_BIBFILE_LINE_CHECKING_PER_LINES = count_of_prefix(average_of_prefix('bib-file line checking per lines'))

COUNT_OF_AVERAGE_SUBTESTS_PER_TEST = count_of_prefix(average_of_prefix('subtests per test'))
COUNT_OF_EXECUTED_TESTS = count_of_prefix('executed tests')
COUNT_OF_EXECUTED_SUBTESTS = count_of_prefix('executed subtests')
