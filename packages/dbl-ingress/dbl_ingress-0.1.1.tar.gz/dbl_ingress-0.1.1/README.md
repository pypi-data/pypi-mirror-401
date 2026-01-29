# dbl-ingress

`dbl-ingress` serves as the admission and shaping layer for the Deterministic Boundary Layer (DBL). Its primary purpose is to strictly validate and shape external inputs into `AdmissionRecord` structures before they are processed by the core system, ensuring that no invalid or non-deterministic data enters the boundary event stream.

## Scope

- **Admission**: strict validation of incoming data payloads.
- **Shaping**: converting raw inputs into typed, immutable records.
- **Invariants**: enforcing data types (e.g., rejecting floats in deterministic fields) early in the pipeline.

## Non-Goals

- Execution logic or side effects.
- Policy decisions or complex business rules.
- Network transport or service runtime concerns.
- CLI tools.

## Relation to dbl-core

This library acts as a precursor to `dbl-core`. While `dbl-core` manages the deterministic event log and state reconstruction, `dbl-ingress` ensures that the data fed into `dbl-core` is well-formed and safe for deterministic processing.

## Validation against dbl-reference

See `docs/validation_workflow.md`.

## Status

**Experimental**: This project is in early development.
