from typing import *

from pydantic import BaseModel, Field

from .TokenIssuer import TokenIssuer


class UpdateTokenIssuerRequest(BaseModel):
    """
    UpdateTokenIssuerRequest model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    id: str = Field(validation_alias="id")

    created_by: str = Field(validation_alias="created_by")

    name: str = Field(validation_alias="name")

    token_issuer: TokenIssuer = Field(validation_alias="token_issuer")
