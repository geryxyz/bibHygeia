import shutil
from typing import List

import glob2
import os

_original_postfix = '.original'


def has_original(file_path:str) -> bool:
    original_path = file_path + _original_postfix
    return os.path.isfile(original_path)


def originals_in(directory) -> List[str]:
    originals = glob2.glob(os.path.join(directory, '**', '*{}'.format(_original_postfix)))
    return originals


def save_current_state(file_path):
    original_path = file_path + _original_postfix
    if os.path.isfile(original_path):
        raise FileExistsError(original_path)
    shutil.copyfile(file_path, original_path)
    return original_path


def restore_original_states(directory):
    originals = originals_in(directory)
    for original_path in originals:
        file_path = original_path.replace(_original_postfix, '')
        os.replace(original_path, file_path)
    return originals


def drop_original_states(directory):
    originals = originals_in(directory)
    for original_path in originals:
        os.remove(original_path)
    return originals
