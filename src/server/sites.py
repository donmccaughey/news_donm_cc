from .resource import Resource
from .sites_doc import SitesDoc
from .views import make_doc_response


class Sites(Resource):
    def get(self):
        doc = SitesDoc(self.cached_news.read(), self.version, self.is_styled)
        return make_doc_response(doc)
