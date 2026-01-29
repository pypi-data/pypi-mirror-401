from pydantic import BaseModel, Field
from typing import Annotated, Generic
from nexo.types.string import OptStr, OptStrT


class Overall(BaseModel, Generic[OptStrT]):
    overall: Annotated[OptStrT, Field(..., description="Overall")]


class OptOtherInformation(BaseModel):
    other_information: Annotated[
        OptStr, Field(None, description="Other information")
    ] = None
