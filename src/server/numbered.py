from typing import cast
from flask import redirect, Response

from .news_resource import NewsResource


class Numbered(NewsResource):
    def get(self, page_number: int) -> Response:
        if page_number == 1:
            return cast(Response, redirect('/', 308))
        return self.get_news(page_number)
