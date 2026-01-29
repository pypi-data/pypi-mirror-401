from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Sequence

from .canon import canon_bytes
from .digest import sha256_label
from .model import DblEvent, EventKind


class InvariantError(Exception):
    pass


@dataclass(frozen=True)
class CorrelationState:
    saw_intent: bool = False
    saw_decision: bool = False
    decision: str | None = None


def validate_stream(events: Sequence[DblEvent]) -> None:
    last_event_id = -1
    by_corr: Dict[str, CorrelationState] = {}
    authoritative_digest_by_corr: Dict[str, str] = {}

    for e in events:
        if e.event_id <= last_event_id:
            raise InvariantError(
                f"event_id must be strictly increasing (append-only order); "
                f"event_id={e.event_id} last_event_id={last_event_id}"
            )
        if not e.correlation_id:
            raise InvariantError(f"correlation_id must be non-empty; event_id={e.event_id}")

        state = by_corr.get(e.correlation_id, CorrelationState())

        if e.kind == EventKind.INTENT:
            _validate_intent_payload(e.payload, e.event_id)
            if state.saw_intent:
                raise InvariantError(
                    f"multiple INTENT events for correlation_id; "
                    f"correlation_id={e.correlation_id} event_id={e.event_id}"
                )
            authoritative_digest_by_corr[e.correlation_id] = sha256_label(
                canon_bytes(e.payload["authoritative_input"])
            )
            state = CorrelationState(
                saw_intent=True,
                saw_decision=state.saw_decision,
                decision=state.decision,
            )
        elif e.kind == EventKind.DECISION:
            _validate_decision_payload(e.payload, e.event_id)
            if not state.saw_intent:
                raise InvariantError(
                    f"DECISION observed before INTENT for correlation_id; "
                    f"correlation_id={e.correlation_id} event_id={e.event_id}"
                )
            if state.saw_decision:
                raise InvariantError(
                    f"multiple DECISION events for correlation_id; "
                    f"correlation_id={e.correlation_id} event_id={e.event_id}"
                )
            expected = authoritative_digest_by_corr.get(e.correlation_id)
            if expected is not None and e.payload["authoritative_digest"] != expected:
                raise InvariantError(
                    "DECISION authoritative_digest does not match INTENT authoritative_input; "
                    f"correlation_id={e.correlation_id} event_id={e.event_id}"
                )
            state = CorrelationState(
                saw_intent=state.saw_intent,
                saw_decision=True,
                decision=e.payload["decision"],
            )
        elif e.kind in (EventKind.EXECUTION, EventKind.PROOF):
            if not state.saw_decision:
                raise InvariantError(
                    f"EXECUTION/PROOF observed before DECISION for correlation_id; "
                    f"correlation_id={e.correlation_id} event_id={e.event_id}"
                )
            if state.decision != "ALLOW":
                raise InvariantError(
                    f"EXECUTION/PROOF observed after non-ALLOW decision; "
                    f"correlation_id={e.correlation_id} event_id={e.event_id}"
                )

        by_corr[e.correlation_id] = state
        last_event_id = e.event_id


def _validate_intent_payload(payload: object, event_id: int) -> None:
    if not isinstance(payload, dict):
        raise InvariantError(f"INTENT payload must be object; event_id={event_id}")
    if "authoritative_input" not in payload or "boundary" not in payload:
        raise InvariantError(f"INTENT payload missing required keys; event_id={event_id}")
    # Authoritative input must be canonicalizable (no floats, no non-json-safe types).
    from .canon import CanonError, canon_bytes

    try:
        canon_bytes(payload["authoritative_input"])
    except CanonError as exc:
        raise InvariantError(
            f"INTENT authoritative_input is not canonical: {exc}; event_id={event_id}"
        ) from exc
    boundary = payload["boundary"]
    if not isinstance(boundary, dict):
        raise InvariantError(f"INTENT boundary must be object; event_id={event_id}")
    if "boundary_version" not in boundary:
        raise InvariantError(f"INTENT boundary missing boundary_version; event_id={event_id}")
    bv = boundary["boundary_version"]
    if isinstance(bv, bool) or not isinstance(bv, int):
        raise InvariantError(f"INTENT boundary_version must be int; event_id={event_id}")
    if "boundary_config_hash" not in boundary:
        raise InvariantError(f"INTENT boundary missing boundary_config_hash; event_id={event_id}")
    bch = boundary["boundary_config_hash"]
    if not isinstance(bch, str) or not _is_sha256_label(bch):
        raise InvariantError(
            f"INTENT boundary_config_hash must be sha256: with 64 hex; event_id={event_id}"
        )


def _validate_decision_payload(payload: object, event_id: int) -> None:
    if not isinstance(payload, dict):
        raise InvariantError(f"DECISION payload must be object; event_id={event_id}")
    for key in ("decision", "policy_version", "authoritative_digest"):
        if key not in payload:
            raise InvariantError(f"DECISION payload missing {key}; event_id={event_id}")
    decision = payload["decision"]
    if decision not in ("ALLOW", "DENY"):
        raise InvariantError(f"DECISION decision must be ALLOW or DENY; event_id={event_id}")
    pv = payload["policy_version"]
    if isinstance(pv, bool) or not isinstance(pv, int):
        raise InvariantError(f"DECISION policy_version must be int; event_id={event_id}")
    ad = payload["authoritative_digest"]
    if not isinstance(ad, str) or not _is_sha256_label(ad):
        raise InvariantError(
            f"DECISION authoritative_digest must be sha256: with 64 hex; event_id={event_id}"
        )


def _is_sha256_label(value: str) -> bool:
    if not value.startswith("sha256:"):
        return False
    hex_part = value[7:]
    if len(hex_part) != 64:
        return False
    return all(ch in "0123456789abcdefABCDEF" for ch in hex_part)
