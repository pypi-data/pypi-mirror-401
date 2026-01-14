from typing import *

from pydantic import BaseModel, Field

from .TokenIssuer import TokenIssuer


class ManagedTokenIssuer(BaseModel):
    """
    ManagedTokenIssuer model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    updated_at: str = Field(validation_alias="updated_at")

    created_by: Optional[Union[str, None]] = Field(validation_alias="created_by", default=None)

    created_at: str = Field(validation_alias="created_at")

    id: Optional[str] = Field(validation_alias="id", default=None)

    name: str = Field(validation_alias="name")

    token_issuer: TokenIssuer = Field(validation_alias="token_issuer")
