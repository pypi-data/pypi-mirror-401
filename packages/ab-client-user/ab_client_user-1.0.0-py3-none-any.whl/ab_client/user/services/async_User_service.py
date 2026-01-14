from typing import *

import httpx

from ..api_config import APIConfig, HTTPException
from ..models import *


async def get_user_by_id_user__user_id__get(api_config_override: Optional[APIConfig] = None, *, user_id: str) -> User:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/user/{user_id}"

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
            f"get_user_by_id_user__user_id__get failed with status code: {response.status_code}",
        )

    body = None if 200 == 204 else response.json()

    return User(**body) if body is not None else User()


async def get_user_by_oidc_user_oidc_get(
    api_config_override: Optional[APIConfig] = None, *, oidc_sub: str, oidc_iss: str
) -> User:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/user/oidc"

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
            f"get_user_by_oidc_user_oidc_get failed with status code: {response.status_code}",
        )

    body = None if 200 == 204 else response.json()

    return User(**body) if body is not None else User()


async def upsert_user_by_oidc_user_oidc_put(
    api_config_override: Optional[APIConfig] = None, *, data: UpsertByOIDCRequest
) -> User:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/user/oidc"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer { api_config.get_access_token() }",
    }

    query_params: Dict[str, Any] = {}
    query_params = {key: value for (key, value) in query_params.items() if value is not None}

    async with httpx.AsyncClient(base_url=base_path, verify=api_config.verify) as client:
        response = await client.request(
            "put",
            httpx.URL(path),
            headers=headers,
            params=query_params,
            json=data.dict(),
        )

    if response.status_code != 200:
        raise HTTPException(
            response.status_code,
            f"upsert_user_by_oidc_user_oidc_put failed with status code: {response.status_code}",
        )

    body = None if 200 == 204 else response.json()

    return User(**body) if body is not None else User()


async def seen_user_user__user_id__seen_post(api_config_override: Optional[APIConfig] = None, *, user_id: str) -> User:
    api_config = api_config_override if api_config_override else APIConfig()

    base_path = api_config.base_path
    path = f"/user/{user_id}/seen"

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
        )

    if response.status_code != 200:
        raise HTTPException(
            response.status_code,
            f"seen_user_user__user_id__seen_post failed with status code: {response.status_code}",
        )

    body = None if 200 == 204 else response.json()

    return User(**body) if body is not None else User()
