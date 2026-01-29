from pydantic import BaseModel, Field
from typing import Annotated, Generic
from nexo.types.string import OptStrT


class Notes(BaseModel, Generic[OptStrT]):
    notes: Annotated[OptStrT, Field(..., description="Notes")]
