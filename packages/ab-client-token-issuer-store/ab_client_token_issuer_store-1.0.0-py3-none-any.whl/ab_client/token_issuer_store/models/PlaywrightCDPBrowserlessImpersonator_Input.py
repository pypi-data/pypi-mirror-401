from typing import *
from typing import Literal

from pydantic import BaseModel, Field

from .BrowserlessService_Input import BrowserlessService_Input
from .CDPGUIService import CDPGUIService
from .ImpersonatorTool import ImpersonatorTool


class PlaywrightCDPBrowserlessImpersonator_Input(BaseModel):
    """
    PlaywrightCDPBrowserlessImpersonator model
        Automate browser login to capture auth code via OIDC with PKCE. Good For CLIs, but
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    tool: Literal[ImpersonatorTool.PLAYWRIGHT_CDP_BROWSERLESS] = Field(
        validation_alias="tool", default=ImpersonatorTool.PLAYWRIGHT_CDP_BROWSERLESS
    )

    cdp_endpoint: str = Field(validation_alias="cdp_endpoint")

    cdp_headers: Optional[Union[Dict[str, Any], None]] = Field(validation_alias="cdp_headers", default=None)

    cdp_timeout: Optional[Union[float, None]] = Field(validation_alias="cdp_timeout", default=None)

    cdp_gui_service: Optional[Union[CDPGUIService, None]] = Field(validation_alias="cdp_gui_service", default=None)

    browserless_service: BrowserlessService_Input = Field(validation_alias="browserless_service")
