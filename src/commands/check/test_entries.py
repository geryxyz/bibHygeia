import pytest
from src.util import BibFile

from .CheckCommand import input_bib_files


@pytest.mark.parametrize("bib_file", input_bib_files())
def test_bib_file(bib_file: BibFile):
    print(f"Checking {bib_file.file_path}")
    assert bib_file.file_path == bib_file.file_path
