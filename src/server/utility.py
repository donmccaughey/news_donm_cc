from pathlib import Path
from typing import Collection


def get_version() -> str:
    version_path = Path('version.txt')
    if version_path.exists():
        try:
            with version_path.open() as f:
                version = f.read().strip()
                if version:
                    return version
        except OSError:
            pass
    return 'unknown'


def count_phrase(collection: Collection, word: str) -> str:
    count = len(collection)
    phrase = f'{count} {word}'
    return phrase if count == 1 else phrase + 's'
