__version__ = "0.3.0"


from fastapi import FastAPI
from fastapi import routing as origin_routing
from fastapi.dependencies import utils as origin_utils


def setup(app: FastAPI) -> None:
    try:
        from fastapi_extra import _patch
        
        _patch.install_routes(app)
        origin_routing.solve_dependencies.__globals__['is_sequence_field'] = _patch.is_sequence_field # type: ignore
        origin_utils.QueryParams.__init__ = _patch.query_params_init # type: ignore
    except ImportError:  # pragma: nocover
        pass
