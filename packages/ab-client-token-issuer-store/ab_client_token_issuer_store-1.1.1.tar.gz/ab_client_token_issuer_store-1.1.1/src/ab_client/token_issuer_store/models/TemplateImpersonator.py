from typing import *
from typing import Literal

from pydantic import BaseModel, Field

from .ImpersonatorTool import ImpersonatorTool


class TemplateImpersonator(BaseModel):
    """
    TemplateImpersonator model
        Automate browser login to capture auth code via OIDC with PKCE.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    tool: Literal[ImpersonatorTool.TEMPLATE] = Field(validation_alias="tool", default=ImpersonatorTool.TEMPLATE)
