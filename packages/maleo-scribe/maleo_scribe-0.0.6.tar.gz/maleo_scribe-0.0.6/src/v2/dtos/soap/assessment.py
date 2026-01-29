from pydantic import BaseModel, Field
from typing import Annotated, Generic, TypeVar
from nexo.types.string import OptStr
from ....common.mixins.soap import Overall


AssessmentOverallT = TypeVar("AssessmentOverallT", bound=OptStr)


class AssessmentDTO(Overall[AssessmentOverallT], Generic[AssessmentOverallT]):
    pass


class FlexibleAssessmentDTO(AssessmentDTO[OptStr]):
    overall: Annotated[OptStr, Field(None, description="Overall")] = None


class StrictAssessmentDTO(AssessmentDTO[str]):
    pass


OptAssessmentDTO = AssessmentDTO | None
OptAssessmentDTOT = TypeVar("OptAssessmentDTOT", bound=OptAssessmentDTO)


class AssessmentDTOMixin(BaseModel, Generic[OptAssessmentDTOT]):
    assessment: Annotated[OptAssessmentDTOT, Field(..., description="Assessment")]
