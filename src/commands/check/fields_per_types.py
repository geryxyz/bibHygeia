# https://en.wikipedia.org/wiki/BibTeX#Entry_types
import typing

from src.util.quantifier import Quantifier, Mandatory, AllOf, AtLeastOneOf, MaybeOneOf

fields_per_types: typing.Dict[str, typing.Tuple[Quantifier, ...]] = {
    'article': (
        Mandatory('author'), Mandatory('title'),
        AllOf('journal', 'year', 'volume')
    ),
    'book': (
        AtLeastOneOf('author', 'editor'), Mandatory('title'),
        AllOf('publisher', 'year'), MaybeOneOf('volume', 'number')
    ),
    'booklet': (
        Mandatory('author'), Mandatory('title')
    ),
    'conference': (
        Mandatory('author'), Mandatory('title'),
        AllOf('booktitle', 'year'), MaybeOneOf('volume', 'number')
    ),
    'inbook': (
        AtLeastOneOf('author', 'editor'), Mandatory('title'), AtLeastOneOf('chapter', 'pages'),
        AllOf('publisher', 'year'), MaybeOneOf('volume', 'number')
    ),
    'incollection': (
        Mandatory('author'), Mandatory('title'),
        AllOf('booktitle', 'publisher', 'year'), MaybeOneOf('volume', 'number')
    ),
    'inproceedings': (
        Mandatory('author'), Mandatory('title'),
        AllOf('booktitle', 'year'), MaybeOneOf('volume', 'number')
    ),
    'manual': (
        Mandatory('title'),  # the coma ensures that this is a tuple
    ),
    'mastersthesis': (
        Mandatory('author'), Mandatory('title'),
        AllOf('year', 'school')
    ),
    'misc': (),
    'phdthesis': (
        Mandatory('author'), Mandatory('title'),
        AllOf('year', 'school')
    ),
    'proceedings': (
        Mandatory('author'), Mandatory('title'),
        MaybeOneOf('volume', 'number')
    ),
    'techreport': (
        Mandatory('author'), Mandatory('title'),
        AllOf('institution', 'year')
    ),
    'unpublished': (
        Mandatory('author'), Mandatory('title'),
        Mandatory('note')
    )
}
