from pathlib import Path
from copy import deepcopy
from datetime import datetime,timezone
import json,csv,sys,platform,hashlib
from engine import Engine,canonical,digest,D
ROOT=Path(__file__).resolve().parents[1]

def run_case(c):
    eng=Engine(ROOT);sid=c['scenario'];a=deepcopy(c['action']);m=c['mutation'];approval=None
    if m.get('stale_balance'):eng.balance_times[a['source_account']]='2026-09-23T14:54:59Z'
    if m.get('stale_state'):eng.state_time='2026-09-23T14:54:59Z'
    if m.get('revoke'):eng.envelopes[sid]['revocation_status']='REVOKED'
    if m.get('policy_conflict'):eng.extra_denials.add(a['asset'])
    if m.get('invent_provider'):a['counterparty']='INVENTED-PROVIDER'
    if m.get('principal_mismatch'):a['principal_id']='UNAUTHORIZED-AGENT'
    if m.get('negative_amount'):a['amount']=-1
    if m.get('self_approval'):approval=eng.approve(a,a['principal_id'])
    if any(m.get(k) for k in ['valid_approval','unavailable','alter_after_approval','settlement_mismatch','revoke_after_authorization','expired_approval','wrong_approver_role']):
        approval=eng.approve(a)
    if m.get('expired_approval'):approval['expires_at']='2026-09-23T14:59:59Z'
    if m.get('wrong_approver_role'):approval['approver_id']='USER-UNREGISTERED'
    if m.get('alter_after_approval'):a['amount']=400000
    decision=eng.evaluate(a,sid,approval);observed=decision['outcome'];execution={'state':'NONE','reconciliation':'N/A'};ins=None
    if m.get('alter_after_approval') and decision['outcome']=='REQUIRE_APPROVAL' and 'APPROVAL_INVALID_OR_EXPIRED' in decision['reason_codes']:
        observed='APPROVAL_INVALIDATED';eng.event('APPROVAL_VALIDATION',a,observed,['ACTION_HASH_CHANGED'])
    if decision['outcome']=='ALLOW' and not m.get('raw_action_execution'):
        ins=eng.authorize(a,sid,approval)
        if m.get('unavailable'):eng.unavailable.add(a['proposed_rail'])
        if m.get('revoke_after_authorization'):eng.envelopes[sid]['revocation_status']='REVOKED'
        if m.get('tamper_instruction'):ins['action']['amount']=90000
        if m.get('expired_instruction'):eng.now='2026-09-23T16:00:00Z'
        execution=eng.execute(ins,settlement_delta=1 if m.get('settlement_mismatch') else 0)
        if m.get('duplicate'):
            first=execution;execution=eng.execute(ins);execution['first_execution']=first
        if execution['state']!='SUCCESS':observed=execution['state']
        elif execution['reconciliation']=='EXCEPTION':observed='EXCEPTION'
    if m.get('raw_action_execution'):
        # This independent adapter attempt does not count the ordinary positive lifecycle above.
        execution=eng.execute({'action':a,'sid':sid});observed=execution['state']
    required={'event_id','timestamp','correlation_id','stage','actor_id','action_hash','dataset_version','outcome','reason_codes','evidence','previous_event_hash'}
    audit_complete=all(required<=set(x) for x in eng.audit)
    unauthorized=sum(s['authorization_outcome']!='ALLOW' for s in eng.submissions)
    return {'case_id':c['case_id'],'group':c['group'],'scenario_id':sid,'dataset_version':eng.version,
      'proposed_action_hash':digest(a),'authority_envelope_version':eng.envelopes[sid]['version'],
      'policy_versions':decision['policy_versions'],'approval_state':approval,'observed_decision':decision['outcome'],
      'observed_outcome':observed,'reason_codes':decision['reason_codes'],'authorized_instruction_id':ins['instruction_id'] if ins else None,
      'execution_state':execution['state'],'reconciliation_state':execution['reconciliation'],
      'settlement_evidence_ref':execution.get('receipt',{}).get('receipt_id'),
      'execution_detail':execution,'audit_record_refs':[e['event_id'] for e in eng.audit],
      'audit_complete':audit_complete,'unauthorized_execution_count':unauthorized,
      'adapter_submissions':len(eng.submissions),'audit':eng.audit}

