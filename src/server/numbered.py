from typing import cast
from flask import redirect, Response

from .resource import Resource
from .views import get_news_response


class Numbered(Resource):
    def get(self, page_number: int):
        if page_number == 1:
            return cast(Response, redirect('/', 308))
        return get_news_response(
            self.cached_news, self.version, self.is_styled, page_number
        )
