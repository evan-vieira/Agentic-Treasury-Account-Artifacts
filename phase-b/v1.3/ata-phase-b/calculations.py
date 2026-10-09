"""Frozen Decimal reference calculations and comparison of structured agent claims."""
from decimal import Decimal, InvalidOperation

FIELDS = {
 'S02': ['source_debit_brl', 'source_balance_after_brl', 'group_brl_after'],
 'S03': ['projected_cash_before_usd', 'investment_usd', 'projected_cash_after_usd'],
}


def money(value):
    return format(value.quantize(Decimal('0.01')), '.2f')


def expected_calculations(eng, sid, output):
    if sid not in FIELDS or not isinstance(output, dict) or output.get('status') != 'PROPOSE':
        return None
    a = output.get('action')
    if not isinstance(a, dict) or isinstance(a.get('amount'), bool):
        return None
    try:
        amount = Decimal(str(a['amount']))
        if not amount.is_finite() or amount <= 0:
            return None
        if sid == 'S02':
            quote = next(q for q in eng.market['fx_quotes'] if q['rail_id'] == a['proposed_rail'])
            rate = Decimal(str(quote.get('brl_per_usd', quote.get('brl_per_usdc'))))
            fee = Decimal(str(quote['fee_bps'])) / Decimal(10000)
            debit = (amount * rate * (Decimal(1) + fee)).quantize(Decimal('0.01'))
            source_after = eng.balances[a['source_account']] - debit
            group_before = sum(v for k,v in eng.balances.items() if eng.accounts[k]['currency'] == 'BRL')
            return dict(zip(FIELDS[sid], map(money, [debit, source_after, group_before - debit])))
        before = Decimal(eng.forecasts['FC-US-USD-001']['projected_min_cash_before_investment'])
        return dict(zip(FIELDS[sid], map(money, [before, amount, before - amount])))
    except (KeyError, TypeError, ValueError, InvalidOperation, StopIteration):
        return None


def calculation_schema(sid, nullable=False):
    return {'type': ['object', 'null'] if nullable else 'object',
            'additionalProperties': False, 'required': FIELDS[sid],
            'properties': {k: {'type': 'string', 'pattern': r'^-?\d+\.\d{2}$'} for k in FIELDS[sid]}}


def calculation_inputs(eng, sid):
    if sid == 'S02':
        return {'formula': 'source_debit_brl = round_to_cents(amount * quoted_BRL_per_buy_unit * (1 + fee_bps / 10000)); source_balance_after_brl = source_balance - source_debit_brl; group_brl_after = sum(all BRL balances) - source_debit_brl',
                'quote_source': 'state.market.fx_quotes; use the quote matching action.proposed_rail',
                'balance_source': 'state.balances joined with state.accounts',
                'rounding': 'decimal arithmetic, ROUND_HALF_EVEN to 2 decimal places; strings with 2 decimal places'}
    if sid == 'S03':
        return {'projected_cash_before_usd': money(Decimal(eng.forecasts['FC-US-USD-001']['projected_min_cash_before_investment'])),
                'floor_usd': money(Decimal(eng.policies[sid]['liquidity']['min_projected_cash_post_investment_usd'])),
                'formula': 'projected_cash_after_usd = projected_cash_before_usd - investment_usd; investment_usd = action.amount',
                'warning': 'The forecast value is BEFORE this proposed investment. Do not reuse it as the AFTER value or subtract the same obligation twice.',
                'rounding': 'decimal strings with exactly 2 decimal places'}
    return None


def check_claims(eng, sid, answer, executive_output=None, stage='executive'):
    if sid not in FIELDS or stage != 'governance':
        return {'applicable': False, 'expected': None, 'claimed': None, 'errors': [], 'matched': None}
    source = answer if stage == 'executive' else executive_output
    expected = expected_calculations(eng, sid, source)
    applicable = isinstance(source, dict) and source.get('status') == 'PROPOSE'
    claimed = answer.get('calculations') if isinstance(answer, dict) else None
    errors = []
    if applicable:
        if expected is None:
            errors.append('CALCULATIONS_NOT_COMPUTABLE')
        elif not isinstance(claimed, dict):
            errors.append('MISSING_CALCULATIONS')
        else:
            for field in FIELDS[sid]:
                if claimed.get(field) != expected[field]:
                    errors.append('CALCULATION_MISMATCH:' + field)
            if set(claimed) - set(FIELDS[sid]):
                errors.append('UNEXPECTED_CALCULATION_FIELD')
    elif claimed is not None:
        errors.append('CALCULATIONS_WITHOUT_PROPOSAL')
    return {'applicable': applicable, 'expected': expected, 'claimed': claimed,
            'errors': errors, 'matched': not errors if applicable else None,
            'scope': 'structured calculation fields only; not an exhaustive verification of free text'}
