from pydantic import BaseModel, Field
from typing import Annotated, Generic, TypeVar
from nexo.types.string import OptStr
from ....common.mixins.soap import Overall


PlanOverallT = TypeVar("PlanOverallT", bound=OptStr)


class PlanDTO(Overall[PlanOverallT], Generic[PlanOverallT]):
    pass


class FlexiblePlanDTO(PlanDTO[OptStr]):
    overall: Annotated[OptStr, Field(None, description="Overall")] = None


class StrictPlanDTO(PlanDTO[str]):
    pass


OptPlanDTO = PlanDTO | None
OptPlanDTOT = TypeVar("OptPlanDTOT", bound=OptPlanDTO)


class PlanDTOMixin(BaseModel, Generic[OptPlanDTOT]):
    plan: Annotated[OptPlanDTOT, Field(..., description="Plan")]
