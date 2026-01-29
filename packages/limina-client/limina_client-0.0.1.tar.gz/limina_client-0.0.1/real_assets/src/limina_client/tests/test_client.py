import pytest

from ..limina_client import LiminaClient


def test_initialization_with_auth():
    client = LiminaClient("http", "localhost", "8080", api_key="test")
    assert client.get.headers["x-api-key"] == "test"
    client = LiminaClient("http", "localhost", "8080", bearer_token="test")
    assert client.get.headers["Authorization"] == "Bearer test"


def test_initialization_error_message():
    with pytest.raises(ValueError) as e:
        client = LiminaClient()

    assert e.match(
        "LiminaClient needs either a url, or a scheme and host to initialize. You can find more information on which url to use here: https://docs.getlimina.ai/client/"
    )
