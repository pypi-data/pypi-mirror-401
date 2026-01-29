import uuid
from contextvars import ContextVar

_request_id_ctx: ContextVar[str] = ContextVar("request_id", default=None)


def set_request_id(request_id: str = None):
    if request_id is None:
        request_id = str(uuid.uuid4())
    _request_id_ctx.set(request_id)
    return request_id


def get_request_id():
    return _request_id_ctx.get()
