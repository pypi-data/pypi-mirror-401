from ..dtos.soap.subjective import StrictSubjectiveDTO
from ..dtos.soap.objective import StrictObjectiveDTO
from ..dtos.soap.objective.vital_sign import VitalSignDTO
from ..dtos.soap.assessment import StrictAssessmentDTO
from ..dtos.soap.plan import StrictPlanDTO
from ..dtos.soap import (
    StrictSOAPDTO,
    SOAPDTOMixin,
)
from ..mixins.transcription import Transcript
from ...common.mixins import Notes


class TranscriptionSchema(
    Notes[str],
    SOAPDTOMixin[StrictSOAPDTO],
    Transcript[str],
):
    pass


c = TranscriptionSchema(
    transcript="aaaaa",
    soap=StrictSOAPDTO(
        subjective=StrictSubjectiveDTO(chief_complaint="aaa"),
        objective=StrictObjectiveDTO(
            overall="alalalaa",
            vital_sign=VitalSignDTO(),
        ),
        assessment=StrictAssessmentDTO(overall="lalala"),
        plan=StrictPlanDTO(overall="lalala"),
    ),
    notes="lalalala",
)
