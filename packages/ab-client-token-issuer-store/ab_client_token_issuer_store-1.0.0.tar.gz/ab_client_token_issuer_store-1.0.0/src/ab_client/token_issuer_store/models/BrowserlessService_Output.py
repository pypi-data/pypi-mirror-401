from typing import *

from pydantic import BaseModel, Field


class BrowserlessService_Output(BaseModel):
    """
    BrowserlessService model
        A minimal client for Browserless&#39;s session API.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    base_url: str = Field(validation_alias="base_url")

    sessions_url: str = Field(validation_alias="sessions_url")

    ws_url_prefix: str = Field(validation_alias="ws_url_prefix")
