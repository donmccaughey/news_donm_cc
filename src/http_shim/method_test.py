from .method import method
from .request import Request
from .resource import Resource
from .response import Response


def test_method() -> None:
    class MyResource(Resource):
        @method
        def get(self, request: Request, page: int) -> Response:
            return Response(
                status_code=200,
                reason_phrase='OK',
                headers={'Content-Type': 'text/plain'},
                body=f'{page}',
            )

        def not_a_method(self):
            pass

    assert getattr(MyResource.get, 'http_shim.method', None) == 'GET'
    assert getattr(MyResource.not_a_method, 'http_shim.method', None) is None
