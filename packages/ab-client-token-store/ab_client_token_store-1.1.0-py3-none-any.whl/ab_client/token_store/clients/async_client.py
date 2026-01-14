from typing import Any, Dict, Optional, Union

import httpx
from pydantic import BaseModel, HttpUrl

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

    async def get_by_connection_oauth2_token_get(
        self,
        created_by: str,
        tenant_id: str,
    ) -> Any:
        base_url = self.base_url
        path = f"/oauth2-token"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer { self.get_access_token() }",
        }

        query_params: Dict[str, Any] = {
            "created_by": created_by,
            "tenant_id": tenant_id,
        }
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
                f"get_by_connection_oauth2_token_get failed with status code: {response.status_code}",
            )

        body = None if 200 == 204 else response.json()
        return body

    async def create_oauth2_token_post(
        self,
        data: CreateOAuth2TokenRequest,
    ) -> Any:
        base_url = self.base_url
        path = f"/oauth2-token"

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

        if response.status_code != 201:
            raise HTTPException(
                response.status_code,
                f"create_oauth2_token_post failed with status code: {response.status_code}",
            )

        body = None if 201 == 204 else response.json()
        return body

    async def delete_by_connection_oauth2_token_delete(
        self,
        created_by: str,
        tenant_id: str,
    ) -> Any:
        base_url = self.base_url
        path = f"/oauth2-token"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer { self.get_access_token() }",
        }

        query_params: Dict[str, Any] = {
            "created_by": created_by,
            "tenant_id": tenant_id,
        }
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
                f"delete_by_connection_oauth2_token_delete failed with status code: {response.status_code}",
            )

        body = None if 204 == 204 else response.json()
        return body

    async def get_one_oauth2_token__id__get(
        self,
        id: str,
    ) -> Any:
        base_url = self.base_url
        path = f"/oauth2-token/{id}"

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
                f"get_one_oauth2_token__id__get failed with status code: {response.status_code}",
            )

        body = None if 200 == 204 else response.json()
        return body

    async def delete_one_oauth2_token__id__delete(
        self,
        id: str,
    ) -> Any:
        base_url = self.base_url
        path = f"/oauth2-token/{id}"

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
                f"delete_one_oauth2_token__id__delete failed with status code: {response.status_code}",
            )

        body = None if 204 == 204 else response.json()
        return body
