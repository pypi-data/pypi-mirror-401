from typing import *

from pydantic import BaseModel, Field


class UpsertByOIDCRequest(BaseModel):
    """
    UpsertByOIDCRequest model
        Request model for creating or updating a user based on OIDC information.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    oidc_sub: str = Field(validation_alias="oidc_sub")

    oidc_iss: str = Field(validation_alias="oidc_iss")

    email: Optional[Union[str, None]] = Field(validation_alias="email", default=None)

    display_name: Optional[Union[str, None]] = Field(validation_alias="display_name", default=None)

    preferred_username: Optional[Union[str, None]] = Field(validation_alias="preferred_username", default=None)
