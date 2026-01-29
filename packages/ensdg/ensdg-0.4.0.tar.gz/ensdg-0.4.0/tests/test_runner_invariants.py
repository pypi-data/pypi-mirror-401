import pytest

from ensdg.boundary import Boundary
from ensdg.example_governance import ExampleGovernance
from ensdg.example_rules import AcceptAll
from ensdg.runner import DecisionPrereqError, DblRunner


def test_decide_requires_prior_intent():
    runner = DblRunner(boundary=Boundary(1, AcceptAll()), governance=ExampleGovernance(), policy_version=1)
    with pytest.raises(DecisionPrereqError):
        runner.decide("c-1")


def test_execution_requires_prior_decision():
    runner = DblRunner(boundary=Boundary(1, AcceptAll()), governance=ExampleGovernance(), policy_version=1)
    runner.submit_intent("c-1", {"x": 1})
    with pytest.raises(DecisionPrereqError):
        runner.record_execution("c-1", {"ok": True})


def test_proof_requires_prior_decision():
    runner = DblRunner(boundary=Boundary(1, AcceptAll()), governance=ExampleGovernance(), policy_version=1)
    runner.submit_intent("c-1", {"x": 1})
    with pytest.raises(DecisionPrereqError):
        runner.record_proof("c-1", {"evidence": 1})


def test_validate_stream_requires_intent_schema():
    from ensdg.invariants import InvariantError, validate_stream
    from ensdg.model import DblEvent, EventKind

    events = [DblEvent(1, EventKind.INTENT, "c", {"boundary": {"boundary_config_hash": "sha256:" + "0" * 64}})]
    with pytest.raises(InvariantError, match="INTENT payload missing required keys"):
        validate_stream(events)


def test_validate_stream_requires_decision_schema():
    from ensdg.invariants import InvariantError, validate_stream
    from ensdg.model import DblEvent, EventKind

    events = [
        DblEvent(1, EventKind.INTENT, "c", {"authoritative_input": {"x": 1}, "boundary": {"boundary_version": 1, "boundary_config_hash": "sha256:" + "0" * 64}}),
        DblEvent(2, EventKind.DECISION, "c", {"decision": "ALLOW", "policy_version": True, "authoritative_digest": "sha256:" + "0" * 64, "rationale": {}}),
    ]
    with pytest.raises(InvariantError, match="DECISION policy_version must be int"):
        validate_stream(events)


def test_execution_after_deny_is_rejected():
    from ensdg.invariants import InvariantError, validate_stream
    from ensdg.model import DblEvent, EventKind

    events = [
        DblEvent(1, EventKind.INTENT, "c", {"authoritative_input": {"x": 1}, "boundary": {"boundary_version": 1, "boundary_config_hash": "sha256:" + "0" * 64}}),
        DblEvent(2, EventKind.DECISION, "c", {"decision": "DENY", "policy_version": 1, "authoritative_digest": "sha256:5041bf1f713df204784353e82f6a4a535931cb64f1f4b4a5aeaffcb720918b22", "rationale": {}}),
        DblEvent(3, EventKind.EXECUTION, "c", {"result": {"ok": True}}),
    ]
    with pytest.raises(InvariantError, match="EXECUTION/PROOF observed after non-ALLOW decision"):
        validate_stream(events)
