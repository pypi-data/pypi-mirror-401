from typing import *
from typing import Literal

from pydantic import BaseModel, Field

from .Oauth2ClientType import Oauth2ClientType
from .OIDCConfig import OIDCConfig


class StandardOAuth2Client(BaseModel):
    """
    StandardOAuth2Client model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    config: OIDCConfig = Field(validation_alias="config")

    type: Literal[Oauth2ClientType.STANDARD] = Field(validation_alias="type", default=Oauth2ClientType.STANDARD)
