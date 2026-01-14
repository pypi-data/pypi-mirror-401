from typing import Annotated, Union

from pydantic import Field

from .PlaywrightCDPBrowserlessImpersonator_Input import PlaywrightCDPBrowserlessImpersonator_Input
from .PlaywrightCDPImpersonator import PlaywrightCDPImpersonator
from .PlaywrightImpersonator import PlaywrightImpersonator
from .TemplateImpersonator import TemplateImpersonator

Impersonator = Annotated[
    Union[
        PlaywrightImpersonator,
        PlaywrightCDPImpersonator,
        PlaywrightCDPBrowserlessImpersonator_Input,
        TemplateImpersonator,
    ],
    Field(discriminator="tool"),
]
