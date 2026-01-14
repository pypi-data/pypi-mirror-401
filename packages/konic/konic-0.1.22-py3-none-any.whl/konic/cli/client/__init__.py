from typing import Any, cast

from konic.cli.client.api_client import KonicAPIClient


class _LazyClient:
    """
    Lazy initialization wrapper for KonicAPIClient.

    This class defers the instantiation of KonicAPIClient until it's first accessed,
    allowing tests to mock the client before it's created and avoiding the need
    for environment variables during module import.
    """

    _instance: KonicAPIClient | None = None

    def _get_client(self) -> KonicAPIClient:
        if self._instance is None:
            self._instance = KonicAPIClient()
        return self._instance

    def set_base_url(self, url: str) -> None:
        self._get_client().set_base_url(url)

    def get_json(self, path: str) -> Any:
        return self._get_client().get_json(path)

    def post_json(self, path: str, data: dict[str, Any] | None = None) -> Any:
        return self._get_client().post_json(path, data)

    def put_json(self, path: str, data: dict[str, Any] | None = None) -> Any:
        return self._get_client().put_json(path, data)

    def delete(self, path: str) -> Any:
        return self._get_client().delete(path)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._get_client(), name)


# Type as KonicAPIClient for static type checking since _LazyClient delegates all methods
client: KonicAPIClient = cast(KonicAPIClient, _LazyClient())

__all__: list[str] = ["KonicAPIClient", "client"]
