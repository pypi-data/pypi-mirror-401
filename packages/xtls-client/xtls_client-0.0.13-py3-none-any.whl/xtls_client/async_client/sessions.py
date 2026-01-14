import asyncio

from asyncio import Future
from typing import Any, Dict, Optional, Union

from xtls_client import Session
from xtls_client.response import Response


class AsyncSession(Session):

    def execute_request(
            self,
            method: str,
            url: str,
            params: Optional[Dict] = None,
            data: Optional[Union[str, dict]] = None,
            headers: Optional[Dict] = None,
            cookies: Optional[Dict] = None,
            json: Optional[Dict] = None,
            allow_redirects: Optional[bool] = True,
            verify: Optional[bool] = True,
            timeout: Optional[int] = None,
            proxy: Optional[Dict] = None,
            proxies: Optional[Dict] = None,
            stream: Optional[bool] = False,
            chunk_size: Optional[int] = 1024,
    ) -> Future[Response]:
        loop = asyncio.get_running_loop()
        parent_execute_request = super().execute_request
        return loop.run_in_executor(
            None,
            lambda: parent_execute_request(
                method=method,
                url=url,
                params=params,
                data=data,
                headers=headers,
                cookies=cookies,
                json=json,
                allow_redirects=allow_redirects,
                verify=verify,
                timeout=timeout,
                proxy=proxy,
                proxies=proxies,
                stream=stream,
                chunk_size=chunk_size,
            ),
        )

    def get(self, url: str, **kwargs: Any) -> Future[Response]:
        return self.execute_request("GET", url, **kwargs)

    def options(self, url: str, **kwargs: Any) -> Future[Response]:
        return self.execute_request("OPTIONS", url, **kwargs)

    def head(self, url: str, **kwargs: Any) -> Future[Response]:
        kwargs.setdefault("allow_redirects", False)
        return self.execute_request("HEAD", url, **kwargs)

    def post(
        self, url: str, data: Optional[Union[str, dict]] = None, json: Optional[Dict] = None, **kwargs: Any
    ) -> Future[Response]:
        return self.execute_request("POST", url, data=data, json=json, **kwargs)

    def put(
        self, url: str, data: Optional[Union[str, dict]] = None, json: Optional[Dict] = None, **kwargs: Any
    ) -> Future[Response]:
        return self.execute_request("PUT", url, data=data, json=json, **kwargs)

    def patch(
        self, url: str, data: Optional[Union[str, dict]] = None, json: Optional[Dict] = None, **kwargs: Any
    ) -> Future[Response]:
        return self.execute_request("PATCH", url, data=data, json=json, **kwargs)

    def delete(self, url: str, **kwargs: Any) -> Future[Response]:
        return self.execute_request("DELETE", url, **kwargs)
