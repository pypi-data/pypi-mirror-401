from typing import Optional
from atk_common.interfaces import *
from atk_common.classes import *

_http_response_handler: HttpResponseHandler | None = None

def create_http_response_handler(
    logger: ILogger,
    error_handler: IErrorHandler,
    env_handler: IEnvHandler,
    my_tracer,
    *,
    timeout: Optional[float] = 5.0,
) -> None:
    global _http_response_handler
    _http_response_handler = HttpResponseHandler(
        logger=logger,
        error_handler=error_handler,
        env_handler=env_handler,
        my_tracer=my_tracer,
        timeout=timeout,              # None disables timeout
    )

def get_http_response_handler():
    global _http_response_handler
    if _http_response_handler is None:
        raise ValueError("HttpResponseHandler not initialized. Call create_http_response_handler first.")
    return _http_response_handler
