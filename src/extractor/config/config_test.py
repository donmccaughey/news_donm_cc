from pathlib import Path

from .config import Config
from .environ import Environ
from .options import Options


def test_config_build() -> None:
    options = Options(
        cache_dir=Path('foo/bar'),
        no_store=True,
    )
    environ = Environ(
        read_write=False,
        reddit_private_rss_feed='https://example.rss',
    )
    config = Config.build(options, environ)

    assert config.cache_dir == Path('foo/bar')
    assert config.no_store == True
    assert config.read_only == True
    assert config.reddit_private_rss_feed == 'https://example.rss'
