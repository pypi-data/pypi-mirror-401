from typing import Any, Dict, Optional, Union

import httpx
from pydantic import BaseModel, HttpUrl

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

    def validate_token_validate_post(
        self,
        data: ValidateTokenRequest,
    ) -> Any:
        base_url = self.base_url
        path = f"/validate"

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
                json=data.dict(),
            )

        if response.status_code != 200:
            raise HTTPException(
                response.status_code,
                f"validate_token_validate_post failed with status code: {response.status_code}",
            )

        body = None if 200 == 204 else response.json()
        return body
