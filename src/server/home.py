from flask import abort, request, Response

from .news_resource import NewsResource


class Home(NewsResource):
    def get(self) -> Response:
        if 'q' in request.args:
            if len(request.args['q']) > 32:
                abort(400)
            return self.get_search(request.args['q'])
        else:
            return self.get_news(1)
