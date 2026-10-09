"""Independent assertions; these do not read the engine's expected outcome fixtures."""
import sys,unittest,json
from pathlib import Path
from copy import deepcopy
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from engine import Engine,D,digest

class Controls(unittest.TestCase):
    def setUp(self):
        self.e=Engine(ROOT)
        self.cases={c['case_id']:c for c in json.loads((ROOT/'resolved/cases.json').read_text())}
    def a(self,cid):return deepcopy(self.cases[cid]['action'])
    def test_liquidity_accounting_and_duplicate(self):
        a=self.a('S01-A');i=self.e.authorize(a,'S01');r=self.e.execute(i)
        self.assertEqual(self.e.balances['ACC-BR-RES-01'],D('2370000'))
        self.assertEqual(self.e.balances['ACC-BR-OPER-01'],D('3360000'))
        before=deepcopy(self.e.balances)
        self.assertEqual(self.e.execute(i)['state'],'EXECUTION_REJECTED')
        self.assertEqual(before,self.e.balances);self.assertEqual(len(self.e.submissions),1)
    def test_fx_accounting(self):
        for cid,cost,dest,end in [('S02-A','2434860','ACC-BR-USD-01','670000'),('S02-B','2433989.25','WAL-BR-USDC-01','630000')]:
            e=Engine(ROOT);a=self.a(cid)
            self.assertIsNone(e.authorize(a,'S02'))
            r=e.execute(e.authorize(a,'S02',e.approve(a)))
            self.assertEqual(r['reconciliation'],'RECONCILED')
            self.assertEqual(e.balances['ACC-BR-OPER-01'],D('3280000')-D(cost))
            self.assertEqual(e.balances[dest],D(end))
    def test_cross_border_two_rails(self):
        for cid,source,end in [('S04-A','ACC-US-OPER-01','1000000'),('S04-B','WAL-US-USDC-01','50000')]:
            e=Engine(ROOT);a=self.a(cid);r=e.execute(e.authorize(a,'S04',e.approve(a)))
            self.assertEqual(e.balances[source],D(end));self.assertEqual(r['reconciliation'],'RECONCILED')
    def test_yield_accounting(self):
        a=self.a('S03-A');r=self.e.execute(self.e.authorize(a,'S03'))
        self.assertEqual(self.e.balances['ACC-US-OPER-01'],D('1175000'))
        self.assertEqual(r['receipt']['observed_balances']['POSITION:TMMF-USD-01'],D('75000'))
    def test_approval_binds_destination(self):
        a=self.a('S04-A');apr=self.e.approve(a);a['destination']='ATTACKER'
        self.assertIsNone(self.e.authorize(a,'S04',apr));self.assertEqual(len(self.e.submissions),0)
    def test_revocation_after_issue(self):
        a=self.a('S02-A');i=self.e.authorize(a,'S02',self.e.approve(a));before=deepcopy(self.e.balances)
        self.e.envelopes['S02']['revocation_status']='REVOKED'
        self.assertEqual(self.e.execute(i)['state'],'EXECUTION_REJECTED');self.assertEqual(before,self.e.balances)
    def test_deny_overrides_missing_information(self):
        a=self.a('S04-C');a.pop('jurisdiction',None)
        self.assertEqual(self.e.evaluate(a,'S04')['outcome'],'DENY')
    def test_policy_and_envelope_are_intersected(self):
        a=self.a('S01-A');self.e.policies['S01']['amount']['max_single_transaction_brl']=70000
        self.assertEqual(self.e.evaluate(a,'S01')['outcome'],'DENY')
    def test_threshold_boundary(self):
        a=self.a('S01-A');a['amount']=100000
        self.assertEqual(self.e.evaluate(a,'S01')['outcome'],'ALLOW')
        a['amount']=100001
        self.assertEqual(self.e.evaluate(a,'S01')['outcome'],'REQUIRE_APPROVAL')
    def test_unissued_and_tampered_instruction(self):
        a=self.a('S01-A');self.assertEqual(self.e.execute({'action':a,'sid':'S01'})['state'],'EXECUTION_REJECTED')
        i=self.e.authorize(a,'S01');i['action']['amount']=1
        self.assertEqual(self.e.execute(i)['state'],'EXECUTION_REJECTED');self.assertEqual(len(self.e.submissions),0)
    def test_audit_snapshots_and_hash_chain(self):
        a=self.a('S02-A');i=self.e.authorize(a,'S02',self.e.approve(a));snapshot=digest(self.e.audit)
        self.e.envelopes['S02']['revocation_status']='REVOKED'
        self.assertEqual(snapshot,digest(self.e.audit))
        for prev,nxt in zip(self.e.audit,self.e.audit[1:]):self.assertEqual(digest(prev),nxt['previous_event_hash'])
    def test_settlement_exception(self):
        a=self.a('S04-A');r=self.e.execute(self.e.authorize(a,'S04',self.e.approve(a)),settlement_delta=1)
        self.assertEqual(r['reconciliation'],'EXCEPTION');self.assertTrue(r['mismatches'])
    def test_envelope_expiry(self):
        a=self.a('S01-A');self.e.envelopes['S01']['valid_until']='2026-09-22T00:00:00Z'
        self.assertEqual(self.e.evaluate(a,'S01')['outcome'],'DENY')
if __name__=='__main__':unittest.main(verbosity=2)
