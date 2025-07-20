import pickle
from os import PathLike
from pathlib import Path

from .types_ import Assets


def load_compiled_assets(file_path: str | PathLike | Path) -> Assets:
    with open(file_path, "rb") as f:
        return pickle.load(f)
