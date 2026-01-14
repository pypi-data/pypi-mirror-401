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

    def get_user_by_id_user__user_id__get(
        self,
        user_id: str,
    ) -> User:
        base_url = self.base_url
        path = f"/user/{user_id}"

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
                f"get_user_by_id_user__user_id__get failed with status code: {response.status_code}",
            )

        body = None if 200 == 204 else response.json()

        return User.model_validate(body) if body is not None else User()

    def get_user_by_oidc_user_oidc_get(
        self,
        oidc_sub: str,
        oidc_iss: str,
    ) -> User:
        base_url = self.base_url
        path = f"/user/oidc"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer { self.get_access_token() }",
        }

        query_params: Dict[str, Any] = {
            "oidc_sub": oidc_sub,
            "oidc_iss": oidc_iss,
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
                f"get_user_by_oidc_user_oidc_get failed with status code: {response.status_code}",
            )

        body = None if 200 == 204 else response.json()

        return User.model_validate(body) if body is not None else User()

    def upsert_user_by_oidc_user_oidc_put(
        self,
        data: UpsertByOIDCRequest,
    ) -> User:
        base_url = self.base_url
        path = f"/user/oidc"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer { self.get_access_token() }",
        }

        query_params: Dict[str, Any] = {}
        query_params = {k: v for (k, v) in query_params.items() if v is not None}

        with httpx.Client(base_url=base_url, verify=self.verify) as client:
            response = client.request(
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

        return User.model_validate(body) if body is not None else User()

    def seen_user_user__user_id__seen_post(
        self,
        user_id: str,
    ) -> User:
        base_url = self.base_url
        path = f"/user/{user_id}/seen"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer { self.get_access_token() }",
        }

        query_params: Dict[str, Any] = {}
        query_params = {k: v for (k, v) in query_params.items() if v is not None}

        with httpx.Client(base_url=base_url, verify=self.verify) as client:
            response = client.request(
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

        return User.model_validate(body) if body is not None else User()
