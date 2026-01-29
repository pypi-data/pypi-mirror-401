import json
from pathlib import Path

from ensdg.invariants import validate_stream
from ensdg.model import DblEvent, EventKind
from ensdg.replay import normative_digest, to_replay_view


FIXTURE = Path(__file__).parent / "fixtures" / "external_stream.jsonl"
EXPECTED_DIGEST = "sha256:74aebf0c8a4ec69e282a4c8c6f89a60d251c7627cd58efd35a0c828150f87b88"


def _load_events(path: Path) -> list[DblEvent]:
    events: list[DblEvent] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        events.append(
            DblEvent(
                event_id=int(obj["event_id"]),
                kind=EventKind(obj["kind"]),
                correlation_id=str(obj["correlation_id"]),
                payload=obj["payload"],
            )
        )
    return events


def test_external_stream_oracle_contract() -> None:
    events = _load_events(FIXTURE)
    validate_stream(events)
    digest = normative_digest(to_replay_view(events))
    assert digest == EXPECTED_DIGEST
