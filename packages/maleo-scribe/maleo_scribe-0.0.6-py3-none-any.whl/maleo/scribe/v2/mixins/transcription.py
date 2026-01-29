from pydantic import BaseModel, Field
from typing import Annotated, Generic
from nexo.types.string import OptStrT


class Transcript(BaseModel, Generic[OptStrT]):
    transcript: Annotated[OptStrT, Field(..., description="Transcript")]


class RawTranscript(BaseModel, Generic[OptStrT]):
    raw_transcript: Annotated[OptStrT, Field(..., description="Raw Transcript")]


class RefinedTranscript(BaseModel, Generic[OptStrT]):
    refined_transcript: Annotated[OptStrT, Field(..., description="Refined Transcript")]
