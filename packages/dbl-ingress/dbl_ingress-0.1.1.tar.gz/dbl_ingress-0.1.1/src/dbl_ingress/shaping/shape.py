from typing import Mapping

from ..admission.json_types import JsonValue
from ..admission.model import AdmissionRecord


def shape_input(
    *, 
    correlation_id: str, 
    deterministic: Mapping[str, JsonValue], 
    observational: Mapping[str, JsonValue] | None = None
) -> AdmissionRecord:
    """
    Constructs an AdmissionRecord from inputs.
    
    This function acts as the primary entry point for creating strictly validated
    records for the dbl-core system. It enforces type constraints and data
    integrity.

    Args:
        correlation_id: A unique identifier for tracking this input.
        deterministic: A dictionary of deterministic data (JSON-safe, no floats).
        observational: Optional dictionary of observational data (JSON-safe, no floats).

    Returns:
        A validated AdmissionRecord.

    Raises:
        InvalidInputError: If validation fails (e.g. invalid types, floats present).
    """
    return AdmissionRecord(
        correlation_id=correlation_id,
        deterministic=deterministic,
        observational=observational
    )
