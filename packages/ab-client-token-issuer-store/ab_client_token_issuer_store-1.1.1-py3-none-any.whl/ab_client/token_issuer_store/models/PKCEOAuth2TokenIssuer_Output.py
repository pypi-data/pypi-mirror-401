from typing import *
from typing import Literal

from pydantic import BaseModel, Field

from .Oauth2Flow import Oauth2Flow
from .PKCEOAuth2Client import PKCEOAuth2Client
from .TokenIssuerType import TokenIssuerType


class PKCEOAuth2TokenIssuer_Output(BaseModel):
    """
    PKCEOAuth2TokenIssuer model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    oauth2_flow: Oauth2Flow = Field(validation_alias="oauth2_flow")

    oauth2_client: PKCEOAuth2Client = Field(validation_alias="oauth2_client")

    identity_provider: Optional[str] = Field(validation_alias="identity_provider", default=None)

    response_type: Optional[str] = Field(validation_alias="response_type", default=None)

    scope: Optional[str] = Field(validation_alias="scope", default=None)

    type: Literal[TokenIssuerType.PKCE] = Field(validation_alias="type", default=TokenIssuerType.PKCE)
