from typing import *

from pydantic import BaseModel, Field

from .TokenIssuer import TokenIssuer


class CreateTokenIssuerRequest(BaseModel):
    """
    CreateTokenIssuerRequest model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    created_by: str = Field(validation_alias="created_by")

    name: str = Field(validation_alias="name")

    token_issuer: TokenIssuer = Field(validation_alias="token_issuer")
