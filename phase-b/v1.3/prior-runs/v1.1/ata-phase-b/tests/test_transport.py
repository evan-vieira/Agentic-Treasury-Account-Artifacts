"""Offline simulated transport tests; no empirical model responses."""
import ast
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import urllib.error
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import transport as t

GOOD = json.dumps({'model':'offline-test-only','choices':[{'message':{'content':'{"status":"ABSTAIN","reason":"offline test"}'}}]}).encode()
class Response:
    def __init__(self, data=GOOD, headers=None):
        self.data=data;self.headers=headers or {};self.status=200
    def __enter__(self): return self
    def __exit__(self,*args): pass
    def read(self): return self.data

def http_error(code=429, error_code='rate_limit_exceeded', headers=None):
    return urllib.error.HTTPError('https://example.invalid',code,'offline simulated error',headers or {},io.BytesIO(json.dumps({'error':{'code':error_code}}).encode()))

class TransportTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.case=Path(self.tmp.name)/'run'/'B01';self.case.mkdir(parents=True)
        self.freeze={'model':'offline-test-only','parameters':{},'endpoint':'https://example.invalid','transport_policy':dict(t.POLICY)}
        self.clock=1000.0
        self.env=patch.dict(os.environ,OPENAI_API_KEY='offline-test-placeholder');self.env.start();self.addCleanup(self.env.stop)
        self.tp=patch.object(t.time,'time',side_effect=lambda:self.clock);self.tp.start();self.addCleanup(self.tp.stop)
        self.sp=patch.object(t.time,'sleep',side_effect=self.sleep);self.sp.start();self.addCleanup(self.sp.stop)
        self.jp=patch.object(t.random,'uniform',return_value=0);self.jp.start();self.addCleanup(self.jp.stop)
    def sleep(self,n): self.clock+=n
    def call(self,label='role',messages=None):return t.call_model(self.freeze,messages or [],self.case,label)
    def test_429_retry_archive_and_resume_no_regeneration(self):
        with patch.object(t.urllib.request,'urlopen',side_effect=[http_error(headers={'Retry-After':'20'}),Response()]) as api:
            value,_=self.call();self.assertEqual(api.call_count,2);self.assertGreaterEqual(self.clock,1020)
        with patch.object(t.urllib.request,'urlopen',side_effect=AssertionError('Must not call API')):
            again,_=self.call();self.assertEqual(value,again)
        attempts=sorted(self.case.glob('calls/role/attempt-*'))
        self.assertEqual(len(attempts),2)
        self.assertEqual((attempts[0]/'request.json').read_bytes(),(attempts[1]/'request.json').read_bytes())
        self.assertTrue((attempts[0]/'error.json').exists())
        self.assertEqual(json.loads((attempts[0]/'response.raw.json').read_text())['error']['code'],'rate_limit_exceeded')
    def test_pacing_and_rate_reset_headers(self):
        with patch.object(t.urllib.request,'urlopen',side_effect=[Response(headers={'x-ratelimit-remaining-tokens':'100','x-ratelimit-reset-tokens':'25s'}),Response(),Response()]):
            self.call('one');self.call('two');self.assertGreaterEqual(self.clock,1025)
            self.call('three');self.assertGreaterEqual(self.clock,1040)
    def test_quota_not_retried(self):
        with patch.object(t.urllib.request,'urlopen',side_effect=http_error(error_code='insufficient_quota')) as api:
            with self.assertRaises(t.DeferredCall):self.call()
            with self.assertRaises(t.DeferredCall):self.call()
            self.assertEqual(api.call_count,1)
    def test_200_invalid_json_never_retried(self):
        bad=json.dumps({'choices':[{'message':{'content':'not json'}}]}).encode()
        with patch.object(t.urllib.request,'urlopen',return_value=Response(bad)) as api:
            with self.assertRaises(t.TerminalModelOutput):self.call()
            with self.assertRaises(t.TerminalModelOutput):self.call()
            self.assertEqual(api.call_count,1)
    def test_long_server_delay_defers_without_early_retry(self):
        with patch.object(t.urllib.request,'urlopen',side_effect=http_error(headers={'Retry-After':'300'})) as api:
            with self.assertRaises(t.DeferredCall):self.call()
            self.assertEqual(api.call_count,1);self.assertEqual(self.clock,1000)
        self.clock=1300
        with patch.object(t.urllib.request,'urlopen',return_value=Response()):self.call()
    def test_attempt_limit_persists_on_resume(self):
        self.freeze['transport_policy']['max_attempts_per_call']=2
        with patch.object(t.urllib.request,'urlopen',side_effect=lambda *a,**kw:http_raise()) as api:
            with self.assertRaises(t.DeferredCall):self.call()
            with self.assertRaises(t.DeferredCall):self.call()
            self.assertEqual(api.call_count,2)
    def test_transport_timeout_recorded_then_retried(self):
        with patch.object(t.urllib.request,'urlopen',side_effect=[TimeoutError('offline'),Response()]):self.call()
        meta=json.loads(next(self.case.glob('calls/role/attempt-001/meta.json')).read_text())
        self.assertEqual(meta['http_status'],0);self.assertTrue(meta['transport_response_is_synthetic_error_record'])
    def test_changed_request_or_response_refused(self):
        with patch.object(t.urllib.request,'urlopen',return_value=Response()):self.call()
        with self.assertRaises(RuntimeError):self.call(messages=[{'changed':True}])
        p=next(self.case.glob('calls/role/attempt-001/response.raw.json'));p.write_text('{}')
        with self.assertRaises(RuntimeError):self.call()
    def test_incomplete_attempt_not_resent(self):
        p=self.case/'calls'/'role'/'attempt-001';p.mkdir(parents=True)
        with patch.object(t.urllib.request,'urlopen',side_effect=AssertionError('Must not call API')):
            with self.assertRaises(t.DeferredCall):self.call()
    def test_total_budget_counts_failures(self):
        self.freeze['transport_policy']['max_http_attempts_per_run']=1
        with patch.object(t.urllib.request,'urlopen',side_effect=http_error()) as api:
            with self.assertRaises(t.DeferredCall):self.call()
            self.assertEqual(api.call_count,1)
    def test_duration_parsing(self):
        self.assertEqual(t.seconds('1m2.5s'),62.5);self.assertEqual(t.seconds('500ms'),.5)
        self.assertEqual(t.seconds('invalid'),0)

def http_raise():raise http_error()

if __name__=='__main__':unittest.main()
