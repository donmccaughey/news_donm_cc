from flask import abort, request

from .resource import Resource
from .views import get_news_response, get_search_response


class Home(Resource):
    def get(self):
        if 'q' in request.args:
            if len(request.args['q']) > 32:
                abort(400)
            return get_search_response(
                self.cached_news,
                self.version,
                self.is_styled,
                request.args['q'],
            )
        else:
            return get_news_response(
                self.cached_news, self.version, self.is_styled, 1
            )
