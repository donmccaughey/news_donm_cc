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


def get_terms(query: str) -> list[str]:
    return query.split()
