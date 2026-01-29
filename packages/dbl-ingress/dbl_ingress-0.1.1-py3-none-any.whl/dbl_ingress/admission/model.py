from dataclasses import dataclass
from typing import Mapping

from ..reason_codes import ADMISSION_INVALID_INPUT
from .errors import InvalidInputError
from .json_types import JsonMapping, deep_freeze


@dataclass(frozen=True)
class AdmissionRecord:
    correlation_id: str
    deterministic: JsonMapping
    observational: JsonMapping | None = None

    def __post_init__(self) -> None:
        # NOTE:
        # AdmissionRecord performs validation and freezing only.
        # It MUST NOT:
        # - interpret semantics
        # - apply policy
        # - inspect dbl-core state
        if not isinstance(self.correlation_id, str) or not self.correlation_id:
            raise InvalidInputError(
                "correlation_id must be a non-empty string",
                reason_code=ADMISSION_INVALID_INPUT,
            )
        
        # Validate and freeze deterministic data
        if not isinstance(self.deterministic, Mapping):
            raise InvalidInputError(
                "deterministic must be a dictionary or mapping",
                reason_code=ADMISSION_INVALID_INPUT,
            )

        try:
            # Enforce immutability / validation
            # We must use object.__setattr__ because the dataclass is frozen
            object.__setattr__(
                self, 
                'deterministic', 
                deep_freeze(self.deterministic, "deterministic")
            )
            
            # Validate and freeze observational data if present
            if self.observational is not None:
                if not isinstance(self.observational, Mapping):
                    raise InvalidInputError(
                        "observational must be a dictionary or mapping if provided",
                        reason_code=ADMISSION_INVALID_INPUT,
                    )
                
                object.__setattr__(
                    self, 
                    'observational', 
                    deep_freeze(self.observational, "observational")
                )

        except TypeError as e:
            raise InvalidInputError(str(e), reason_code=ADMISSION_INVALID_INPUT) from e

