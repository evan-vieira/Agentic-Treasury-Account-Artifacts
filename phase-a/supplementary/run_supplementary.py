"""Supplementary robustness tests for ATA Sprint 3D.

This runner does NOT modify the original Sprint 3D cases, expectations, or results.
It adds separately versioned post-hoc robustness tests:
  T15b: provider-to-adapter binding validation
  A1: Authority Envelope enforcement ablation (full vs policy-only)
  A2: Treasury Policy enforcement ablation (full vs authority-only)

No network, LLMs, real payment rails, or external settlement systems are used.
"""
from copy import deepcopy
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, platform, sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from engine import Engine,D,digest,canonical

SUPP_VERSION='ATA-SUPP-GOV-v1.0'
REPETITIONS=10
GHOST='FX-PROV-GHOST'


def original_integrity():
    manifest=json.loads((ROOT/'metadata/sprint3c-manifest.json').read_text())
    checked=[]
    for entry in manifest['files']:
        actual=hashlib.sha256((ROOT/entry['path']).read_bytes()).hexdigest()
        checked.append({'path':entry['path'],'expected':entry['sha256'],'actual':actual,'match':actual==entry['sha256']})
    cases=json.loads((ROOT/'resolved/cases.json').read_text())
    expectations=json.loads((ROOT/'resolved/expectations.json').read_text())
    freeze=json.loads((ROOT/'resolved/freeze.json').read_text())
    return {
      'manifest_files':len(checked),
      'manifest_matches':sum(x['match'] for x in checked),
      'cases_freeze_match':digest(cases)==freeze['cases_sha256'],
      'expectations_freeze_match':digest(expectations)==freeze['expectations_sha256'],
      'details':checked,
    }


def ghost_counterparty(engine):
    engine.counterparties[GHOST]={
      'counterparty_id':GHOST,'country':'BR','type':'fx_provider','approved':'True',
      'bank_destination':'N/A','wallet_destination':'N/A'
    }


def base_cases():
    cases={c['case_id']:c for c in json.loads((ROOT/'resolved/cases.json').read_text())}
    s02=deepcopy(cases['S02-A']['action'])
    s02.update({'action_id':'ACT-T15B','amount':50000,'counterparty':GHOST})
    a1=deepcopy(s02);a1['action_id']='ACT-A1'
    a2=deepcopy(cases['S03-C']['action']);a2['action_id']='ACT-A2'
    return s02,a1,a2


def neutralize_authority(engine,sid,a):
    """Make Authority Envelope non-binding while retaining Treasury Policy enforcement.
    This is a deliberate ablation, not a production configuration.
    """
    e=deepcopy(engine.envelopes[sid])
    e['principal_id']=a['principal_id']
    e['entity_scope']=sorted(set(e.get('entity_scope',[])+[a['entity']]))
    e['actions']=sorted(set(e.get('actions',[])+[a['action_type']]))
    e['currencies']=sorted(set(e.get('currencies',[])+[a['currency'],a.get('sell_asset',a['currency'])]))
    for k in list(e):
        if k.startswith('max_amount'): e[k]=10**15
    if 'permitted_counterparties' in e:
        e['permitted_counterparties']=sorted(set([k for k,v in engine.counterparties.items() if v.get('approved')=='True']+[a.get('counterparty') or a.get('beneficiary')]))
    if 'permitted_assets' in e:
        e['permitted_assets']=sorted(set([k for k,v in engine.assets.items() if v.get('approved_for_treasury')=='True']+[a['asset']]))
    e['permitted_rails']=sorted(set(engine.rails.keys()))
    if 'jurisdictions' in e:
        e['jurisdictions']=sorted(set([v.get('country') for v in engine.counterparties.values() if v.get('country')]+([a.get('jurisdiction')] if a.get('jurisdiction') else [])))
    for k in list(e.get('approval_requirement',{})):
        e['approval_requirement'][k]=10**15
    e['valid_from']='2020-01-01T00:00:00Z';e['valid_until']='2099-12-31T23:59:59Z';e['revocation_status']='ACTIVE'
    e['version']='ABLATION-POLICY-ONLY-v1.0'
    engine.envelopes[sid]=e


