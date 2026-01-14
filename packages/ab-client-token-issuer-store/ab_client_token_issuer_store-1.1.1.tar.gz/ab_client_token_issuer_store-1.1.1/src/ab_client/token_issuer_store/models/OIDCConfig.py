from typing import *

from pydantic import BaseModel, Field


class OIDCConfig(BaseModel):
    """
    OIDCConfig model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    client_id: str = Field(validation_alias="client_id")

    client_secret: Optional[Union[str, None]] = Field(validation_alias="client_secret", default=None)

    redirect_uri: str = Field(validation_alias="redirect_uri")

    authorize_url: str = Field(validation_alias="authorize_url")

    token_url: str = Field(validation_alias="token_url")
