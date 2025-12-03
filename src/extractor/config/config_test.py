from pathlib import Path

from .config import Config
from .environ import Environ
from .options import Options
from .s3_creds import S3Creds


def test_config_build() -> None:
    options = Options(
        cache_dir=Path('foo/bar'),
        no_store=True,
    )
    environ = Environ(
        read_write=False,
        reddit_private_rss_feed='https://example.rss',
    )
    s3_creds = S3Creds(
        aws_access_key_id='secret-id',
        aws_secret_access_key='secret-key',
        endpoint_url='https://s3.us-east-1.amazonaws.com',
        region_name='us-east-1'
    )
    config = Config.build(options, environ, s3_creds)

    assert config.cache_dir == Path('foo/bar')
    assert config.no_store == True
    assert config.read_only == True
    assert config.reddit_private_rss_feed == 'https://example.rss'
    assert config.s3_creds == s3_creds
