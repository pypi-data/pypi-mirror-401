from typing import *

from pydantic import BaseModel, Field

from .TokenIssuer import TokenIssuer


class AuthenticateRequest(BaseModel):
    """
    AuthenticateRequest model
        Generate a token, using user provided token issuer.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    token_issuer: TokenIssuer = Field(validation_alias="token_issuer")
