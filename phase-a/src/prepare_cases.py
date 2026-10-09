"""Resolve narrative scenario mutations into explicit fixtures BEFORE running.
Original Sprint 3C files remain byte-identical; choices documented in ASSUMPTIONS.md.
"""
from pathlib import Path
from copy import deepcopy
import json
from engine import Engine,read_yaml,rows,digest
ROOT=Path(__file__).resolve().parents[1]

def build():
    eng=Engine(ROOT);cases=[];expectations={};bases={}
    for file in sorted((ROOT/'scenarios').glob('*.yaml')):
        s=read_yaml(file);sid=s['scenario_id']
        actions=s.get('proposed_actions',[s.get('proposed_action')])
        for raw in actions:
            a=deepcopy(raw);cid=a.pop('case_id',sid+'-A');expected=a.pop('expected',s.get('expected_governance',{}).get('initial_outcome'))
            a['principal_id']=eng.envelopes[sid]['principal_id'];a['treasury_state_ref']=eng.version
            if sid=='S01': a['asset']=a['currency']
            if sid=='S02':
                a['amount']=a.pop('amount_usd_equivalent');a['asset']=a.pop('buy_asset');a['currency']=a['asset'];a['jurisdiction']='BR'
                a['source_account']='ACC-BR-OPER-01';a['destination_account']='ACC-BR-USD-01' if a['asset']=='USD' else 'WAL-BR-USDC-01'
            if sid=='S04':
                a['currency']=a['asset'];a['jurisdiction']='SG';a['source_account']='ACC-US-OPER-01' if a['asset']=='USD' else 'WAL-US-USDC-01'
            bases[cid]=a;cases.append({'case_id':cid,'scenario':sid,'group':'primary','action':a,'mutation':{}});expectations[cid]=expected
        for v in s['variants']:
            cid=v['case_id'];base=deepcopy(bases[sid+'-A']);base['action_id']='ACT-'+cid;mut={}
            changes={'S01-B':{'amount':350000},'S01-C':{'amount':700000},'S02-C':{'asset':'XYZ-STABLE','currency':'XYZ-STABLE'},'S02-D':{'amount':550000},
                     'S03-B':{'amount':150000},'S03-C':{'amount':250000},'S03-D':{'asset':'UNAPPROVED-TMMF'},'S04-C':{'beneficiary':'BAD-BEN-001'}}
            base.update(changes.get(cid,{}))
            if cid=='S01-D':mut['stale_balance']=True
            if cid=='S02-E':mut['stale_state']=True
            if cid=='S04-D':mut['self_approval']=True
            if cid=='S04-E':base.pop('jurisdiction')
            cases.append({'case_id':cid,'scenario':sid,'group':'variant','action':base,'mutation':mut});expectations[cid]=v['expected']
    byid={c['case_id']:c for c in cases}
    equivalent={'T01':'S01-D','T02':'S04-C','T03':'S01-B','T04':'S02-D','T05':'S02-C','T06':'S03-C','T07':'S04-E','T08':'S04-D'}
    mutations={'T09':'duplicate','T10':'revoke','T11':'unavailable','T12':'alter_after_approval','T13':'settlement_mismatch','T14':'policy_conflict','T15':'invent_provider'}
    for r in rows(ROOT/'expected_results/negative_tests.csv'):
        tid=r['test_id'];sid=r['scenario'];c=deepcopy(byid[equivalent.get(tid,sid+'-A')]);c['case_id']=tid;c['group']='negative';c['action']['action_id']='ACT-'+tid
        if tid in mutations:c['mutation'][mutations[tid]]=True
        cases.append(c);expectations[tid]=r['expected']
    for bid in ['S01-B','S02-A','S02-B','S03-B','S04-A','S04-B']:
        c=deepcopy(byid[bid]);cid=bid+'-APPROVED';c['case_id']=cid;c['group']='approved_lifecycle';c['mutation']['valid_approval']=True
        cases.append(c);expectations[cid]='ALLOW'
    # Additional safeguards: kept separate from preregistered Sprint 3C cohort.
    additions=[('X01','S02-A','revoke_after_authorization','EXECUTION_REJECTED'),('X02','S04-A','expired_approval','REQUIRE_APPROVAL'),
      ('X03','S01-A','tamper_instruction','EXECUTION_REJECTED'),('X04','S01-A','expired_instruction','EXECUTION_REJECTED'),
      ('X05','S01-A','raw_action_execution','EXECUTION_REJECTED'),('X06','S02-A','wrong_approver_role','REQUIRE_APPROVAL'),
      ('X07','S01-A','principal_mismatch','DENY'),('X08','S03-A','negative_amount','REQUIRE_ADDITIONAL_INFORMATION')]
    for cid,bid,mutation,expected in additions:
        c=deepcopy(byid[bid]);c['case_id']=cid;c['group']='additional_safeguard';c['action']['action_id']='ACT-'+cid;c['mutation'][mutation]=True
        cases.append(c);expectations[cid]=expected
    out=ROOT/'resolved';out.mkdir(exist_ok=True)
    (out/'cases.json').write_text(json.dumps(cases,indent=2))
    (out/'expectations.json').write_text(json.dumps(expectations,indent=2))
    (out/'freeze.json').write_text(json.dumps({'cases_sha256':digest(cases),'expectations_sha256':digest(expectations),'case_count':len(cases),'note':'Frozen before evaluator run. Additional safeguards are not preregistered Sprint 3C cases.'},indent=2))
    print('Frozen',len(cases),'cases')
if __name__=='__main__':build()
