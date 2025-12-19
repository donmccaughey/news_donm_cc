from flask import abort, request, Response

from .news_doc import NewsDoc
from .resource import Resource
from .search_doc import SearchDoc


class NewsResource(Resource):
    def get_news(self, page_number: int) -> Response:
        doc = NewsDoc(
            self.cached_news.read(),
            self.version,
            self.is_styled,
            request.accept_mimetypes,
            page_number,
        )
        if not doc.page.is_valid:
            abort(404)
        return self.make_doc_response(doc)

    def get_search(self, query: str):
        doc = SearchDoc(
            self.cached_news.read(), self.version, self.is_styled, query
        )
        return self.make_doc_response(doc)
