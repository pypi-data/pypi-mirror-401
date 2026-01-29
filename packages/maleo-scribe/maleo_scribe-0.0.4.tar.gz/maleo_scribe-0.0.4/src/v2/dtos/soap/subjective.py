from pydantic import BaseModel, Field
from typing import Annotated, Generic, TypeVar
from nexo.types.string import OptStr, OptStrT
from ....common.mixins.soap import OptOtherInformation
from ....common.mixins.soap.subjective import (
    ChiefComplaint,
    OptAdditionalComplaint,
    OptPainScale,
    OptOnset,
    OptChronology,
    OptLocation,
    OptAggravatingFactor,
    OptRelievingFactor,
    OptPersonalMedicalHistory,
    OptFamilyMedicalHistory,
    OptHabitActivityOccupation,
    OptConsumedMedication,
)


class SubjectiveDTO(
    OptOtherInformation,
    OptConsumedMedication,
    OptHabitActivityOccupation,
    OptFamilyMedicalHistory,
    OptPersonalMedicalHistory,
    OptRelievingFactor,
    OptAggravatingFactor,
    OptLocation,
    OptChronology,
    OptOnset,
    OptPainScale,
    OptAdditionalComplaint,
    ChiefComplaint[OptStrT],
    Generic[OptStrT],
):
    pass


class FlexibleSubjectiveDTO(SubjectiveDTO[OptStr]):
    chief_complaint: Annotated[
        OptStr, Field(None, description="Patient's chief complaint")
    ] = None


class StrictSubjectiveDTO(SubjectiveDTO[str]):
    pass


OptSubjectiveDTO = SubjectiveDTO | None
OptSubjectiveDTOT = TypeVar("OptSubjectiveDTOT", bound=OptSubjectiveDTO)


class SubjectiveDTOMixin(BaseModel, Generic[OptSubjectiveDTOT]):
    subjective: Annotated[OptSubjectiveDTOT, Field(..., description="Subjective")]
