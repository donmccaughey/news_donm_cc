from pathlib import Path
from news import CACHE_DIR
from .options import Options


def test_no_options() -> None:
    options = Options.parse([])
    assert options.cache_dir == Path(CACHE_DIR)
    assert options.no_store == False


def test_cache_dir() -> None:
    options = Options.parse(['--cache-dir', 'tmp'])
    assert options.cache_dir == Path('tmp')


def test_no_store() -> None:
    options = Options.parse(['--no-store'])
    assert options.no_store == True
