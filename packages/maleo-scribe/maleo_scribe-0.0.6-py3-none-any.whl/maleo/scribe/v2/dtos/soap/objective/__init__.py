from pydantic import BaseModel, Field
from typing import Annotated, Generic, TypeVar
from nexo.types.string import OptStr
from .....common.mixins.soap import Overall, OptOtherInformation
from .vital_sign import OptVitalSignDTOT, VitalSignDTO, VitalSignDTOMixin


ObjectiveOverallT = TypeVar("ObjectiveOverallT", bound=OptStr)


class ObjectiveDTO(
    OptOtherInformation,
    VitalSignDTOMixin[OptVitalSignDTOT],
    Overall[ObjectiveOverallT],
    Generic[
        ObjectiveOverallT,
        OptVitalSignDTOT,
    ],
):
    pass


class FlexibleObjectiveDTO(ObjectiveDTO[OptStr, VitalSignDTO]):
    overall: Annotated[OptStr, Field(None, description="Overall")] = None


class StrictObjectiveDTO(ObjectiveDTO[str, VitalSignDTO]):
    pass


OptObjectiveDTO = ObjectiveDTO | None
OptObjectiveDTOT = TypeVar("OptObjectiveDTOT", bound=OptObjectiveDTO)


class ObjectiveDTOMixin(BaseModel, Generic[OptObjectiveDTOT]):
    objective: Annotated[OptObjectiveDTOT, Field(..., description="Objective")]