def neutralize_policy(engine,sid):
    """Make transaction-specific Treasury Policy non-binding while retaining Authority Envelope.
    Common data-integrity controls remain active. Deliberate ablation only.
    """
    e=engine.envelopes[sid];p=deepcopy(engine.policies[sid])
    p['status']='ACTIVE'
    p['scope']['entities']=list(e['entity_scope']);p['scope']['actions']=list(e['actions'])
    if 'currencies' in p:
        p['currencies']['sell']=['BRL','USD','EUR','USDC']
        p['currencies']['buy']=['BRL','USD','EUR','USDC']
    if 'assets' in p:
        p['assets']['permitted']=[k for k,v in engine.assets.items() if v.get('approved_for_treasury')=='True']
    if 'rails' in p:
        p['rails']['permitted']=list(engine.rails.keys())
    if 'jurisdictions' in p:
        p['jurisdictions']['permitted']=['BR','US','SG','NL','XX']
    for k in list(p.get('amount',{})):
        if k.startswith('max_single') or k.startswith('autonomous_threshold'): p['amount'][k]=10**15
    for k in list(p.get('liquidity',{})):
        if k.startswith('min_'): p['liquidity'][k]=-10**15
    for k in list(p.get('approval',{})):
        if k.startswith('required_above'): p['approval'][k]=10**15
    p['version']='ABLATION-AUTHORITY-ONLY-v1.0'
    engine.policies[sid]=p


def common_result(case_id,variant,engine,a,decision=None,instruction=None,execution=None):
    return {
      'supplementary_version':SUPP_VERSION,'case_id':case_id,'variant':variant,
      'dataset_version':engine.version,'action_hash':digest(a),
      'decision':decision['outcome'] if decision else None,
      'reason_codes':decision['reason_codes'] if decision else [],
      'instruction_issued':bool(instruction),
      'instruction_id':instruction.get('instruction_id') if instruction else None,
      'execution_state':execution.get('state') if execution else 'NOT_ATTEMPTED',
      'execution_reason':execution.get('reason') if execution else None,
      'reconciliation':execution.get('reconciliation') if execution else 'N/A',
      'adapter_submissions':len(engine.submissions),
      'balances_hash':digest(engine.balances),
      'audit_hash':digest(engine.audit),
      'audit_events':len(engine.audit),
    }


def run_t15b():
    a,_,_=base_cases();e=Engine(ROOT);ghost_counterparty(e)
    # Governance explicitly permits the ghost provider for this supplementary fixture,
    # but the selected bank_fx rail remains bound to FX-PROV-01 in the adapter registry.
    e.envelopes['S02']['permitted_counterparties'].append(GHOST)
    before=deepcopy(e.balances)
    decision=e.evaluate(a,'S02')
    ins=e.authorize(a,'S02') if decision['outcome']=='ALLOW' else None
    # authorize evaluates again; no approval needed at 50k.
    execution=e.execute(ins) if ins else None
    r=common_result('T15b','FULL_GOVERNANCE_ADAPTER_BINDING',e,a,decision,ins,execution)
    r.update({
      'expected_decision':'ALLOW','expected_execution_state':'EXECUTION_VALIDATION_FAIL',
      'expected_execution_reason':'PROVIDER_RAIL_MISMATCH',
      'no_balance_mutation':before==e.balances,
      'expected_match': decision['outcome']=='ALLOW' and bool(ins) and execution and execution['state']=='EXECUTION_VALIDATION_FAIL' and execution.get('reason')=='PROVIDER_RAIL_MISMATCH' and before==e.balances and len(e.submissions)==0,
    })
    return r


def run_a1_full():
    _,a,_=base_cases();e=Engine(ROOT);ghost_counterparty(e)
    # Ghost is approved globally/policy-compatible but deliberately outside the original Authority Envelope.
    decision=e.evaluate(a,'S02')
    ins=e.authorize(a,'S02') if decision['outcome']=='ALLOW' else None
    r=common_result('A1','FULL_GOVERNANCE',e,a,decision,ins,None)
    r.update({'expected_decision':'DENY','expected_match':decision['outcome']=='DENY' and 'COUNTERPARTY_OUTSIDE_AUTHORITY' in decision['reason_codes'] and not ins})
    return r


def run_a1_policy_only():
    _,a,_=base_cases();e=Engine(ROOT);ghost_counterparty(e);neutralize_authority(e,'S02',a)
    decision=e.evaluate(a,'S02')
    ins=e.authorize(a,'S02') if decision['outcome']=='ALLOW' else None
    r=common_result('A1','POLICY_ONLY_ABLATION',e,a,decision,ins,None)
    r.update({'expected_decision':'ALLOW','expected_match':decision['outcome']=='ALLOW' and bool(ins)})
    return r


