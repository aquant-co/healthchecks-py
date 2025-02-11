from contextlib import AbstractAsyncContextManager
from traceback import format_tb
from types import TracebackType
from uuid import UUID

from aiohttp import ClientSession

from .Method import Method


class HealthChecksContextManager(
    AbstractAsyncContextManager["HealthChecksContextManager"]
):
    _http: ClientSession
    _ping_body_limit: int
    _failed: bool

    _request_method: Method
    _params: dict[str, str] | None
    _url: str

    def __init__(
        self,
        http: ClientSession,
        url: str,
        request_method: Method,
        run_id: UUID | None = None,
    ):
        self._http = http
        self._ping_body_limit = 0
        self._has_signaled_stop = False

        self._request_method = request_method
        self._params = None
        self._url = url

        if run_id:
            self._params = {"rid": str(run_id)}

    async def fail(self):
        self._has_signaled_stop = True

        async with self._http.request(
            method=self._request_method,
            url=f"{self._url}/fail",
            params=self._params,
        ) as _:
            pass

    async def log(self, log: str):
        # TODO: send only `self._ping_body_limit`

        async with self._http.request(
            method=self._request_method,
            url=f"{self._url}/log",
            params=self._params,
            data=log,
        ) as _:
            pass

    async def exit_code(self, exit_code: int):
        self._has_signaled_stop = True

        async with self._http.request(
            method=self._request_method,
            url=f"{self._url}/{str(exit_code)}",
            params=self._params,
        ) as _:
            pass

    async def start(self):
        async with self._http.request(
            method=self._request_method,
            url=self._url + "/start",
            params=self._params,
        ) as response:
            self._ping_body_limit = int(response.headers.get("Ping-Body-Limit", 0))

    async def stop(self):
        self._has_signaled_stop = True

        async with self._http.request(
            method=self._request_method, url=self._url, params=self._params
        ) as _:
            pass

    async def __aenter__(self):
        await self.start()

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ):
        if not self._has_signaled_stop:
            if exc_type is not None:
                await self.log(str(exc_value) + "\n" + "\n".join(format_tb(traceback)))
                await self.fail()
            else:
                await self.stop()

        return None
