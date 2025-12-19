from flask import Response

from .resource import Resource
from .sites_doc import SitesDoc


class Sites(Resource):
    def get(self) -> Response:
        doc = SitesDoc(self.cached_news.read(), self.version, self.is_styled)
        return self.make_doc_response(doc)
