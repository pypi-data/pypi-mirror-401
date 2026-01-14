from typing import *

from pydantic import BaseModel, Field


class ValidateTokenRequest(BaseModel):
    """
    ValidateTokenRequest model
        Schema for token request.
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    token: str = Field(validation_alias="token")
