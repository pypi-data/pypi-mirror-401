from typing import *

from pydantic import BaseModel, Field


class OAuth2Token(BaseModel):
    """
    OAuth2Token model
        An OAuth2 token model with secrets stored as SecretStr.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    access_token: str = Field(validation_alias="access_token")

    id_token: Optional[Union[str, None]] = Field(validation_alias="id_token", default=None)

    refresh_token: Optional[Union[str, None]] = Field(validation_alias="refresh_token", default=None)

    expires_in: int = Field(validation_alias="expires_in")

    scope: Optional[Union[str, None]] = Field(validation_alias="scope", default=None)

    token_type: str = Field(validation_alias="token_type")