def run_a2_full():
    _,_,a=base_cases();e=Engine(ROOT)
    approval=e.approve(a)
    decision=e.evaluate(a,'S03',approval)
    ins=e.authorize(a,'S03',approval) if decision['outcome']=='ALLOW' else None
    r=common_result('A2','FULL_GOVERNANCE',e,a,decision,ins,None)
    r.update({'expected_decision':'DENY','expected_match':decision['outcome']=='DENY' and 'PROJECTED_LIQUIDITY_BREACH' in decision['reason_codes'] and not ins})
    return r


def run_a2_authority_only():
    _,_,a=base_cases();e=Engine(ROOT);neutralize_policy(e,'S03')
    approval=e.approve(a)
    decision=e.evaluate(a,'S03',approval)
    ins=e.authorize(a,'S03',approval) if decision['outcome']=='ALLOW' else None
    execution=e.execute(ins) if ins else None
    r=common_result('A2','AUTHORITY_ONLY_ABLATION',e,a,decision,ins,execution)
    r.update({'expected_decision':'ALLOW','expected_execution_state':'SUCCESS','expected_match':decision['outcome']=='ALLOW' and bool(ins) and execution and execution['state']=='SUCCESS' and execution['reconciliation']=='RECONCILED'})
    return r

RUNNERS=[run_t15b,run_a1_full,run_a1_policy_only,run_a2_full,run_a2_authority_only]


def main():
    integ=original_integrity()
    started=datetime.now(timezone.utc).isoformat()
    all_runs=[];summaries=[]
    for fn in RUNNERS:
        reps=[]
        for i in range(REPETITIONS):
            r=fn();r['run_id']=f"{r['case_id']}-{r['variant']}-R{i+1:02d}"
            r['behavior_hash']=digest({k:v for k,v in r.items() if k not in ['run_id','behavior_hash']})
            reps.append(r);all_runs.append(r)
        first=reps[0]
        summaries.append({
          'case_id':first['case_id'],'variant':first['variant'],'repetitions':REPETITIONS,
          'expected_decision':first.get('expected_decision'),'observed_decision':first['decision'],
          'expected_execution_state':first.get('expected_execution_state'),'observed_execution_state':first['execution_state'],
          'execution_reason':first.get('execution_reason'),'instruction_issued':first['instruction_issued'],
          'expected_match':all(x['expected_match'] for x in reps),
          'deterministic':len({x['behavior_hash'] for x in reps})==1,
          'reason_codes':first['reason_codes'],
        })
    summary={
      'artifact':'ATA Supplementary Governance Tests v1.0','status':'EXECUTED',
      'started_at':started,'completed_at':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),
      'original_integrity':{k:v for k,v in integ.items() if k!='details'},
      'supplementary_case_variants':len(summaries),'repetitions_per_variant':REPETITIONS,'total_supplementary_runs':len(all_runs),
      'all_expected_matches':all(x['expected_match'] for x in summaries),
      'all_deterministic':all(x['deterministic'] for x in summaries),
      'results':summaries,
      'interpretation_boundary':'Post-hoc supplementary robustness tests; separate from the original Sprint 3D case set and denominators.'
    }
    out=ROOT/'results-supplementary';out.mkdir(exist_ok=True)
    (out/'runs.jsonl').write_text('\n'.join(canonical(r) for r in all_runs)+'\n')
    (out/'summary.json').write_text(json.dumps(summary,indent=2))
    (out/'integrity.json').write_text(json.dumps(integ,indent=2))
    (out/'protocol.json').write_text(json.dumps({
      'version':SUPP_VERSION,'post_hoc':True,'repetitions_per_variant':REPETITIONS,
      'tests':[
        {'id':'T15b','purpose':'Isolate provider-to-adapter binding validation after governance ALLOW and AuthorizedInstruction issuance.'},
        {'id':'A1','purpose':'Compare full governance with Authority Envelope enforcement neutralized (policy-only ablation).'},
        {'id':'A2','purpose':'Compare full governance with transaction-specific Treasury Policy enforcement neutralized (authority-only ablation).'}
      ],
      'original_results_immutable':True
    },indent=2))
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
