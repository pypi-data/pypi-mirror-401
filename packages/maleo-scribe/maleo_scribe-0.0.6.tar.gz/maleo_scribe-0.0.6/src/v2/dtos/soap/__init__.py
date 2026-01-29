from pydantic import BaseModel, Field
from typing import Annotated, Generic, TypeVar
from .subjective import (
    StrictSubjectiveDTO,
    FlexibleSubjectiveDTO,
    OptSubjectiveDTOT,
    SubjectiveDTOMixin,
)
from .objective import (
    StrictObjectiveDTO,
    FlexibleObjectiveDTO,
    OptObjectiveDTOT,
    ObjectiveDTOMixin,
)
from .assessment import (
    StrictAssessmentDTO,
    FlexibleAssessmentDTO,
    OptAssessmentDTOT,
    AssessmentDTOMixin,
)
from .plan import StrictPlanDTO, FlexiblePlanDTO, OptPlanDTOT, PlanDTOMixin


class SOAPDTO(
    PlanDTOMixin[OptPlanDTOT],
    AssessmentDTOMixin[OptAssessmentDTOT],
    ObjectiveDTOMixin[OptObjectiveDTOT],
    SubjectiveDTOMixin[OptSubjectiveDTOT],
    Generic[
        OptSubjectiveDTOT,
        OptObjectiveDTOT,
        OptAssessmentDTOT,
        OptPlanDTOT,
    ],
):
    pass


OptSOAPDTO = SOAPDTO | None
OptSOAPDTOT = TypeVar("OptSOAPDTOT", bound=OptSOAPDTO)


class FlexibleSOAPDTO(
    SOAPDTO[
        FlexibleSubjectiveDTO | None,
        FlexibleObjectiveDTO | None,
        FlexibleAssessmentDTO | None,
        FlexiblePlanDTO | None,
    ]
):
    subjective: Annotated[
        FlexibleSubjectiveDTO | None, Field(None, description="Subjective")
    ] = None
    objective: Annotated[
        FlexibleObjectiveDTO | None, Field(None, description="Objective")
    ] = None
    assessment: Annotated[
        FlexibleAssessmentDTO | None, Field(None, description="Assessment")
    ] = None
    plan: Annotated[FlexiblePlanDTO | None, Field(None, description="Plan")] = None


class StrictSOAPDTO(
    SOAPDTO[
        StrictSubjectiveDTO,
        StrictObjectiveDTO,
        StrictAssessmentDTO,
        StrictPlanDTO,
    ]
):
    pass


class SOAPDTOMixin(BaseModel, Generic[OptSOAPDTOT]):
    soap: Annotated[OptSOAPDTOT, Field(..., description="SOAP")]
