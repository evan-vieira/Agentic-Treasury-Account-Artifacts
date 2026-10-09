"""Deterministic research simulator. No network, keys, LLMs or real payment rails.
The evaluator never reads expected outcomes. All monetary arithmetic is Decimal.
Trust and authentication are simulated in-process, not production security.
"""
from copy import deepcopy
from decimal import Decimal, InvalidOperation
from datetime import datetime
import csv, json, hashlib
from pathlib import Path
import yaml

D = lambda v: Decimal(str(v))
def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), default=str)
def digest(obj):
    return hashlib.sha256(canonical(obj).encode()).hexdigest()
def ts(s):
    return datetime.fromisoformat(str(s).replace('Z', '+00:00'))
def read_yaml(p):
    return yaml.safe_load(p.read_text())
def rows(p):
    with p.open() as f: return list(csv.DictReader(f))

class Engine:
    def __init__(self, root):
        self.root = Path(root)
        self.protocol = read_yaml(self.root/'metadata/protocol.yaml')
        self.now = self.protocol['canonical_timestamp']
        self.version = self.protocol['dataset_version']
        self.accounts = {r['account_id']: r for r in rows(self.root/'dataset/accounts.csv')}
        self.balances = {r['account_id']: D(r['amount']) for r in rows(self.root/'dataset/balances.csv')}
        self.balance_times = {r['account_id']: r['as_of'] for r in rows(self.root/'dataset/balances.csv')}
        self.forecasts = {r['forecast_id']: r for r in rows(self.root/'dataset/forecast.csv')}
        self.counterparties = {r['counterparty_id']: r for r in rows(self.root/'dataset/counterparties.csv')}
        self.assets = {r['asset_id']: r for r in rows(self.root/'dataset/assets.csv')}
        self.rails = {r['rail_id']: r for r in read_yaml(self.root/'dataset/rails.yaml')['rails']}
        self.market = read_yaml(self.root/'dataset/market_snapshot.yaml')
        self.common = read_yaml(self.root/'policies/common-data-policy.yaml')
        self.policies = {}; self.envelopes = {}
        for sid, p, a in [('S01','liquidity','liquidity'),('S02','fx','fx'),('S03','yield','yield'),('S04','cross-border','payments')]:
            self.policies[sid] = read_yaml(self.root/f'policies/{p}-policy.yaml')
            self.envelopes[sid] = read_yaml(self.root/f'authority/{a}-agent-envelope.yaml')
        self.state_time = self.now
        self.audit = []; self.issued = {}; self.used = set(); self.positions = {}
        self.unavailable = set(); self.extra_denials = set(); self.submissions = []
        self.approvers = {'USER-TREASURY-01':'treasury_manager'}

    def event(self, stage, a, outcome, reasons=(), **data):
        e={'event_id':f'EVT-{len(self.audit)+1:04d}', 'timestamp':self.now,
           'correlation_id':a.get('action_id','INVALID'), 'stage':stage,
           'actor_id':{'APPROVAL':'USER-TREASURY-01','EXECUTION':'SIMULATED-ADAPTER','RECONCILIATION':'RECONCILER'}.get(stage,'ATA-CONTROL-PLANE'),
           'action_hash':digest(a),'dataset_version':self.version,
           'outcome':outcome,'reason_codes':list(reasons),'evidence':data,
           'previous_event_hash':digest(self.audit[-1]) if self.audit else None}
        self.audit.append(deepcopy(e))
        return e['event_id']

    def context(self, sid):
        return {'now':self.now,'dataset_version':self.version,'state_time':self.state_time,
                'balances':self.balances,'balance_times':self.balance_times,'forecasts':self.forecasts,
                'accounts':self.accounts,'counterparties':self.counterparties,'assets':self.assets,
                'rails':self.rails,'market':self.market,'policy':self.policies[sid],
                'common_policy':self.common,'authority':self.envelopes[sid],
                'extra_denials':sorted(self.extra_denials)}

    def evaluate(self, a, sid, approval=None):
        p=self.policies[sid]; e=self.envelopes[sid]; deny=[]; missing=[]
        def bad(code):
            if code not in deny: deny.append(code)
        def lack(code):
            if code not in missing: missing.append(code)
        required=['action_id','principal_id','entity','action_type','source_account','amount','currency','asset','proposed_rail','treasury_state_ref']
        for k in required:
            if a.get(k) in (None,''): lack('MISSING_'+k.upper())
        try:
            amount=D(a.get('amount',0))
            if not amount.is_finite() or amount<=0: raise InvalidOperation
        except (InvalidOperation,ValueError,TypeError):
            lack('INVALID_AMOUNT'); amount=D(0)
        if a.get('principal_id')!=e['principal_id']: bad('PRINCIPAL_NOT_AUTHORIZED')
        if e['revocation_status']!='ACTIVE': bad('AUTHORITY_REVOKED')
        if not ts(e['valid_from'])<=ts(self.now)<=ts(e['valid_until']): bad('AUTHORITY_OUTSIDE_VALIDITY')
        if p['status']!='ACTIVE' or self.common['status']!='ACTIVE': bad('POLICY_INACTIVE')
        max_age=self.common['data_requirements']['treasury_state_max_age_seconds']
        if (ts(self.now)-ts(self.state_time)).total_seconds()>max_age: lack('STALE_TREASURY_STATE')
        if a.get('treasury_state_ref')!=self.version: lack('UNKNOWN_TREASURY_STATE')
        for k, allowed in [('entity',e['entity_scope']),('action_type',e['actions'])]:
            if a.get(k) not in allowed: bad(k.upper()+'_OUTSIDE_AUTHORITY')
        if a.get('entity') not in p['scope']['entities'] or a.get('action_type') not in p['scope']['actions']: bad('POLICY_SCOPE_MISMATCH')
        if a.get('currency') not in e['currencies']: bad('CURRENCY_NOT_PERMITTED')
        asset=a.get('asset'); rail=a.get('proposed_rail')
        if asset not in self.assets or self.assets[asset]['approved_for_treasury']!='True': bad('ASSET_NOT_APPROVED')
        if 'permitted_assets' in e and asset not in e['permitted_assets']: bad('ASSET_OUTSIDE_AUTHORITY')
        if 'assets' in p and asset not in p['assets']['permitted']: bad('ASSET_POLICY_PROHIBITION')
        cp_id=a.get('beneficiary') or a.get('counterparty'); cp=self.counterparties.get(cp_id)
        if sid!='S01':
            if not cp or cp['approved']!='True': bad('COUNTERPARTY_NOT_APPROVED')
            if cp_id not in e['permitted_counterparties']: bad('COUNTERPARTY_OUTSIDE_AUTHORITY')
        if 'jurisdictions' in e:
            jurisdiction=a.get('jurisdiction')
            if not jurisdiction: lack('MISSING_JURISDICTION')
            else:
                if jurisdiction not in e['jurisdictions']: bad('JURISDICTION_OUTSIDE_AUTHORITY')
                if 'jurisdictions' in p and jurisdiction not in p['jurisdictions']['permitted']: bad('JURISDICTION_POLICY_PROHIBITION')
                if cp and jurisdiction!=cp['country']: bad('JURISDICTION_COUNTERPARTY_MISMATCH')
        max_authority=next(D(v) for k,v in e.items() if k.startswith('max_amount'))
        if amount>max_authority: bad('AMOUNT_EXCEEDS_AUTHORITY')
        maximum=next(D(v) for k,v in p['amount'].items() if k.startswith('max_single'))
        if amount>maximum: bad('AMOUNT_EXCEEDS_POLICY')
        source=a.get('source_account'); account=self.accounts.get(source)
        if not account: lack('UNKNOWN_SOURCE_ACCOUNT')
        else:
            if account['approved']!='True': bad('SOURCE_ACCOUNT_NOT_APPROVED')
            if account['entity_id']!=a.get('entity'): bad('SOURCE_ENTITY_MISMATCH')
            source_asset='BRL' if sid=='S02' else ('USD' if sid=='S03' else a.get('asset'))
            if account['currency']!=source_asset: bad('SOURCE_CURRENCY_MISMATCH')
            age=(ts(self.now)-ts(self.balance_times[source])).total_seconds()
            if age>max_age or age<0: lack('STALE_OR_FUTURE_BALANCE')
        if sid=='S01':
            dest=self.accounts.get(a.get('destination_account'))
            if not dest: lack('UNKNOWN_DESTINATION_ACCOUNT')
            else:
                if dest['approved']!='True': bad('DESTINATION_NOT_APPROVED')
                if dest['entity_id']!=a.get('entity'): bad('CROSS_ENTITY_TRANSFER_NOT_SUPPORTED')
                if dest['currency']!=a.get('currency'): bad('DESTINATION_CURRENCY_MISMATCH')
            if source in self.balances and self.balances[source]-amount<D(p['liquidity']['source_min_post_execution_brl']): bad('SOURCE_LIQUIDITY_BREACH')
            fc=self.forecasts['FC-BR-BRL-001']
            if D(fc['projected_balance_before_action'])+amount<D(p['liquidity']['destination_min_required_brl']): bad('DESTINATION_PROJECTED_LIQUIDITY_BREACH')
        if sid=='S02':
            dest=self.accounts.get(a.get('destination_account'))
            if not dest: lack('UNKNOWN_DESTINATION_ACCOUNT')
            elif dest['approved']!='True' or dest['entity_id']!=a.get('entity') or dest['currency']!=asset: bad('FX_DESTINATION_INVALID')
            if a.get('sell_asset') not in p['currencies']['sell'] or asset not in p['currencies']['buy']: bad('FX_CURRENCY_PAIR_NOT_PERMITTED')
            quote=next((q for q in self.market['fx_quotes'] if q['rail_id']==rail),None)
            if not quote: lack('MISSING_FX_QUOTE')
            else:
                rate=D(quote.get('brl_per_usd',quote.get('brl_per_usdc')))
                cost=(amount*rate*(1+D(quote['fee_bps'])/10000)).quantize(D('.01'))
                if source in self.balances and self.balances[source]<cost: bad('INSUFFICIENT_SOURCE_FUNDS')
                total=sum(v for k,v in self.balances.items() if self.accounts[k]['currency']=='BRL')
                if total-cost<D(p['liquidity']['min_group_brl_post_execution']): bad('GROUP_BRL_LIQUIDITY_BREACH')
        else:
            if source in self.balances and self.balances[source]<amount: bad('INSUFFICIENT_SOURCE_FUNDS')
        if sid=='S03':
            projected=D(self.forecasts['FC-US-USD-001']['projected_min_cash_before_investment'])-amount
            if projected<D(p['liquidity']['min_projected_cash_post_investment_usd']): bad('PROJECTED_LIQUIDITY_BREACH')
        if sid=='S04' and cp:
            field='wallet_destination' if rail=='stablecoin_transfer' else 'bank_destination'
            if a.get('destination')!=cp[field]: bad('BENEFICIARY_DESTINATION_MISMATCH')
        if rail not in e['permitted_rails']: bad('RAIL_OUTSIDE_AUTHORITY')
        if 'rails' in p and rail not in p['rails']['permitted']: bad('RAIL_POLICY_PROHIBITION')
        r=self.rails.get(rail)
        if not r: bad('RAIL_NOT_REGISTERED')
        elif 'supported_assets' in r and asset not in r['supported_assets']: bad('RAIL_ASSET_MISMATCH')
        elif 'supported_pairs' in r and f"{a.get('sell_asset')}/{asset}" not in r['supported_pairs']: bad('RAIL_PAIR_MISMATCH')
        if asset in self.extra_denials: bad('MANDATORY_POLICY_CONFLICT_FAIL_CLOSED')
        valid_approval=False
        if approval:
            if approval.get('approver_id')==a.get('principal_id'): bad('SEGREGATION_OF_DUTIES_VIOLATION')
            role=self.approvers.get(approval.get('approver_id'))
            valid_approval=(role in p['approval']['eligible_roles'] and approval.get('action_hash')==digest(a)
                and approval.get('decision')=='APPROVE' and ts(approval['issued_at'])<=ts(self.now)<ts(approval['expires_at'])
                and amount<=D(approval['max_amount']) and approval.get('currency')==a.get('currency'))
        threshold=min(next(D(v) for k,v in p['approval'].items() if k.startswith('required_above')),next(D(v) for v in e['approval_requirement'].values()))
        if deny: outcome='DENY'; reasons=deny+missing
        elif missing: outcome='REQUIRE_ADDITIONAL_INFORMATION'; reasons=missing
        elif amount>threshold and not valid_approval:
            outcome='REQUIRE_APPROVAL'; reasons=['HUMAN_APPROVAL_REQUIRED']
            if approval: reasons.append('APPROVAL_INVALID_OR_EXPIRED')
        else: outcome='ALLOW'; reasons=['ALL_REQUIRED_CONTROLS_SATISFIED']
        decision={'outcome':outcome,'reason_codes':reasons,'action_hash':digest(a),'authority_envelope_id':e['envelope_id'],
                  'authority_version':e['version'],'policy_versions':{p['policy_id']:p['version'],self.common['policy_id']:self.common['version']},
                  'context_hash':digest(self.context(sid))}
        self.event('POLICY_EVALUATION',a,outcome,reasons,decision=decision,inputs={'action':a,'approval':approval,'context':self.context(sid)})
        return decision

    def approve(self,a,approver='USER-TREASURY-01'):
        approval={'approval_id':'APR-'+digest(a)[:16],'version':'1.0','action_hash':digest(a),'action_id':a['action_id'],
                  'approver_id':approver,'decision':'APPROVE','issued_at':self.now,'expires_at':'2026-09-23T16:00:00Z',
                  'max_amount':a['amount'],'currency':a['currency']}
        self.event('APPROVAL',a,'APPROVAL_RECORDED',approval=approval)
        return approval

    def authorize(self,a,sid,approval=None):
        decision=self.evaluate(a,sid,approval)
        if decision['outcome']!='ALLOW': return None
        ins={'instruction_id':'INS-'+digest(a)[:20],'action':deepcopy(a),'sid':sid,'approval':deepcopy(approval),
             'action_hash':digest(a),'decision':decision,'expires_at':'2026-09-23T16:00:00Z','idempotency_key':digest(a)}
        self.issued[ins['instruction_id']]=digest(ins)
        self.event('AUTHORIZATION',a,'AUTHORIZED',instruction=ins)
        return ins

    def execute(self,ins,settlement_delta=0):
        if not ins: return {'state':'EXECUTION_REJECTED','reason':'NO_AUTHORIZED_INSTRUCTION','reconciliation':'N/A'}
        a=ins.get('action',{});sid=ins.get('sid');iid=ins.get('instruction_id')
        def reject(state,reason):
            self.event('EXECUTION_GATE',a,state,[reason]);return {'state':state,'reason':reason,'reconciliation':'N/A'}
        if iid not in self.issued or self.issued[iid]!=digest(ins): return reject('EXECUTION_REJECTED','UNISSUED_OR_TAMPERED_INSTRUCTION')
        if ins['idempotency_key'] in self.used: return reject('EXECUTION_REJECTED','DUPLICATE_INSTRUCTION')
        if ts(self.now)>=ts(ins['expires_at']): return reject('EXECUTION_REJECTED','EXPIRED_INSTRUCTION')
        if a['proposed_rail'] in self.unavailable: return reject('RE_EVALUATION_REQUIRED','RAIL_UNAVAILABLE_NO_FALLBACK')
        if self.evaluate(a,sid,ins['approval'])['outcome']!='ALLOW': return reject('EXECUTION_REJECTED','EXECUTION_TIME_GOVERNANCE_FAILED')
        provider=a.get('counterparty')
        rail=self.rails[a['proposed_rail']]
        if provider and provider!=rail['provider']: return reject('EXECUTION_VALIDATION_FAIL','PROVIDER_RAIL_MISMATCH')
        before=deepcopy(self.balances);expected=deepcopy(before);amount=D(a['amount']);source=a['source_account']
        postings=[]
        def post(account,delta):
            expected[account]=expected.get(account,D(0))+delta;postings.append({'account':account,'delta':str(delta)})
        if sid=='S01': post(source,-amount);post(a['destination_account'],amount)
        elif sid=='S02':
            q=next(q for q in self.market['fx_quotes'] if q['rail_id']==a['proposed_rail'])
            cost=(amount*D(q.get('brl_per_usd',q.get('brl_per_usdc')))*(1+D(q['fee_bps'])/10000)).quantize(D('.01'))
            post(source,-cost);post(a['destination_account'],amount)
        elif sid=='S03': post(source,-amount);post('POSITION:'+a['asset'],amount)
        else: post(source,-amount);post('EXTERNAL:'+a['destination'],amount)
        self.used.add(ins['idempotency_key']);self.submissions.append({'instruction_id':iid,'authorization_outcome':'ALLOW'})
        self.event('EXECUTION',a,'SUBMITTED',instruction_id=iid,postings=postings)
        # Adapter receipt is synthesized from requested postings; injected faults perturb it.
        observed=deepcopy(before)
        for entry in postings: observed[entry['account']]=observed.get(entry['account'],D(0))+D(entry['delta'])
        if settlement_delta: observed[source]+=D(settlement_delta)
        receipt={'receipt_id':'SET-'+iid,'rail':a['proposed_rail'],'instruction_id':iid,'observed_balances':observed}
        self.event('SETTLEMENT',a,'SETTLED',receipt=receipt)
        mismatches={k:{'expected':str(expected.get(k,0)),'observed':str(observed.get(k,0))} for k in set(expected)|set(observed) if expected.get(k,0)!=observed.get(k,0)}
        recon='EXCEPTION' if mismatches else 'RECONCILED'
        self.balances={k:v for k,v in observed.items() if k in self.accounts}
        self.event('RECONCILIATION',a,recon,mismatches=mismatches,expected_balances=expected,observed_balances=observed)
        return {'state':'SUCCESS','reconciliation':recon,'receipt':receipt,'expected_balances':expected,'mismatches':mismatches}
