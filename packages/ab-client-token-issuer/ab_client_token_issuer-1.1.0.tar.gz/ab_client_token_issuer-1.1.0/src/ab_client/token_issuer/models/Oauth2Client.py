from typing import Annotated, Union

from pydantic import Field

from .PKCEOAuth2Client import PKCEOAuth2Client
from .StandardOAuth2Client import StandardOAuth2Client

Oauth2Client = Annotated[Union[StandardOAuth2Client, PKCEOAuth2Client], Field(discriminator="type")]
