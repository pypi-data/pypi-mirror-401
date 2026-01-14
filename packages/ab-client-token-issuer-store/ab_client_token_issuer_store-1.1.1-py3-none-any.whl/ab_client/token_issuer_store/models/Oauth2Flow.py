from typing import Annotated, Union

from pydantic import Field

from .ImpersonationOAuth2Flow_Input import ImpersonationOAuth2Flow_Input
from .TemplateOAuth2Flow import TemplateOAuth2Flow

Oauth2Flow = Annotated[Union[ImpersonationOAuth2Flow_Input, TemplateOAuth2Flow], Field(discriminator="type")]
