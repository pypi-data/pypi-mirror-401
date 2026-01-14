from typing import *
from typing import Literal

from pydantic import BaseModel, Field

from .Oauth2Client import Oauth2Client
from .Oauth2Flow import Oauth2Flow
from .TokenIssuerType import TokenIssuerType


class TemplateTokenIssuer_Output(BaseModel):
    """
    TemplateTokenIssuer model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    oauth2_flow: Oauth2Flow = Field(validation_alias="oauth2_flow")

    oauth2_client: Oauth2Client = Field(validation_alias="oauth2_client")

    identity_provider: Optional[str] = Field(validation_alias="identity_provider", default=None)

    response_type: Optional[str] = Field(validation_alias="response_type", default=None)

    scope: Optional[str] = Field(validation_alias="scope", default=None)

    type: Literal[TokenIssuerType.TEMPLATE] = Field(validation_alias="type", default=TokenIssuerType.TEMPLATE)
