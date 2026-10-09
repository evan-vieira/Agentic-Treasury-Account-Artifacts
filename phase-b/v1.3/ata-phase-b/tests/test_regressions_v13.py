"""Offline regression tests for previously observed omissions and arithmetic errors."""
import copy,json,tempfile,unittest,sys
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from test_experiment import fixture
import phase_b as pb
from contracts import contract,validate
from calculations import expected_calculations,check_claims

class RegressionTests(unittest.TestCase):
    def setUp(self):self.eng=pb.Engine(pb.BASE)
    def test_fx_jurisdiction_missing_or_null_rejected(self):
        for omit in (True,False):
            a=fixture('S02')
            if omit:del a['action']['jurisdiction']
            else:a['action']['jurisdiction']=None
            self.assertTrue(validate(a,contract(self.eng,'S02','executive')['output_schema']))
            normalized,errors=pb.inspect_action(a,self.eng,'S02','B02')
            self.assertIsNone(normalized);self.assertTrue(errors)
    def test_fx_provider_country_must_match(self):
        a=fixture('S02');a['action']['jurisdiction']='US'
        self.assertTrue(validate(a,contract(self.eng,'S02','executive')['output_schema']))
    def test_both_fx_routes_accepted_but_mixed_fields_rejected(self):
        a=fixture('S02');schema=contract(self.eng,'S02','executive')['output_schema']
        self.assertEqual(validate(a,schema),[])
        a['action'].update(action_type='STABLECOIN_CONVERSION',asset='USDC',currency='USDC',
            proposed_rail='regulated_stablecoin_provider',counterparty='SC-PROV-01',destination_account='WAL-BR-USDC-01')
        self.assertEqual(validate(a,schema),[])
        a['action']['currency']='USD'
        self.assertTrue(validate(a,schema))
    def test_exact_fx_costs_and_cash(self):
        a=fixture('S02')
        self.assertEqual(expected_calculations(self.eng,'S02',a),{
            'source_debit_brl':'2434860.00','source_balance_after_brl':'845140.00','group_brl_after':'3295140.00'})
        a['action']['proposed_rail']='regulated_stablecoin_provider'
        self.assertEqual(expected_calculations(self.eng,'S02',a)['source_debit_brl'],'2433989.25')
    def test_investment_forecast_is_before_not_after(self):
        self.assertEqual(expected_calculations(self.eng,'S03',fixture('S03')),{
            'projected_cash_before_usd':'825000.00','investment_usd':'175000.00','projected_cash_after_usd':'650000.00'})
    def test_previous_arithmetic_errors_flagged(self):
        for sid,field,bad in [('S02','source_debit_brl','2433300.00'),('S03','projected_cash_after_usd','825000.00')]:
            source=fixture(sid);answer={'status':'ADVISORY','observations':['offline'],
                'calculations':expected_calculations(self.eng,sid,source)}
            self.assertTrue(check_claims(self.eng,sid,answer,source,'governance')['matched'])
            answer['calculations'][field]=bad
            report=check_claims(self.eng,sid,answer,source,'governance')
            self.assertFalse(report['matched']);self.assertIn('CALCULATION_MISMATCH:'+field,report['errors'])
    def test_governance_sees_reference_without_action_repair(self):
        source=fixture('S02');unchanged=copy.deepcopy(source)
        data=pb.context(self.eng,'S02','base')
        msgs=pb.prompt('Treasury Governance and Controls','S02','B02','base',data,[], 'governance',source)
        m=json.loads(msgs[1]['content'])
        self.assertEqual(m['executive_contract_errors'],[])
        self.assertEqual(m['verified_calculations']['source_debit_brl'],'2434860.00')
        self.assertEqual(source,unchanged)
        self.assertEqual(data['transaction_facts']['provider_jurisdictions']['FX-PROV-01'],'BR')
    def test_abstain_has_no_fabricated_calculations(self):
        source={'status':'ABSTAIN','reason':'offline'}
        self.assertIsNone(expected_calculations(self.eng,'S02',source))
        report=check_claims(self.eng,'S02',{'status':'ADVISORY','observations':['offline'],'calculations':None},source,'governance')
        self.assertFalse(report['applicable']);self.assertEqual(report['errors'],[])
    def test_structured_decimal_format(self):
        out={'status':'ADVISORY','observations':['offline'],'calculations':expected_calculations(self.eng,'S02',fixture('S02'))}
        schema=contract(self.eng,'S02','governance')['output_schema']
        self.assertEqual(validate(out,schema),[])
        out['calculations']['source_debit_brl']='2,434,860'
        self.assertTrue(validate(out,schema))
    def test_checked_arithmetic_matches_engine_receipt(self):
        for sid in ('S02','S03'):
            eng=pb.Engine(pb.BASE);obj=fixture(sid)
            expected=expected_calculations(eng,sid,obj)
            action,_=pb.inspect_action(obj,eng,sid,'B02')
            approval=eng.approve(action);instruction=eng.authorize(action,sid,approval)
            result=eng.execute(instruction);self.assertEqual(result['state'],'SUCCESS')
            if sid=='S02':
                self.assertEqual(format(result['receipt']['observed_balances'][action['source_account']],'.2f'),expected['source_balance_after_brl'])
            else:
                self.assertEqual(expected['projected_cash_after_usd'],'650000.00')

if __name__=='__main__':unittest.main()
