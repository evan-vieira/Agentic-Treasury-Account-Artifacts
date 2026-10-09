"""v1.2 output vocabulary and local validation; never repair a generated action."""
import math

COMMON_REQUIRED = ['action_id', 'principal_id', 'entity', 'action_type', 'source_account',
                   'amount', 'currency', 'asset', 'proposed_rail', 'treasury_state_ref']
OPTIONAL_STRINGS = ['destination_account', 'beneficiary', 'destination', 'counterparty',
                    'jurisdiction', 'sell_asset']
SCENARIO_REQUIRED = {'S01': ['destination_account'],
                     'S02': ['destination_account', 'counterparty', 'sell_asset'],
                     'S03': ['counterparty'], 'S04': ['beneficiary', 'destination']}
SEMANTICS = {
 'S01': [
  'amount is BRL transferred from source_account to destination_account; currency=asset=BRL.',
  'Use action_type INTRAGROUP_TRANSFER and the executive principal from authority_envelope, not the entity name.',
  'Choose the amount yourself from the stated objective, forecast, liquidity floors and authority.'],
 'S02': [
  'amount is the number of destination USD or USDC units to BUY, never the amount of BRL to sell. currency and asset are the purchased denomination; sell_asset is BRL.',
  'The BRL source debit is amount * quoted BRL per purchased unit * (1 + fee_bps/10000), rounded to cents. Assess available source cash and policy liquidity limits using that debit.',
  'bank_fx buys USD with action_type FX_CONVERSION; regulated_stablecoin_provider buys USDC with action_type STABLECOIN_CONVERSION.',
  'source_account holds BRL; destination_account holds the purchased asset for the same entity. counterparty is the selected rail provider ID; beneficiary is null or omitted, never the entity name.',
  'jurisdiction describes the provider country from counterparty data, not the currency country. State uncertainties and any human approval requirement in rationale; do not include approval or execute fields.'],
 'S03': [
  'action_type is INVEST_EXCESS_CASH. amount is USD cash invested, currency is USD, and asset is the chosen fund ID.',
  'counterparty is the fund provider matching the rail. A position is created by the simulator; no external destination_account is needed.',
  'The projected cash after investment equals forecast.projected_min_cash_before_investment minus amount. Choose amount/asset/rail yourself subject to supplied policy and authority.'],
 'S04': [
  'action_type is CROSS_BORDER_PAYMENT. amount and currency denote the settlement units sent; asset matches the settlement asset.',
  'beneficiary is the supplier ID named by the invoice. destination is its bank_destination for bank_wire_cross_border or wallet_destination for stablecoin_transfer. A country code is not a payment destination.',
  'counterparty, if supplied, is the rail provider ID from state.rails (BANK-SIM or CHAIN-SIM), not the supplier. Beneficiary permission is evaluated separately. destination_account is not used for an external payment.',
  'jurisdiction is a verified transaction fact, not inferred from identifiers, permitted jurisdiction lists or addresses. If unknown, abstain or propose with jurisdiction null/omitted for the Control Plane to request information; never invent it.']}


def action_schema(eng, sid):
    properties = {k: {'type': 'string', 'minLength': 1} for k in COMMON_REQUIRED if k != 'amount'}
    properties['amount'] = {'type': 'number', 'exclusiveMinimum': 0}
    properties['principal_id']['const'] = eng.envelopes[sid]['principal_id']
    properties['treasury_state_ref']['const'] = eng.version
    properties['action_type']['enum'] = eng.envelopes[sid]['actions']
    for k in OPTIONAL_STRINGS:
        properties[k] = {'type': ['string', 'null'], 'minLength': 1}
    for k in SCENARIO_REQUIRED[sid]:
        properties[k] = {'type': 'string', 'minLength': 1}
    return {'type': 'object', 'additionalProperties': False,
            'required': COMMON_REQUIRED + SCENARIO_REQUIRED[sid], 'properties': properties}


def contract(eng, sid, stage):
    advisory = {'type': 'object', 'additionalProperties': False, 'required': ['status', 'observations'],
      'properties': {'status': {'const': 'ADVISORY'},
                     'observations': {'type': 'array', 'items': {'type': 'string'}, 'minItems': 1}}}
    if stage != 'executive':
        return {'contract_version': 'v1.2', 'output_schema': advisory,
                'field_semantics_for_review': SEMANTICS[sid]}
    abstain = {'type': 'object', 'additionalProperties': False, 'required': ['status', 'reason'],
      'properties': {'status': {'const': 'ABSTAIN'}, 'reason': {'type': 'string', 'minLength': 1}}}
    propose = {'type': 'object', 'additionalProperties': False, 'required': ['status', 'action', 'rationale'],
      'properties': {'status': {'const': 'PROPOSE'}, 'action': action_schema(eng, sid),
                     'rationale': {'type': 'string', 'minLength': 1}}}
    return {'contract_version': 'v1.2', 'output_schema': {'oneOf': [propose, abstain]},
            'field_semantics': SEMANTICS[sid],
            'constraints': ['Return one JSON object. Do not rename enum values.',
             'Use the dataset_version as treasury_state_ref, not the market snapshot ID or timestamp.',
             'Do not include approval or execute fields. The executive cannot approve itself.',
             'No fixed amount, route or expected outcome is prescribed by this output contract.']}


def validate(value, schema, path='$'):
    """Validate exactly the JSON Schema subset generated above, including finite numbers."""
    errors = []
    if 'oneOf' in schema:
        variants = [validate(value, s, path) for s in schema['oneOf']]
        if sum(not e for e in variants) == 1:
            return []
        # Return the matching status branch errors to keep diagnostics useful.
        for s,e in zip(schema['oneOf'], variants):
            if isinstance(value, dict) and value.get('status') == s['properties']['status']['const']:
                return e or [path + ':ONE_OF_MISMATCH']
        return [path + ':INVALID_STATUS']
    if 'const' in schema and value != schema['const']:
        errors.append(path + ':CONST_MISMATCH')
    if 'enum' in schema and value not in schema['enum']:
        errors.append(path + ':INVALID_ENUM')
    checks = {'string': lambda x: isinstance(x, str), 'null': lambda x: x is None,
              'object': lambda x: isinstance(x, dict), 'array': lambda x: isinstance(x, list),
              'number': lambda x: isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)}
    types = schema.get('type')
    if types:
        allowed = types if isinstance(types, list) else [types]
        if not any(checks[t](value) for t in allowed):
            return errors + [path + ':INVALID_TYPE']
    if isinstance(value, str) and len(value) < schema.get('minLength', 0):
        errors.append(path + ':TOO_SHORT')
    if 'exclusiveMinimum' in schema and value <= schema['exclusiveMinimum']:
        errors.append(path + ':NOT_POSITIVE')
    if isinstance(value, dict) and 'properties' in schema:
        for k in schema.get('required', []):
            if k not in value:
                errors.append(path + '.' + k + ':MISSING')
        for k,v in value.items():
            if k in schema['properties']:
                errors.extend(validate(v, schema['properties'][k], path + '.' + k))
            elif schema.get('additionalProperties') is False:
                errors.append(path + '.' + k + ':UNEXPECTED_FIELD')
    if isinstance(value, list) and 'items' in schema:
        if len(value) < schema.get('minItems', 0):
            errors.append(path + ':TOO_FEW_ITEMS')
        for i,item in enumerate(value):
            errors.extend(validate(item, schema['items'], path + '[' + str(i) + ']'))
    return errors
