from typing import *

from pydantic import BaseModel, Field


class PKCEAuthorizeResponse(BaseModel):
    """
    PKCEAuthorizeResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    url: str = Field(validation_alias="url")

    state: str = Field(validation_alias="state")

    code_verifier: str = Field(validation_alias="code_verifier")

    code_challenge: str = Field(validation_alias="code_challenge")

    code_challenge_method: str = Field(validation_alias="code_challenge_method")
