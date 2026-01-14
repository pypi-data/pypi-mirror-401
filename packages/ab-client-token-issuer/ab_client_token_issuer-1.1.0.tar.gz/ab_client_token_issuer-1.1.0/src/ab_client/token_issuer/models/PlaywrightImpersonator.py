from typing import *
from typing import Literal

from pydantic import BaseModel, Field

from .ImpersonatorTool import ImpersonatorTool


class PlaywrightImpersonator(BaseModel):
    """
    PlaywrightImpersonator model
        Automate browser login to capture auth code via OIDC with PKCE. Good For CLIs, but
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    tool: Literal[ImpersonatorTool.PLAYWRIGHT] = Field(validation_alias="tool", default=ImpersonatorTool.PLAYWRIGHT)

    browser_channel: Optional[str] = Field(validation_alias="browser_channel", default=None)
