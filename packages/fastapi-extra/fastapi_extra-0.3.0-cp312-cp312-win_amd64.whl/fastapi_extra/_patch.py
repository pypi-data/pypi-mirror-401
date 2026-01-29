__author__ = "ziyan.yin"
__date__ = "2026-01-13"


from fastapi import FastAPI
from fastapi._compat import v2
from starlette import datastructures

from fastapi_extra import routing
from fastapi_extra.urlparse import parse_qsl


def install_routes(app: FastAPI) -> None:
    routing.install(app)


def is_sequence_field(field: v2.ModelField) -> bool:
    if not hasattr(field, "_is_sequence"):
        setattr(field, "_is_sequence", v2.is_sequence_field(field))
    return getattr(field, "_is_sequence")


def query_params_init(obj: datastructures.QueryParams, *args, **kwargs) -> None:
    value = args[0] if args else []

    if isinstance(value, bytes):
        super(datastructures.QueryParams, obj).__init__(parse_qsl(value, keep_blank_values=True), **kwargs)
    elif isinstance(value, str):
        super(datastructures.QueryParams, obj).__init__(parse_qsl(value.encode("latin-1"), keep_blank_values=True), **kwargs)
    else:
        super(datastructures.QueryParams, obj).__init__(*args, **kwargs)  # type: ignore[arg-type]
        obj._list = [(str(k), str(v)) for k, v in obj._list]
        obj._dict = {str(k): str(v) for k, v in obj._dict.items()}
