from typing import *

from pydantic import BaseModel, Field


class OAuth2AuthorizeResponse(BaseModel):
    """
    OAuth2AuthorizeResponse model
    """

    model_config = {"populate_by_name": True, "validate_assignment": True}

    url: str = Field(validation_alias="url")

    state: str = Field(validation_alias="state")
