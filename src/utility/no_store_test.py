from .no_store import NoStore


def test_str_and_repr_for_no_store():
    store = NoStore()

    assert str(store) == 'NoStore()'
    assert repr(store) == 'NoStore()'
