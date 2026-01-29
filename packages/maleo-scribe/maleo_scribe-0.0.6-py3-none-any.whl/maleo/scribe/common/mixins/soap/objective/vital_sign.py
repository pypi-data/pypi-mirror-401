from pydantic import BaseModel, Field
from typing import Annotated
from nexo.types.integer import OptInt
from nexo.types.float import OptFloat
from nexo.types.string import OptStr


class OptSystole(BaseModel):
    systole: Annotated[OptInt, Field(None, description="Patient's systole", ge=1)] = (
        None
    )


class OptSystolicBloodPressure(BaseModel):
    systolic_blood_pressure: Annotated[
        OptInt, Field(None, description="Patient's systolic blood pressure", ge=1)
    ] = None


class OptDiastole(BaseModel):
    diastole: Annotated[OptInt, Field(None, description="Patient's diastole", ge=1)] = (
        None
    )


class OptDiastolicBloodPressure(BaseModel):
    diastolic_blood_pressure: Annotated[
        OptInt, Field(None, description="Patient's diastolic blood pressure", ge=1)
    ] = None


class OptTemperature(BaseModel):
    temperature: Annotated[
        OptFloat, Field(None, description="Patient's temperature", ge=1)
    ] = None


class OptRespirationRate(BaseModel):
    respiration_rate: Annotated[
        OptInt, Field(None, description="Patient's respiration rate", ge=1)
    ] = None


class OptHeartRate(BaseModel):
    heart_rate: Annotated[
        OptInt, Field(None, description="Patient's heart rate", ge=1)
    ] = None


class OptOxygenSaturation(BaseModel):
    oxygen_saturation: Annotated[
        OptInt, Field(None, description="Patient's oxygen saturation", le=100)
    ] = None


class OptAbdominalCircumference(BaseModel):
    abdominal_circumference: Annotated[
        OptFloat, Field(None, description="Patient's abdominal circumference")
    ] = None


class OptWaistCircumference(BaseModel):
    waist_circumference: Annotated[
        OptFloat, Field(None, description="Patient's waist circumference")
    ] = None


class OptWeight(BaseModel):
    weight: Annotated[OptFloat, Field(None, description="Patient's weight", ge=0.0)] = (
        None
    )


class OptHeight(BaseModel):
    height: Annotated[OptFloat, Field(None, description="Patient's height", ge=0.0)] = (
        None
    )


class OptBodyMassIndex(BaseModel):
    body_mass_index: Annotated[
        OptFloat, Field(None, description="Patient's body mass index", ge=0.0)
    ] = None


class OptOrganExaminationDetail(BaseModel):
    organ_examination_detail: Annotated[
        OptStr, Field(None, description="Patient's organ examination details")
    ] = None
