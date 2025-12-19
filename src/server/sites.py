from .resource import Resource
from .views import get_sites_response


class Sites(Resource):
    def get(self):
        return get_sites_response(
            self.cached_news, self.version, self.is_styled
        )
