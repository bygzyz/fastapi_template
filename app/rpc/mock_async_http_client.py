import sys

from omi_async_http_client import APIClient as omi_api_client_builder
from fastapi.testclient import TestClient

from app.rpc.mock_test_client_backend import \
    MockTestClientBackend
from app.core.config import settings

sys.path.append("../")


def mock_rpc_api_client_builder(
        model,
        http_backend=None,
        resource_endpoint=settings.API_V1_STR + "/mock",
        client_id="",
        client_secret=""
):
    if isinstance(http_backend, str):
        pass
    else:
        from business.bootstrap import app
        http_backend = MockTestClientBackend(TestClient(app))

    return omi_api_client_builder(
        model=model,
        http_backend=http_backend,
        resource_endpoint=resource_endpoint,
        client_id=client_id,
        client_secret=client_secret,
    )


APIClient = mock_rpc_api_client_builder
