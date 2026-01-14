from typing import Annotated, Union

from pydantic import Field

from .PlaywrightCDPBrowserlessImpersonator import PlaywrightCDPBrowserlessImpersonator
from .PlaywrightCDPImpersonator import PlaywrightCDPImpersonator
from .PlaywrightImpersonator import PlaywrightImpersonator
from .TemplateImpersonator import TemplateImpersonator

Impersonator = Annotated[
    Union[
        PlaywrightImpersonator, PlaywrightCDPImpersonator, PlaywrightCDPBrowserlessImpersonator, TemplateImpersonator
    ],
    Field(discriminator="tool"),
]
