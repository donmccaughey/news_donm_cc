from .resource import Resource
from .views import get_site_response


class Site(Resource):
    def get(self, identity: str):
        return get_site_response(
            self.cached_news, self.version, self.is_styled, identity
        )
