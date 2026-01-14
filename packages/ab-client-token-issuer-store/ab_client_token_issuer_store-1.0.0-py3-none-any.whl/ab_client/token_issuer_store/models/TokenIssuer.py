from typing import Annotated, Union

from pydantic import Field

from .OAuth2TokenIssuer_Input import OAuth2TokenIssuer_Input
from .PKCEOAuth2TokenIssuer_Input import PKCEOAuth2TokenIssuer_Input
from .TemplateTokenIssuer_Input import TemplateTokenIssuer_Input

TokenIssuer = Annotated[
    Union[PKCEOAuth2TokenIssuer_Input, OAuth2TokenIssuer_Input, TemplateTokenIssuer_Input], Field(discriminator="type")
]
