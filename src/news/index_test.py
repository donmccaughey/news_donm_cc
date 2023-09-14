from .index import Index


def test_get_indices_for_term_when_empty():
    index = Index()
    assert index.get_indices_for_term('') == set()


def test_get_indices_for_term_when_not_found():
    terms = {
        'foo': {1, 2, 3},
    }
    index = Index(terms)
    assert index.get_indices_for_term('bar') == set()


def test_get_indices_for_term():
    terms = {
        'foo': {1, 2, 3},
        'bar': {2, 3, 4},
    }
    index = Index(terms)
    assert index.get_indices_for_term('foo') == {1, 2, 3}


def test_search_when_empty():
    index = Index()
    assert index.search('') == set()


def test_search_when_not_found():
    terms = {
        'foo': {1, 2, 3},
        'bar': {2, 3, 4},
    }
    index = Index(terms)
    assert index.search('fnord') == set()


def test_search_for_two_terms():
    terms = {
        'foo': {1, 2, 3},
        'bar': {2, 3, 4},
        'fnord': {3, 4, 5},
    }
    index = Index(terms)
    assert index.search('foo bar') == {2, 3}


def test_search_for_three_terms():
    terms = {
        'foo': {1, 2, 3},
        'bar': {2, 3, 4},
        'fnord': {3, 4, 5},
    }
    index = Index(terms)
    assert index.search('fnord foo bar') == {3}
