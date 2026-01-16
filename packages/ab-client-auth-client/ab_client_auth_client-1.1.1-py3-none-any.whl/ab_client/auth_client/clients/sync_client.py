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

    def get_login_url_login_get(
        self,
        scope: Optional[str] = None,
        response_type: Optional[str] = None,
        identity_provider: Optional[Union[str, None]] = None,
    ) -> Union[OAuth2AuthorizeResponse, PKCEAuthorizeResponse]:
        base_url = self.base_url
        path = f"/login"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer { self.get_access_token() }",
        }

        query_params: Dict[str, Any] = {
            "scope": scope,
            "response_type": response_type,
            "identity_provider": identity_provider,
        }
        query_params = {k: v for (k, v) in query_params.items() if v is not None}

        with httpx.Client(base_url=base_url, verify=self.verify) as client:
            response = client.request(
                "get",
                httpx.URL(path),
                headers=headers,
                params=query_params,
            )

        if response.status_code != 200:
            raise HTTPException(
                response.status_code,
                f"get_login_url_login_get failed with status code: {response.status_code}",
            )

        body = None if 200 == 204 else response.json()

        return (
            Union[OAuth2AuthorizeResponse, PKCEAuthorizeResponse].model_validate(body)
            if body is not None
            else Union[OAuth2AuthorizeResponse, PKCEAuthorizeResponse]()
        )

    def callback_callback_get(self) -> OAuth2TokenExposed:
        base_url = self.base_url
        path = f"/callback"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer { self.get_access_token() }",
        }

        query_params: Dict[str, Any] = {}
        query_params = {k: v for (k, v) in query_params.items() if v is not None}

        with httpx.Client(base_url=base_url, verify=self.verify) as client:
            response = client.request(
                "get",
                httpx.URL(path),
                headers=headers,
                params=query_params,
            )

        if response.status_code != 200:
            raise HTTPException(
                response.status_code,
                f"callback_callback_get failed with status code: {response.status_code}",
            )

        body = None if 200 == 204 else response.json()

        return OAuth2TokenExposed.model_validate(body) if body is not None else OAuth2TokenExposed()
