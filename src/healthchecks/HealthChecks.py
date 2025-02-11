from uuid import UUID

from aiohttp import ClientSession

from .HealthChecksContextManager import HealthChecksContextManager
from .Method import Method


class HealthChecks:
    _http: ClientSession

    _base_url: str | None
    _ping_key: str | None

    def __init__(
        self,
        http: ClientSession,
        base_url: str | None = None,
        ping_key: str | None = None,
    ) -> None:
        self._http = http

        self._base_url = base_url if base_url is not None else "https://hc-ping.com"
        self._ping_key = ping_key

    def ping(
        self,
        uuid: str | None = None,
        slug: str | None = None,
        run_id: UUID | None = None,
        request_method: Method = Method.GET,
    ):
        if uuid is None and slug is None:
            raise ValueError("Either `uuid` or `slug` must be provided")

        if slug and not self._ping_key:
            raise ValueError("`ping_key` must be provided when using `slug`")

        url = f"{self._base_url}/{self._ping_key if self._ping_key else ''}/{uuid if uuid else slug}"  # noqa: E501
        return HealthChecksContextManager(self._http, url, request_method, run_id)
