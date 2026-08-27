"""HTTP API client for Constrafor streams."""

from __future__ import annotations

from typing import Any

import requests
from hotglue_singer_sdk.authenticators import APIKeyAuthenticator
from hotglue_singer_sdk.streams import RESTStream
from typing_extensions import override

BASE_URL = "https://api.constrafor.com/public_api/v1"
INCREMENTAL_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


class ConstraforStream(RESTStream):
    """Base Constrafor API stream."""

    @override
    @property
    def url_base(self) -> str:
        return BASE_URL

    @override
    @property
    def authenticator(self) -> APIKeyAuthenticator:
        return APIKeyAuthenticator(
            stream=self,
            key="Authorization",
            value=f"Api-Key {self.config['api_key']}",
            location="header",
        )

    @override
    @property
    def http_headers(self) -> dict[str, str]:
        return {"Accept": "application/json"}

    @override
    def get_next_page_token(
        self,
        response: requests.Response,
        previous_token: Any | None,
    ) -> Any | None:
        return None
