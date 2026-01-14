from typing import *

from pydantic import BaseModel, Field


class ManagedOAuth2Token(BaseModel):
    """
    ManagedOAuth2Token model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    updated_at: str = Field(validation_alias="updated_at")

    created_by: Optional[Union[str, None]] = Field(validation_alias="created_by", default=None)

    created_at: str = Field(validation_alias="created_at")

    id: Optional[str] = Field(validation_alias="id", default=None)

    name: Optional[Union[str, None]] = Field(validation_alias="name", default=None)

    tenant_id: str = Field(validation_alias="tenant_id")

    access_token: str = Field(validation_alias="access_token")

    id_token: Optional[Union[str, None]] = Field(validation_alias="id_token", default=None)

    refresh_token: Optional[Union[str, None]] = Field(validation_alias="refresh_token", default=None)

    expires_in: int = Field(validation_alias="expires_in")

    scope: Optional[Union[str, None]] = Field(validation_alias="scope", default=None)

    token_type: str = Field(validation_alias="token_type")

    expires_at: Optional[Union[str, None]] = Field(validation_alias="expires_at", default=None)
