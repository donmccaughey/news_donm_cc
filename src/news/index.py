import re
import unicodedata
from collections import defaultdict

from news import Item


class Index:
    def __init__(self, terms: dict[str, set[int]] | None = None):
        self.terms = terms or defaultdict(set)

    @staticmethod
    def from_ordered_items(ordered_items: list[Item]) -> 'Index':
        terms = defaultdict(set)
        for i, item in enumerate(ordered_items):
            for term in get_terms(item.title):
                terms[term].add(i)
        return Index(terms)

    def get_indices_for_term(self, term: str) -> set[int]:
        return self.terms.get(term, set())

    def search(self, query: str) -> set[int]:
        terms = get_terms(query)
        matches = [self.get_indices_for_term(term) for term in terms]
        return set.intersection(*matches) if matches else set()


NON_TERMS = {
    'a',
    'an',
    'and',

    'not',

    'or',

    's',

    't',
    'the',
}
TERM = re.compile(r'\b\w+\b')


def get_terms(query: str) -> set[str]:
    query = query.lower()
    query = strip_accents(query)
    terms = TERM.findall(query)
    return set(terms) - NON_TERMS


def strip_accents(text: str) -> str:
    return ''.join(
        ch for ch in unicodedata.normalize('NFD', text)
        if unicodedata.category(ch) != 'Mn'
    )
