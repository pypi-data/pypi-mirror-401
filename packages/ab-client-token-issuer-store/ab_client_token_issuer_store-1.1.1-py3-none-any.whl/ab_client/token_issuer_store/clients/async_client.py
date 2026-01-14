from __future__ import annotations

import json
from collections.abc import AsyncGenerator
from typing import Any, Dict, Optional, Union

import httpx
from pydantic import BaseModel

from ..exceptions import HTTPException
from ..models import *


class AsyncClient(BaseModel):
    model_config = {"validate_assignment": True}

    base_url: str = "/"
    verify: Union[bool, str] = True
    access_token: Optional[str] = None

    def get_access_token(self) -> Optional[str]:
        return self.access_token

    def set_access_token(self, value: str) -> None:
        self.access_token = value

    async def get_schema_token_issuer_schema_get(self) -> Any:
        base_url = self.base_url
        path = f"/token-issuer/schema"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer { self.get_access_token() }",
        }

        query_params: Dict[str, Any] = {}
        query_params = {k: v for (k, v) in query_params.items() if v is not None}

        async with httpx.AsyncClient(base_url=base_url, verify=self.verify) as client:
            response = await client.request(
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

    async def get_token_issuer__id__get(
        self,
        id: str,
    ) -> ManagedTokenIssuer:
        base_url = self.base_url
        path = f"/token-issuer/{id}"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer { self.get_access_token() }",
        }

        query_params: Dict[str, Any] = {}
        query_params = {k: v for (k, v) in query_params.items() if v is not None}

        async with httpx.AsyncClient(base_url=base_url, verify=self.verify) as client:
            response = await client.request(
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

        return ManagedTokenIssuer.model_validate(body) if body is not None else ManagedTokenIssuer()

    async def delete_one_token_issuer__id__delete(
        self,
        id: str,
    ) -> None:
        base_url = self.base_url
        path = f"/token-issuer/{id}"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer { self.get_access_token() }",
        }

        query_params: Dict[str, Any] = {}
        query_params = {k: v for (k, v) in query_params.items() if v is not None}

        async with httpx.AsyncClient(base_url=base_url, verify=self.verify) as client:
            response = await client.request(
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

    async def update_token_issuer__id__patch(
        self,
        id: str,
        data: UpdateTokenIssuerRequest,
    ) -> ManagedTokenIssuer:
        base_url = self.base_url
        path = f"/token-issuer/{id}"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer { self.get_access_token() }",
        }

        query_params: Dict[str, Any] = {}
        query_params = {k: v for (k, v) in query_params.items() if v is not None}

        async with httpx.AsyncClient(base_url=base_url, verify=self.verify) as client:
            response = await client.request(
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

        return ManagedTokenIssuer.model_validate(body) if body is not None else ManagedTokenIssuer()

    async def create_token_issuer_post(
        self,
        data: CreateTokenIssuerRequest,
    ) -> ManagedTokenIssuer:
        base_url = self.base_url
        path = f"/token-issuer"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer { self.get_access_token() }",
        }

        query_params: Dict[str, Any] = {}
        query_params = {k: v for (k, v) in query_params.items() if v is not None}

        async with httpx.AsyncClient(base_url=base_url, verify=self.verify) as client:
            response = await client.request(
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

        return ManagedTokenIssuer.model_validate(body) if body is not None else ManagedTokenIssuer()
