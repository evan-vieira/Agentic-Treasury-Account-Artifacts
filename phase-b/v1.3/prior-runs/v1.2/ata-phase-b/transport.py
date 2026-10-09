"""Versioned, auditable API transport. No changes to experimental prompts or scoring."""
import email.utils
import hashlib
import json
import os
import random
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

POLICY = {
    'minimum_start_interval_seconds': 15,
    'max_attempts_per_call': 6,
    'max_retry_elapsed_seconds': 600,
    'max_automatic_wait_seconds': 180,
    'backoff_base_seconds': 5,
    'backoff_cap_seconds': 120,
    'jitter_max_seconds': 1,
    'timeout_seconds': 90,
    'max_http_attempts_per_run': 100,
    'next_request_token_reserve': 7000,
    'retry_http_statuses': [429, 500, 502, 503, 504],
    'retry_transport_errors': True,
    'never_retry_http_200_content': True,
}


class DeferredCall(RuntimeError):
    pass


class TerminalModelOutput(ValueError):
    pass


def stamp():
    return datetime.now(timezone.utc).isoformat()


def write(path, value):
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str) + '\n')
    tmp.replace(path)


def raw_write(path, data):
    tmp = path.with_name(path.name + '.tmp')
    tmp.write_bytes(data)
    tmp.replace(path)


def seconds(value):
    """Read Retry-After seconds/date or x-ratelimit-reset durations."""
    if not value:
        return 0.0
    try:
        return max(0.0, float(value))
    except ValueError:
        pass
    parts = re.findall(r'(\d+(?:\.\d+)?)(ms|s|m|h)', value)
    if parts and ''.join(a + b for a, b in parts) == value:
        scales = {'ms': .001, 's': 1, 'm': 60, 'h': 3600}
        return sum(float(a) * scales[b] for a, b in parts)
    try:
        return max(0.0, email.utils.parsedate_to_datetime(value).timestamp() - time.time())
    except (TypeError, ValueError, OverflowError):
        return 0.0


def safe_headers(headers):
    return {k.lower(): v for k, v in headers.items()
            if k.lower().startswith('x-ratelimit-')
            or k.lower() in ('retry-after', 'x-request-id', 'date', 'content-type')}


def read_json(path):
    return json.loads(path.read_text())


def wait_until(deadline):
    while deadline > time.time():
        time.sleep(max(0, min(1, deadline - time.time())))


def decode_success(attempt, request):
    if read_json(attempt / 'request.json') != request:
        raise RuntimeError('Checkpoint request mismatch; refusing reuse')
    meta = read_json(attempt / 'meta.json')
    raw = (attempt / 'response.raw.json').read_bytes()
    if hashlib.sha256(raw).hexdigest() != meta['raw_response_sha256']:
        raise RuntimeError('Raw response checksum mismatch')
    try:
        envelope = json.loads(raw)
        content = envelope['choices'][0]['message']['content']
        if not isinstance(content, str):
            raise ValueError('No text JSON returned')
        parsed = json.loads(content)
        if not isinstance(parsed, dict):
            raise ValueError('Model JSON is not an object')
    except (ValueError, KeyError, IndexError, TypeError) as exc:
        if not (attempt / 'parse-error.json').exists():
            write(attempt / 'parse-error.json', {'at': stamp(), 'error_type': type(exc).__name__,
                                                'error': str(exc), 'retry': False})
        raise TerminalModelOutput('HTTP 200 content invalid; retained without regeneration') from exc
    if not (attempt / 'parsed.json').exists():
        write(attempt / 'parsed.json', parsed)
    return parsed, {'response_model': envelope.get('model'), 'usage': envelope.get('usage'),
                    'attempt': attempt.name, **meta}


def retryable(status, body, policy):
    if status == 0:
        return policy['retry_transport_errors']
    if status not in policy['retry_http_statuses']:
        return False
    if status == 429:
        try:
            err = json.loads(body).get('error', {})
            code = str(err.get('code', '')) + ' ' + str(err.get('type', ''))
        except (ValueError, AttributeError):
            return False
        # Unknown 429s are not assumed to be transient quota errors.
        return any(x in code for x in ('rate_limit', 'slow_down')) and not any(
            x in code for x in ('quota', 'billing', 'spend', 'credit'))
    return True


