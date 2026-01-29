from pydantic import BaseModel, Field
from typing import Annotated, Generic
from nexo.types.integer import OptInt
from nexo.types.string import OptStr, OptStrT


class ChiefComplaint(BaseModel, Generic[OptStrT]):
    chief_complaint: Annotated[
        OptStrT, Field(..., description="Patient's chief complaint")
    ]


class OptAdditionalComplaint(BaseModel):
    additional_complaint: Annotated[
        OptStr, Field(None, description="Patient's additional complaint")
    ] = None


class CombinedComplaint(BaseModel, Generic[OptStrT]):
    combined_complaint: Annotated[
        OptStrT, Field(..., description="Patient's combined complaint")
    ]


class OptPainScale(BaseModel):
    pain_scale: Annotated[
        OptInt, Field(None, description="Patient's pain scale", ge=1, le=10)
    ] = None


class OptOnset(BaseModel):
    onset: Annotated[OptStr, Field(None, description="Patient's onset")] = None


class OptChronology(BaseModel):
    chronology: Annotated[OptStr, Field(None, description="Patient's chronology")] = (
        None
    )


class OptLocation(BaseModel):
    location: Annotated[OptStr, Field(None, description="Patient's location")] = None


class OptFactors(BaseModel):
    factors: Annotated[OptStr, Field(None, description="Patient's factors")] = None


class OptAggravatingFactor(BaseModel):
    aggravating_factor: Annotated[
        OptStr, Field(None, description="Patient's aggravating factor")
    ] = None


class OptAggravatingFactors(BaseModel):
    aggravating_factors: Annotated[
        OptStr, Field(None, description="Patient's aggravating factors")
    ] = None


class OptRelievingFactor(BaseModel):
    relieving_factor: Annotated[
        OptStr, Field(None, description="Patient's relieving factor")
    ] = None


class OptRelievingFactors(BaseModel):
    relieving_factors: Annotated[
        OptStr, Field(None, description="Patient's relieving factors")
    ] = None


class OptPersonalMedicalHistory(BaseModel):
    personal_medical_history: Annotated[
        OptStr, Field(None, description="Patient's personal medical history")
    ] = None


class OptFamilyMedicalHistory(BaseModel):
    family_medical_history: Annotated[
        OptStr, Field(None, description="Patient's family medical history")
    ] = None


class OptPastIllnessHistory(BaseModel):
    past_illness_history: Annotated[
        OptStr, Field(None, description="Patient's past illness history")
    ] = None


class OptFamilyIllnessHistory(BaseModel):
    family_illness_history: Annotated[
        OptStr, Field(None, description="Patient's family illness history")
    ] = None


class OptHabitActivityOccupation(BaseModel):
    habit_activity_occupation: Annotated[
        OptStr, Field(None, description="Patient's habit activity occupation")
    ] = None


class OptConsumedMedication(BaseModel):
    consumed_medication: Annotated[
        OptStr, Field(None, description="Patient's consumed medication")
    ] = None
