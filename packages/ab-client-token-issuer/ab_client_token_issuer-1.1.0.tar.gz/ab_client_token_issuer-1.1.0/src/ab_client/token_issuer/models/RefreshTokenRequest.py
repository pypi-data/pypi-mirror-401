from typing import *

from pydantic import BaseModel, Field


class RefreshTokenRequest(BaseModel):
    """
    RefreshTokenRequest model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    refresh_token: str = Field(validation_alias="refresh_token")

    scope: Optional[Union[str, None]] = Field(validation_alias="scope", default=None)
