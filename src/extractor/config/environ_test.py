from unittest.mock import patch
from pytest import raises

from .environ import _environ_is_true, Environ, os


def test_environ_read() -> None:
    # missing all keys
    with patch.dict('os.environ', {}):
        with raises(KeyError):
            Environ.read()

    # missing boolean keys
    values = {
        'REDDIT_PRIVATE_RSS_FEED': 'https://reddit.com/rss',
    }
    with patch.dict('os.environ', values):
        environ = Environ.read()
        assert environ.reddit_private_rss_feed == 'https://reddit.com/rss'
        assert environ.read_write == False

    # all keys present
    values = {
        'EXTRACTOR_READ_WRITE': 'yes',
        'REDDIT_PRIVATE_RSS_FEED': 'https://reddit.com/rss',
    }
    with patch.dict('os.environ', values):
        environ = Environ.read()
        assert environ.reddit_private_rss_feed == 'https://reddit.com/rss'
        assert environ.read_write == True


def test_environ_is_true() -> None:
    # false values

    with patch.dict('os.environ', {}):
        assert not _environ_is_true('FOO')

    with patch.dict('os.environ', {'FOO': 'false'}):
        assert not _environ_is_true('FOO')

    with patch.dict('os.environ', {'FOO': 'no'}):
        assert not _environ_is_true('FOO')

    with patch.dict('os.environ', {'FOO': '0'}):
        assert not _environ_is_true('FOO')

    with patch.dict('os.environ', {'FOO': '2'}):
        assert not _environ_is_true('FOO')

    with patch.dict('os.environ', {'FOO': 'bar'}):
        assert not _environ_is_true('FOO')

    # true values

    with patch.dict('os.environ', {'FOO': 'true'}):
        assert _environ_is_true('FOO')

    with patch.dict('os.environ', {'FOO': 'yes'}):
        assert _environ_is_true('FOO')

    with patch.dict('os.environ', {'FOO': '1'}):
        assert _environ_is_true('FOO')
