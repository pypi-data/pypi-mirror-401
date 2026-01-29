from pydantic import BaseModel, Field
from typing import Annotated, Generic, TypeVar
from .....common.mixins.soap.objective.vital_sign import (
    OptSystolicBloodPressure,
    OptDiastolicBloodPressure,
    OptTemperature,
    OptRespirationRate,
    OptHeartRate,
    OptOxygenSaturation,
    OptAbdominalCircumference,
    OptWaistCircumference,
    OptWeight,
    OptHeight,
    OptBodyMassIndex,
    OptOrganExaminationDetail,
)


class VitalSignDTO(
    OptOrganExaminationDetail,
    OptBodyMassIndex,
    OptWeight,
    OptHeight,
    OptWaistCircumference,
    OptAbdominalCircumference,
    OptOxygenSaturation,
    OptHeartRate,
    OptRespirationRate,
    OptTemperature,
    OptDiastolicBloodPressure,
    OptSystolicBloodPressure,
):
    pass


OptVitalSignDTO = VitalSignDTO | None
OptVitalSignDTOT = TypeVar("OptVitalSignDTOT", bound=OptVitalSignDTO)


class VitalSignDTOMixin(BaseModel, Generic[OptVitalSignDTOT]):
    vital_sign: Annotated[OptVitalSignDTOT, Field(..., description="Vital Sign")]
