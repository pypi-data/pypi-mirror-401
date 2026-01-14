from typing import *

import httpx

from ..api_config import APIConfig, HTTPException
from ..models import *


async def get_by_connection_oauth2_token_get(
    api_config_override: Optional[APIConfig] = None, *, created_by: str, tenant_id: str
) -> ManagedOAuth2Token:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/oauth2-token"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer { api_config.get_access_token() }",
    }

    query_params: Dict[str, Any] = {}
    query_params = {key: value for (key, value) in query_params.items() if value is not None}

    async with httpx.AsyncClient(base_url=base_path, verify=api_config.verify) as client:
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

    return ManagedOAuth2Token(**body) if body is not None else ManagedOAuth2Token()


async def create_oauth2_token_post(
    api_config_override: Optional[APIConfig] = None, *, data: CreateOAuth2TokenRequest
) -> ManagedOAuth2Token:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/oauth2-token"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer { api_config.get_access_token() }",
    }

    query_params: Dict[str, Any] = {}
    query_params = {key: value for (key, value) in query_params.items() if value is not None}

    async with httpx.AsyncClient(base_url=base_path, verify=api_config.verify) as client:
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

    return ManagedOAuth2Token(**body) if body is not None else ManagedOAuth2Token()


async def delete_by_connection_oauth2_token_delete(
    api_config_override: Optional[APIConfig] = None, *, created_by: str, tenant_id: str
) -> None:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/oauth2-token"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer { api_config.get_access_token() }",
    }

    query_params: Dict[str, Any] = {}
    query_params = {key: value for (key, value) in query_params.items() if value is not None}

    async with httpx.AsyncClient(base_url=base_path, verify=api_config.verify) as client:
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

    return None


async def get_one_oauth2_token__id__get(
    api_config_override: Optional[APIConfig] = None, *, id: str
) -> ManagedOAuth2Token:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/oauth2-token/{id}"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer { api_config.get_access_token() }",
    }

    query_params: Dict[str, Any] = {}
    query_params = {key: value for (key, value) in query_params.items() if value is not None}

    async with httpx.AsyncClient(base_url=base_path, verify=api_config.verify) as client:
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

    return ManagedOAuth2Token(**body) if body is not None else ManagedOAuth2Token()


async def delete_one_oauth2_token__id__delete(api_config_override: Optional[APIConfig] = None, *, id: str) -> None:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/oauth2-token/{id}"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer { api_config.get_access_token() }",
    }

    query_params: Dict[str, Any] = {}
    query_params = {key: value for (key, value) in query_params.items() if value is not None}

    async with httpx.AsyncClient(base_url=base_path, verify=api_config.verify) as client:
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

    return None
