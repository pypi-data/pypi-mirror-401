from typing import *

from pydantic import BaseModel, Field

from .RefreshTokenRequest import RefreshTokenRequest
from .TokenIssuer import TokenIssuer


class RefreshRequest(BaseModel):
    """
    RefreshRequest model
        Refresh a token, using user provided token issuer.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    refresh_token: RefreshTokenRequest = Field(validation_alias="refresh_token")

    token_issuer: TokenIssuer = Field(validation_alias="token_issuer")
