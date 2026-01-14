from typing import *
from typing import Literal

from pydantic import BaseModel, Field

from .Oauth2FlowType import Oauth2FlowType


class TemplateOAuth2Flow(BaseModel):
    """
    TemplateOAuth2Flow model
        Automate browser login to capture auth code via OIDC with PKCE.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    idp_prefix: str = Field(validation_alias="idp_prefix")

    timeout: Optional[Union[int, None]] = Field(validation_alias="timeout", default=None)

    type: Literal[Oauth2FlowType.TEMPLATE] = Field(validation_alias="type", default=Oauth2FlowType.TEMPLATE)
