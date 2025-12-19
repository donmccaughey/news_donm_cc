from flask import Response

from .resource import Resource
from .site_doc import SiteDoc


class Site(Resource):
    def get(self, identity: str) -> Response:
        doc = SiteDoc(
            self.cached_news.read(), self.version, self.is_styled, identity
        )
        return self.make_doc_response(doc)
