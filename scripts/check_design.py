"""Check proposed design files for syntax, inventory and resolvable local handoffs."""
import json
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = [
    "authority/principal.schema.json", "authority/authority-envelope.schema.json",
    "policies/policy.schema.json", "policies/policy-decision.schema.json",
    "approvals/approval.schema.json", "execution/proposed-action.schema.json",
    "execution/authorized-instruction.schema.json",
    "settlement/transaction-state.schema.json", "settlement/reconciliation.schema.json",
    "audit/audit-record.schema.json",
]
AGENTS = ["liquidity", "forecast", "payments", "fx-stablecoin", "yield", "governance"]
REQUEST = {"treasury_state", "objective", "constraints", "context"}
RESPONSE = {"observation", "reasoning_summary", "proposed_action", "expected_effect", "confidence", "required_controls", "evidence"}


def check():
    ids = set()
    for path in SCHEMAS:
        schema = json.loads((ROOT / path).read_text())
        assert schema["$schema"].endswith("2020-12/schema"), path
        assert schema["$id"] not in ids, path
        ids.add(schema["$id"])
        assert schema["x-design-status"] == "proposed-not-validated-by-phase-a-engine", path
        assert schema["type"] == "object" and schema["required"], path
    architecture = yaml.safe_load((ROOT / "architecture/ata-v1.1.yaml").read_text())
    assert len(architecture["layers"]) == 6
    assert architecture["layers"][3]["decisions"] == ["ALLOW", "DENY", "REQUIRE_APPROVAL", "REQUIRE_ADDITIONAL_INFORMATION"]
    contracts = []
    for name in AGENTS:
        contract = yaml.safe_load((ROOT / f"agents/{name}-agent.yaml").read_text())
        assert contract["id"] == f"{name}-agent"
        assert set(contract["request_fields"]) == REQUEST
        assert set(contract["response_fields"]) == RESPONSE
        assert contract["status"] == "proposed_contract_not_phase_a_executed"
        if contract["handoff"] is not None:
            assert (ROOT / contract["handoff"]).is_file()
        else:
            assert name in {"forecast", "governance"}, name
        contracts.append(contract["id"])
    assert set(contracts) == set(architecture["layers"][2]["canonical_agents"])
    invariant_text = (ROOT / "architecture/invariants.md").read_text()
    invariant_ids = [int(value) for value in re.findall(r"^\| I(\d{1,2}) \|", invariant_text, re.MULTILINE)]
    assert invariant_ids == list(range(1, 15)), "Invariants must retain approved I1–I14 numbering"
    reason_codes = yaml.safe_load((ROOT / "policies/reason-codes.yaml").read_text())
    assert reason_codes["status"] == "observed_phase_a_reason_codes"
    assert len(reason_codes["codes"]) == len(set(reason_codes["codes"]))
    print(f"PASS: {len(SCHEMAS)} proposed schemas, {len(contracts)} agent contracts, six layers, {len(invariant_ids)} sourced invariants, {len(reason_codes['codes'])} observed reason codes")
    print("Boundary: design syntax and inventory only; Phase A does not validate against these schemas")


if __name__ == "__main__":
    check()
