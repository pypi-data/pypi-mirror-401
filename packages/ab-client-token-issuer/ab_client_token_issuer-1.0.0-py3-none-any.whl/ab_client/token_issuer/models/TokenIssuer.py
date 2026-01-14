from typing import Annotated, Union

from pydantic import Field

from .OAuth2TokenIssuer import OAuth2TokenIssuer
from .PKCEOAuth2TokenIssuer import PKCEOAuth2TokenIssuer
from .TemplateTokenIssuer import TemplateTokenIssuer

TokenIssuer = Annotated[
    Union[PKCEOAuth2TokenIssuer, OAuth2TokenIssuer, TemplateTokenIssuer], Field(discriminator="type")
]
