from typing import *

from pydantic import BaseModel, Field

from .OAuth2Token import OAuth2Token


class CreateOAuth2TokenRequest(BaseModel):
    """
    CreateOAuth2TokenRequest model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    created_by: str = Field(validation_alias="created_by")

    tenant_id: str = Field(validation_alias="tenant_id")

    name: Optional[Union[str, None]] = Field(validation_alias="name", default=None)

    oauth2_token: OAuth2Token = Field(validation_alias="oauth2_token")

    expires_at: Optional[Union[str, None]] = Field(validation_alias="expires_at", default=None)
