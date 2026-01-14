from __future__ import annotations

import json
from collections.abc import Generator
from typing import Any, Dict, Optional, Union

import httpx
from pydantic import BaseModel

from ..exceptions import HTTPException
from ..models import *


class SyncClient(BaseModel):
    model_config = {"validate_assignment": True}

    base_url: str = "/"
    verify: Union[bool, str] = True
    access_token: Optional[str] = None

    def get_access_token(self) -> Optional[str]:
        return self.access_token

    def set_access_token(self, value: str) -> None:
        self.access_token = value

    def authenticate_run_authenticate_post(
        self,
        data: AuthenticateRequest,
    ) -> Generator[str | dict[str, Any], None, None]:
        base_url = self.base_url
        path = f"/run/authenticate"

        headers = {
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
            "Authorization": f"Bearer { self.get_access_token() }",
        }

        query_params: Dict[str, Any] = {}
        query_params = {k: v for (k, v) in query_params.items() if v is not None}

        with httpx.Client(base_url=base_url, verify=self.verify) as client:
            with client.stream(
                "post",
                httpx.URL(path),
                headers=headers,
                params=query_params,
                json=data.dict(),
            ) as response:
                if response.status_code != 200:
                    raise HTTPException(
                        response.status_code,
                        f"authenticate_run_authenticate_post failed with status code: {response.status_code}",
                    )

                for line in response.iter_lines():
                    if not line:
                        continue
                    if line.startswith("data:"):
                        payload = line[len("data:") :].strip()
                        if not payload:
                            continue
                        if payload == "[DONE]":
                            break
                        try:
                            obj = json.loads(payload)
                            if isinstance(obj, dict):
                                yield obj
                            else:
                                yield payload
                        except Exception:
                            yield payload
                    else:
                        yield line

    def refresh_run_refresh_post(
        self,
        data: RefreshRequest,
    ) -> Generator[str | dict[str, Any], None, None]:
        base_url = self.base_url
        path = f"/run/refresh"

        headers = {
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
            "Authorization": f"Bearer { self.get_access_token() }",
        }

        query_params: Dict[str, Any] = {}
        query_params = {k: v for (k, v) in query_params.items() if v is not None}

        with httpx.Client(base_url=base_url, verify=self.verify) as client:
            with client.stream(
                "post",
                httpx.URL(path),
                headers=headers,
                params=query_params,
                json=data.dict(),
            ) as response:
                if response.status_code != 200:
                    raise HTTPException(
                        response.status_code,
                        f"refresh_run_refresh_post failed with status code: {response.status_code}",
                    )

                for line in response.iter_lines():
                    if not line:
                        continue
                    if line.startswith("data:"):
                        payload = line[len("data:") :].strip()
                        if not payload:
                            continue
                        if payload == "[DONE]":
                            break
                        try:
                            obj = json.loads(payload)
                            if isinstance(obj, dict):
                                yield obj
                            else:
                                yield payload
                        except Exception:
                            yield payload
                    else:
                        yield line
