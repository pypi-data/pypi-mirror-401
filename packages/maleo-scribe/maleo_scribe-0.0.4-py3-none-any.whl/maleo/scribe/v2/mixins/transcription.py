from pydantic import BaseModel, Field
from typing import Annotated, Generic
from nexo.types.string import OptStrT


class Transcript(BaseModel, Generic[OptStrT]):
    trancript: Annotated[OptStrT, Field(..., description="Transcript")]


class RawTranscript(BaseModel, Generic[OptStrT]):
    raw_trancript: Annotated[OptStrT, Field(..., description="Raw Transcript")]


class RefinedTranscript(BaseModel, Generic[OptStrT]):
    refined_trancript: Annotated[OptStrT, Field(..., description="Refined Transcript")]
