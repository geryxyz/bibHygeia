import argparse
import sys


def bool_switch(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def in_in(what, containers):
    for container in containers:
        if what in container:
            return True
    return False


def level_of(open: str, close: str, text: str):
    if len(open) > 1 or len(close) > 1:
        raise ValueError('only single char allowed')
    current_level = 0
    levels = []
    for char in text:
        if char == open:
            current_level += 1
            levels.append((current_level - 1, current_level))
        elif char == close:
            current_level -= 1
            levels.append((current_level + 1, current_level))
        else:
            levels.append((current_level,))
    return levels


valid_bibtex_types = {
    'article': 'An article from a journal or magazine.',
    'book': 'A book with an explicit publisher.',
    'booklet': 'A work that is printed and bound, but without a named publisher or sponsoring institution.',
    'conference': 'The same as inproceedings, included for Scribe compatibility.',
    'inbook': 'A part of a book, usually untitled. May be a chapter (or section, etc.) and/or a range of pages.',
    'incollection': 'A part of a book having its own title.',
    'inproceedings': 'An article in a conference proceedings.',
    'manual': 'Technical documentation.',
    'mastersthesis': 'A Master\'s thesis.',
    'misc': 'For use when nothing else fits.',
    'phdthesis': 'A Ph.D. thesis.',
    'proceedings': 'The proceedings of a conference.',
    'techreport': 'A report published by a school or other institution, usually numbered within a series.',
    'unpublished': 'A document having an author and title, but not formally published.'
}
