from .method import method
from .request import Request
from .resource import Resource
from .response import Response


def test_no_methods() -> None:
    assert Resource.allow() == []
    assert Resource.methods() == []


def test_with_methods() -> None:
    class MyResource(Resource):
        @method
        def get(self, request: Request) -> Response:
            return Response(
                status_code=200,
                reason_phrase='OK',
                headers={'Content-Type': 'text/plain'},
                body='foobar',
            )

        @method
        def delete(self, request: Request) -> Response:
            return Response(
                status_code=200,
                reason_phrase='OK',
                headers={},
                body='',
            )

        def helper(self) -> None:
            pass

    assert MyResource.allow() == ['DELETE', 'GET']

    methods = MyResource.methods()
    assert len(methods) == 2

    assert callable(methods[0])
    assert methods[0].__name__ == 'delete'

    assert callable(methods[1])
    assert methods[1].__name__ == 'get'
