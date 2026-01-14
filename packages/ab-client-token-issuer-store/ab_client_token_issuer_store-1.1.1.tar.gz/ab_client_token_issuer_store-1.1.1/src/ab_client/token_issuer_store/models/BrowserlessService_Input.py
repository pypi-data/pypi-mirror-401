from typing import *

from pydantic import BaseModel, Field


class BrowserlessService_Input(BaseModel):
    """
    BrowserlessService model
        A minimal client for Browserless's session API.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    base_url: str = Field(validation_alias="base_url")
