"""Build the proposed ATA v1.1 interface schemas; never writes inside phase-a/."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STR = {"type": "string", "minLength": 1}
ID = STR
TIME = {"type": "string", "format": "date-time"}
MONEY = {"oneOf": [{"type": "string", "pattern": r"^(0|[1-9][0-9]*)(\.[0-9]+)?$"}, {"type": "number", "minimum": 0}]}


def obj(properties, required=(), **extra):
    return {"type": "object", "properties": properties, "required": list(required), "additionalProperties": True, **extra}


def arr(items):
    return {"type": "array", "items": items}


def schema(path, title, props, required, description, **extra):
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"urn:ata:design:v1.1:{path.replace('/', ':')}",
        "title": title,
        "description": description,
        "x-design-status": "proposed-not-validated-by-phase-a-engine",
        "x-source-documents": ["ATA Reference Architecture v1.2", "Policy Schema & Authority Model v1.1"],
        "x-original-source-documents": ["ATA Reference Architecture v1.1", "Policy Schema & Authority Model v1.0"],
        "x-document-baseline": "Baseline Manifest v1.1 (2026-10-08); editorial alignment only",
        **obj(props, required, **extra),
    }


sc = {}
sc["authority/principal.schema.json"] = schema(
    "authority/principal.schema.json", "Principal",
    {"principal_id": ID, "type": {"enum": ["agent", "human", "system_service", "organizational_role"]},
     "acting_for": obj({"entity": ID}, ["entity"]), "delegated_by": obj({"role": ID})},
    ["principal_id", "type", "acting_for"], "Identity of a workflow actor, not a grant of financial authority.")

sc["authority/authority-envelope.schema.json"] = schema(
    "authority/authority-envelope.schema.json", "Authority Envelope",
    {"envelope_id": ID, "version": ID, "principal": obj({"principal_id": ID}, ["principal_id"]),
     "entity_scope": obj({"permitted": arr(ID)}, ["permitted"]),
     "actions": obj({"permitted": arr(ID)}, ["permitted"]),
     "currencies": obj({"permitted": arr(ID)}, ["permitted"]),
     "amount": obj({"max_single_transaction_usd_equivalent": MONEY}),
     "counterparties": obj({"mode": {"enum": ["APPROVED_ONLY", "ALLOWLIST"]}, "permitted": arr(ID)}),
     "assets": obj({"permitted": arr(ID)}), "rails": obj({"permitted": arr(ID)}),
     "jurisdictions": obj({"permitted": arr(ID)}),
     "approval": obj({"above_usd_equivalent": MONEY, "required_role": arr(ID)}),
     "validity": obj({"valid_from": TIME, "valid_until": TIME}, ["valid_from", "valid_until"]),
     "revocation": obj({"status": {"enum": ["ACTIVE", "REVOKED"]}, "effective_at": TIME}, ["status"])},
    ["envelope_id", "version", "principal", "entity_scope", "actions", "currencies", "validity", "revocation"],
    "Externally delegated maximum scope; transaction-specific Treasury Policy is evaluated separately.")

sc["policies/policy.schema.json"] = schema(
    "policies/policy.schema.json", "Treasury Policy",
    {"policy_id": ID, "version": ID, "status": {"enum": ["ACTIVE", "INACTIVE"]},
     "scope": obj({"entities": arr(ID), "actions": arr(ID)}, ["entities", "actions"]),
     "principals": obj({"permitted": arr(ID)}),
     "currencies": obj({"sell": arr(ID), "buy": arr(ID)}),
     "amount": obj({"max_single_transaction_usd_equivalent": MONEY}),
     "liquidity": obj({"min_post_execution_buffer": obj({"currency": ID, "value": MONEY}, ["currency", "value"])}),
     "counterparties": obj({"approved_only": {"type": "boolean"}}),
     "assets": obj({"permitted": arr(ID)}), "jurisdictions": obj({"permitted": arr(ID)}),
     "execution": obj({"permitted_rails": arr(ID)}),
     "approval": obj({"required_above_usd_equivalent": MONEY, "eligible_roles": arr(ID)}),
     "segregation_of_duties": obj({"proposer_cannot_approve": {"type": "boolean"}}),
     "data_requirements": obj({"treasury_state_max_age_seconds": {"type": "integer", "minimum": 0}}),
     "audit": obj({"mandatory": {"type": "boolean"}}),
     "conflict_behavior": obj({"default": {"const": "DENY"}}, ["default"])},
    ["policy_id", "version", "status", "scope", "conflict_behavior"],
    "Conditions for an action in the current treasury context; distinct from delegated authority.")

sc["policies/policy-decision.schema.json"] = schema(
    "policies/policy-decision.schema.json", "Policy Decision",
    {"decision_id": ID, "action_id": ID, "action_hash": ID,
     "outcome": {"enum": ["ALLOW", "DENY", "REQUIRE_APPROVAL", "REQUIRE_ADDITIONAL_INFORMATION"]},
     "reason_codes": arr(ID),
     "evaluated_policies": arr(obj({"policy_id": ID, "version": ID}, ["policy_id", "version"])),
     "evaluated_authority_envelope": obj({"envelope_id": ID, "version": ID}, ["envelope_id", "version"]),
     "treasury_state_version": ID, "approval_state_ref": ID, "evaluation_timestamp": TIME,
     "context_hash": ID},
    ["decision_id", "action_id", "outcome", "reason_codes", "evaluated_policies", "evaluated_authority_envelope", "treasury_state_version", "evaluation_timestamp"],
    "Deterministic governance result with versioned inputs and reason codes.")

sc["approvals/approval.schema.json"] = schema(
    "approvals/approval.schema.json", "Bounded Approval",
    {"approval_id": ID, "version": ID, "action_id": ID, "action_hash": ID,
     "approver": obj({"principal_id": ID, "role": ID}, ["principal_id", "role"]),
     "decision": {"enum": ["APPROVE", "REJECT"]}, "timestamp": TIME,
     "conditions": obj({"max_amount": MONEY, "currency": ID}), "expires_at": TIME},
    ["approval_id", "version", "action_id", "action_hash", "approver", "decision", "timestamp", "conditions", "expires_at"],
    "Action-bound, versioned approval; material modification invalidates approval.")

sc["execution/proposed-action.schema.json"] = schema(
    "execution/proposed-action.schema.json", "Proposed Action",
    {"action_id": ID, "proposed_by": obj({"principal_id": ID}, ["principal_id"]),
     "entity": obj({"entity_id": ID}, ["entity_id"]), "action_type": ID,
     "source": obj({"account_id": ID, "asset": ID}),
     "destination": obj({"account_id": ID, "asset": ID, "beneficiary_id": ID}),
     "amount": obj({"value": MONEY, "denomination": ID}, ["value", "denomination"]),
     "proposed_rail": ID, "settlement": obj({"requested_by": TIME}),
     "rationale": obj({"condition_id": ID, "summary": STR}), "treasury_state_ref": ID},
    ["action_id", "proposed_by", "entity", "action_type", "amount", "treasury_state_ref"],
    "Structured financial intent. Passing this schema never grants execution authority.",
    **{"not": {"anyOf": [{"required": ["execute"]}, {"required": ["authorized_instruction"]}, {"required": ["idempotency_key"]}]}})

sc["execution/authorized-instruction.schema.json"] = schema(
    "execution/authorized-instruction.schema.json", "Authorized Instruction",
    {"instruction_id": ID, "derived_from_action": obj({"action_id": ID, "action_hash": ID}, ["action_id", "action_hash"]),
     "entity": obj({"entity_id": ID}, ["entity_id"]), "action_type": ID,
     "source": obj({"account_id": ID}), "destination": obj({"account_id": ID, "beneficiary_id": ID}),
     "amount": obj({"value": MONEY, "currency": ID}, ["value", "currency"]),
     "rail": obj({"adapter": ID, "provider_id": ID}, ["adapter"]),
     "authorization": obj({"authority_envelope_id": ID, "authority_envelope_version": ID,
                           "policies": arr(obj({"policy_id": ID, "version": ID}, ["policy_id", "version"])),
                           "approval_ids": arr(ID), "decision_id": ID},
                          ["authority_envelope_id", "authority_envelope_version", "policies", "decision_id"]),
     "controls": obj({"idempotency_key": ID}, ["idempotency_key"]),
     "validity": obj({"expires_at": TIME}, ["expires_at"])},
    ["instruction_id", "derived_from_action", "entity", "action_type", "amount", "rail", "authorization", "controls", "validity"],
    "Executable only after a successful governance workflow; adapters independently validate binding and expiry.")

sc["settlement/transaction-state.schema.json"] = schema(
    "settlement/transaction-state.schema.json", "Transaction State",
    {"transaction_id": ID, "instruction_id": ID,
     "state": {"enum": ["REQUESTED", "AUTHORIZED", "SUBMITTED", "ACCEPTED", "SETTLED", "RECONCILED", "FAILED", "REVERSED", "EXCEPTION"]},
     "observed_at": TIME, "evidence_refs": arr(ID), "reason_codes": arr(ID)},
    ["transaction_id", "state", "observed_at"],
    "Lifecycle state; submission is not settlement or reconciliation.")

sc["settlement/reconciliation.schema.json"] = schema(
    "settlement/reconciliation.schema.json", "Reconciliation Result",
    {"reconciliation_id": ID, "instruction_id": ID, "transaction_id": ID,
     "status": {"enum": ["RECONCILED", "EXCEPTION"]}, "expected_state_ref": ID,
     "observed_evidence_refs": arr(ID), "difference_codes": arr(ID), "evaluated_at": TIME},
    ["reconciliation_id", "instruction_id", "status", "expected_state_ref", "observed_evidence_refs", "evaluated_at"],
    "Comparison of expected and observed financial outcomes; simulated receipts do not prove external finality.")

sc["audit/audit-record.schema.json"] = schema(
    "audit/audit-record.schema.json", "Audit Record",
    {"event_id": ID, "correlation_id": ID, "timestamp": TIME, "stage": ID,
     "actor": obj({"type": ID, "actor_id": ID}, ["type", "actor_id"]),
     "input": obj({"action_id": ID, "treasury_state_id": ID, "authority_envelope_id": ID}),
     "policies": obj({"evaluated": arr(obj({"policy_id": ID, "version": ID}, ["policy_id", "version"]))}),
     "decision": obj({"outcome": ID, "reason_codes": arr(ID)}),
     "evidence_refs": arr(ID), "previous_event_hash": {"type": ["string", "null"]}},
    ["event_id", "correlation_id", "timestamp", "stage", "actor"],
    "Structured audit event; a hash chain is local integrity evidence, not tamper-proof attestation.")


for relative, spec in sc.items():
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n")
print(f"Wrote {len(sc)} proposed design schemas")
