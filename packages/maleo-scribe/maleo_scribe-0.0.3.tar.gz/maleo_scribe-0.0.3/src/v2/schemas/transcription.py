from pydantic import BaseModel, Field
from typing import Annotated


class TranscribeParameter(BaseModel):
    a: Annotated[
        str,
        Field(
            ...,
        ),
    ]