def main():
    manifest=json.loads((ROOT/'metadata/sprint3c-manifest.json').read_text())
    for entry in manifest['files']:
        assert hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest()==entry['sha256'], 'Sprint 3C input drift: '+entry['path']
    cases=json.loads((ROOT/'resolved/cases.json').read_text());expectations=json.loads((ROOT/'resolved/expectations.json').read_text())
    freeze=json.loads((ROOT/'resolved/freeze.json').read_text())
    assert digest(cases)==freeze['cases_sha256'] and digest(expectations)==freeze['expectations_sha256']
    n=Engine(ROOT).protocol['core_evaluation']['phase_A_deterministic_replay']['repetitions_per_case']
    results=[];aggregates=[];started=datetime.now(timezone.utc).isoformat()
    for c in cases:
        repetitions=[]
        for i in range(n):
            r=run_case(c);r['behavior_hash']=digest(r);r['run_id']=f"{c['case_id']}-R{i+1:02d}";results.append(r);repetitions.append(r)
        first=repetitions[0];expected=expectations[c['case_id']]
        exact=first['observed_outcome']==expected
        semantic=exact or (expected=='FAIL_CLOSED_OR_ESCALATE' and first['observed_decision'] in ['DENY','REQUIRE_ADDITIONAL_INFORMATION'])
        aggregates.append({'case_id':c['case_id'],'group':c['group'],'expected':expected,'observed':first['observed_outcome'],
          'exact_match':exact,'semantic_match':semantic,'consistent':len({r['behavior_hash'] for r in repetitions})==1,
          'repetitions':n,'reason_codes':'|'.join(first['reason_codes']),'execution_state':first['execution_state'],'reconciliation':first['reconciliation_state']})
    prereg=[r for r in aggregates if r['group'] in ['primary','variant','negative']]
    governance=[r for r in prereg if r['expected'] in ['ALLOW','DENY','REQUIRE_APPROVAL','REQUIRE_ADDITIONAL_INFORMATION']]
    lifecycle=[e for r in results for e in r['audit'] if e['stage']=='RECONCILIATION']
    summary={'artifact':'ATA Simulation Harness & Experimental Run v1.0','status':'EXECUTED_WITH_DOCUMENTED_EXPECTATION_DISCREPANCIES',
      'started_at':started,'completed_at':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),
      'case_count':len(cases),'repetitions_per_case':n,'total_runs':len(results),
      'preregistered_cases':len(prereg),'preregistered_exact_matches':sum(r['exact_match'] for r in prereg),
      'preregistered_semantic_matches':sum(r['semantic_match'] for r in prereg),
      'governance_expected_decision_matches':sum(r['exact_match'] for r in governance),'governance_expected_decision_cases':len(governance),
      'deterministic_cases':sum(r['consistent'] for r in aggregates),
      'audit_complete_runs':sum(r['audit_complete'] for r in results),
      'unauthorized_execution_count':sum(r['unauthorized_execution_count'] for r in results),
      'duplicate_attempts':sum(r['case_id']=='T09' for r in results),
      'duplicates_rejected':sum(r['case_id']=='T09' and r['execution_detail'].get('reason')=='DUPLICATE_INSTRUCTION' for r in results),
      'adapter_submissions':sum(r['adapter_submissions'] for r in results),
      'reconciled_settlements':sum(e['outcome']=='RECONCILED' for e in lifecycle),'total_settlements':len(lifecycle),
      'discrepancies':[r for r in aggregates if not r['exact_match']],
      'phase_B':'NOT_RUN_OPTIONAL','synthetic_dataset_literature_gap':'OPEN'}
    out=ROOT/'results';out.mkdir(exist_ok=True)
    (out/'runs.jsonl').write_text('\n'.join(canonical(r) for r in results)+'\n')
    with (out/'case_summary.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(aggregates[0]));w.writeheader();w.writerows(aggregates)
    (out/'summary.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
