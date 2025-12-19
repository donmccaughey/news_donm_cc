from .resource import Resource
from .views import get_home_response


class Home(Resource):
    def get(self):
        return get_home_response(self.cached_news, self.version, self.is_styled)