def call_model(freeze, messages, outdir, label):
    request = {'model': freeze['model'], 'messages': messages, **freeze['parameters']}
    policy = freeze['transport_policy']
    rundir = outdir.parent
    call = outdir / 'calls' / label
    call.mkdir(parents=True, exist_ok=True)
    reqpath = call / 'request.json'
    if reqpath.exists():
        if read_json(reqpath) != request:
            raise RuntimeError('Frozen logical request changed')
    else:
        write(reqpath, request)
    attempts = sorted(call.glob('attempt-*'))
    for attempt in attempts:
        if not (attempt / 'meta.json').exists():
            # Do not regenerate after a crash with unknown delivery/response status.
            raise DeferredCall('Incomplete attempt requires review: ' + str(attempt))
        if read_json(attempt / 'request.json') != request:
            raise RuntimeError('Attempt request changed')
        if read_json(attempt / 'meta.json')['http_status'] == 200:
            return decode_success(attempt, request)
    if attempts and not read_json(attempts[-1] / 'meta.json')['retryable']:
        raise DeferredCall('Non-retryable API error retained; user action required')
    if len(attempts) >= policy['max_attempts_per_call']:
        raise DeferredCall('Attempt limit reached; no further regeneration')
    first_epoch = (read_json(attempts[0] / 'meta.json')['started_epoch'] if attempts else None)
    while len(attempts) < policy['max_attempts_per_call']:
        if len(list(rundir.glob('B*/calls/*/attempt-*'))) >= policy['max_http_attempts_per_run']:
            raise DeferredCall('Frozen total HTTP attempt budget reached')
        pacefile = rundir / 'transport-state.json'
        deadline = read_json(pacefile)['next_start_epoch'] if pacefile.exists() else 0
        if attempts:
            deadline = max(deadline, read_json(attempts[-1] / 'meta.json')['retry_not_before_epoch'])
        delay = max(0, deadline - time.time())
        if delay > policy['max_automatic_wait_seconds']:
            raise DeferredCall('Server delay exceeds automatic wait; resume after deadline')
        if first_epoch is not None and max(deadline, time.time()) - first_epoch > policy['max_retry_elapsed_seconds']:
            raise DeferredCall('Frozen retry time budget reached')
        wait_until(deadline)
        attempt = call / ('attempt-%03d' % (len(attempts) + 1))
        attempt.mkdir()
        write(attempt / 'request.json', request)
        started = stamp(); epoch = time.time()
        if first_epoch is None:
            first_epoch = epoch
        write(attempt / 'started.json', {'at': started, 'epoch': epoch})
        write(pacefile, {'next_start_epoch': epoch + policy['minimum_start_interval_seconds']})
        req = urllib.request.Request(freeze['endpoint'], json.dumps(request).encode(),
            {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + os.environ['OPENAI_API_KEY']})
        print(outdir.name + ' ' + label + ' ' + attempt.name, flush=True)
        headers = {}; transport_error = None
        try:
            with urllib.request.urlopen(req, timeout=policy['timeout_seconds']) as response:
                raw = response.read(); status = response.status
                headers = safe_headers(response.headers)
        except urllib.error.HTTPError as exc:
            raw = exc.read(); status = exc.code; headers = safe_headers(exc.headers)
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as exc:
            transport_error = {'transport_error': type(exc).__name__, 'message': str(exc),
                               'remote_completion_unknown': True}
            raw = json.dumps(transport_error).encode(); status = 0
        raw_write(attempt / 'response.raw.json', raw)
        finished = time.time()
        retry = retryable(status, raw, policy)
        server_wait = seconds(headers.get('retry-after'))
        rate_wait = 0
        for kind, reserve in [('tokens', policy['next_request_token_reserve']), ('requests', 1),
                              ('project-tokens', policy['next_request_token_reserve'])]:
            remaining = headers.get('x-ratelimit-remaining-' + kind)
            if remaining is not None:
                try:
                    if float(remaining) < reserve:
                        rate_wait = max(rate_wait, seconds(headers.get('x-ratelimit-reset-' + kind)))
                except ValueError:
                    pass
        backoff = min(policy['backoff_cap_seconds'], policy['backoff_base_seconds'] * 2 ** len(attempts))
        retry_wait = max(server_wait, rate_wait, backoff) + random.uniform(0, policy['jitter_max_seconds']) if retry else 0
        meta = {'started_at': started, 'finished_at': stamp(), 'started_epoch': epoch,
                'http_status': status, 'response_headers': headers, 'retryable': retry,
                'raw_response_sha256': hashlib.sha256(raw).hexdigest(),
                'retry_not_before_epoch': finished + retry_wait,
                'transport_response_is_synthetic_error_record': transport_error is not None}
        write(attempt / 'meta.json', meta)
        write(pacefile, {'next_start_epoch': max(epoch + policy['minimum_start_interval_seconds'],
                                               finished + rate_wait, finished + server_wait)})
        attempts.append(attempt)
        if status == 200:
            return decode_success(attempt, request)
        write(attempt / 'error.json', {'at': stamp(), 'http_status': status, 'retryable': retry,
                                      'transport_error': transport_error})
        if not retry:
            raise DeferredCall('Non-retryable API error HTTP ' + str(status))
    raise DeferredCall('Frozen per-call retry limit reached')
