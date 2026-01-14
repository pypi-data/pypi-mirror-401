from typing import Annotated, Union

from pydantic import Field

from .ImpersonationOAuth2Flow import ImpersonationOAuth2Flow
from .TemplateOAuth2Flow import TemplateOAuth2Flow

Oauth2Flow = Annotated[Union[ImpersonationOAuth2Flow, TemplateOAuth2Flow], Field(discriminator="type")]
