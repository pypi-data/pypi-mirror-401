from typing import *

import httpx

from ..api_config import APIConfig, HTTPException
from ..models import *


def get_schema_token_issuer_schema_get(api_config_override: Optional[APIConfig] = None) -> Any:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/token-issuer/schema"

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
            f"get_schema_token_issuer_schema_get failed with status code: {response.status_code}",
        )

    body = None if 200 == 204 else response.json()

    return body


def get_token_issuer__id__get(api_config_override: Optional[APIConfig] = None, *, id: str) -> ManagedTokenIssuer:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/token-issuer/{id}"

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
            f"get_token_issuer__id__get failed with status code: {response.status_code}",
        )

    body = None if 200 == 204 else response.json()

    return ManagedTokenIssuer(**body) if body is not None else ManagedTokenIssuer()


def delete_one_token_issuer__id__delete(api_config_override: Optional[APIConfig] = None, *, id: str) -> None:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/token-issuer/{id}"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer { api_config.get_access_token() }",
    }

    query_params: Dict[str, Any] = {}
    query_params = {key: value for (key, value) in query_params.items() if value is not None}

    with httpx.Client(base_url=base_path, verify=api_config.verify) as client:
        response = client.request(
            "delete",
            httpx.URL(path),
            headers=headers,
            params=query_params,
        )

    if response.status_code != 204:
        raise HTTPException(
            response.status_code,
            f"delete_one_token_issuer__id__delete failed with status code: {response.status_code}",
        )

    body = None if 204 == 204 else response.json()

    return None


def update_token_issuer__id__patch(
    api_config_override: Optional[APIConfig] = None, *, id: str, data: UpdateTokenIssuerRequest
) -> ManagedTokenIssuer:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/token-issuer/{id}"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer { api_config.get_access_token() }",
    }

    query_params: Dict[str, Any] = {}
    query_params = {key: value for (key, value) in query_params.items() if value is not None}

    with httpx.Client(base_url=base_path, verify=api_config.verify) as client:
        response = client.request(
            "patch",
            httpx.URL(path),
            headers=headers,
            params=query_params,
            json=data.dict(),
        )

    if response.status_code != 200:
        raise HTTPException(
            response.status_code,
            f"update_token_issuer__id__patch failed with status code: {response.status_code}",
        )

    body = None if 200 == 204 else response.json()

    return ManagedTokenIssuer(**body) if body is not None else ManagedTokenIssuer()


def create_token_issuer_post(
    api_config_override: Optional[APIConfig] = None, *, data: CreateTokenIssuerRequest
) -> ManagedTokenIssuer:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/token-issuer"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer { api_config.get_access_token() }",
    }

    query_params: Dict[str, Any] = {}
    query_params = {key: value for (key, value) in query_params.items() if value is not None}

    with httpx.Client(base_url=base_path, verify=api_config.verify) as client:
        response = client.request(
            "post",
            httpx.URL(path),
            headers=headers,
            params=query_params,
            json=data.dict(),
        )

    if response.status_code != 200:
        raise HTTPException(
            response.status_code,
            f"create_token_issuer_post failed with status code: {response.status_code}",
        )

    body = None if 200 == 204 else response.json()

    return ManagedTokenIssuer(**body) if body is not None else ManagedTokenIssuer()
