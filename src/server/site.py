from .resource import Resource
from .site_doc import SiteDoc
from .views import make_doc_response


class Site(Resource):
    def get(self, identity: str):
        doc = SiteDoc(
            self.cached_news.read(), self.version, self.is_styled, identity
        )
        return make_doc_response(doc)
