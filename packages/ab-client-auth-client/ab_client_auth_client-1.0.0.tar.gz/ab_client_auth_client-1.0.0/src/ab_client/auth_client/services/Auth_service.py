from typing import *

import httpx

from ..api_config import APIConfig, HTTPException
from ..models import *


def get_login_url_login_get(
    api_config_override: Optional[APIConfig] = None,
    *,
    scope: Optional[str] = None,
    response_type: Optional[str] = None,
    identity_provider: Optional[Union[str, None]] = None,
) -> Union[OAuth2AuthorizeResponse, PKCEAuthorizeResponse]:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/login"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer { api_config.get_access_token() }",
    }

    query_params: Dict[str, Any] = {}
    query_params = {key: value for (key, value) in query_params.items() if value is not None}

    with httpx.Client(base_url=base_path, verify=api_config.verify) as client:
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
        Union[OAuth2AuthorizeResponse, PKCEAuthorizeResponse](**body)
        if body is not None
        else Union[OAuth2AuthorizeResponse, PKCEAuthorizeResponse]()
    )


def callback_callback_get(api_config_override: Optional[APIConfig] = None) -> OAuth2TokenExposed:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/callback"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer { api_config.get_access_token() }",
    }

    query_params: Dict[str, Any] = {}
    query_params = {key: value for (key, value) in query_params.items() if value is not None}

    with httpx.Client(base_url=base_path, verify=api_config.verify) as client:
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

    return OAuth2TokenExposed(**body) if body is not None else OAuth2TokenExposed()
