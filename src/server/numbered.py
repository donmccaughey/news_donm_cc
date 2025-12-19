from .resource import Resource
from .views import get_numbered_response


class Numbered(Resource):
    def get(self, page_number: int):
        return get_numbered_response(
            self.cached_news, self.version, self.is_styled, page_number
        )
