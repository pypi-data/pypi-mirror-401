from typing import *

from pydantic import BaseModel, Field


class CDPGUIService(BaseModel):
    """
    CDPGUIService model
        A minimal client for Browserless&#39;s session API.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    base_url: str = Field(validation_alias="base_url")
