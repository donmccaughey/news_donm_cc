from .source import Source
from .url import URL


def test_decode_from_str():
    source = Source.decode('https://source.com/1')

    assert source.url == URL('https://source.com/1')
    assert source.site_id == 'hn'


def test_decode_from_dict():
    source = Source.decode({
        'url': 'https://source.com/1',
        'site_id': 'so',
    })

    assert source.url == URL('https://source.com/1')
    assert source.site_id == 'so'
