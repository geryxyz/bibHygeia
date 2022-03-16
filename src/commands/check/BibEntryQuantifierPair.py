import dataclasses

from src.util import BibEntry
from src.util.quantifier import Quantifier


@dataclasses.dataclass
class BibEntryQuantifierPair:
    entry: BibEntry
    quantifier: Quantifier
