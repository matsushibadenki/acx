import copy
from threading import Thread
import unittest
from urllib.error import HTTPError

from client import call, run, verify_receipt
from provider import make_server


class LifecycleTests(unittest.TestCase):
    def setUp(self):
        self.now = 1000
        self.server = make_server(clock=lambda: self.now)
        self.thread = Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f'http://127.0.0.1:{self.server.server_port}'
        self.request = {'text': 'Hello / こんにちは / 你好', 'copies': 1}

    def tearDown(self):
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()

    def post(self, path, body):
        return call(self.base, path, body)

    def prepare(self, copies=1):
        pf = self.post('/preflight', {'input': {**self.request, 'copies': copies}})
        binding = {k: pf[k] for k in ('preflightId', 'preflightDigest')}
        return binding

    def authorized(self):
        binding = self.prepare()
        auth = self.post('/authorize', binding)
        return {**binding, 'authorization': auth['authorization'], 'input': self.request}

    def rejects(self, path, body, status):
        with self.assertRaises(HTTPError) as caught:
            self.post(path, body)
        self.assertEqual(caught.exception.code, status)
        caught.exception.close()

    def test_full_lifecycle(self):
        self.assertEqual(run(self.base)['status'], 'succeeded')

    def test_changed_request_and_preflight(self):
        body = self.authorized()
        self.rejects('/commit', {**body, 'input': {**self.request, 'copies': 2}}, 409)
        self.rejects('/commit', {**body, 'preflightDigest': 'sha256:tampered'}, 409)
        self.assertFalse(self.server.provider.commits)

    def test_missing_and_cross_preflight_authorization(self):
        body = self.authorized()
        self.rejects('/commit', {**body, 'authorization': 'unknown'}, 403)
        self.rejects('/commit', {**body, **self.prepare()}, 403)

    def test_policy_denial_and_invalid_input(self):
        self.rejects('/authorize', self.prepare(copies=3), 403)
        self.rejects('/preflight', {'input': {**self.request, 'copies': 0}}, 400)
        self.rejects('/preflight', {'input': {**self.request, 'extra': True}}, 400)

    def test_expired_authorize_commit_execute(self):
        body = self.authorized()
        self.now += 120
        self.rejects('/authorize', body, 410)
        self.rejects('/commit', body, 410)
        fresh = self.authorized()
        commit = self.post('/commit', fresh)
        self.now += 120
        self.rejects('/execute', {'commitId': commit['commitId']}, 410)
        self.assertFalse(self.server.provider.receipts)

    def test_replay_and_execute_before_commit(self):
        self.rejects('/execute', {'commitId': 'unknown'}, 403)
        body = self.authorized()
        commit = self.post('/commit', body)
        self.rejects('/commit', body, 409)
        first = self.post('/execute', {'commitId': commit['commitId']})
        again = self.post('/execute', {'commitId': commit['commitId']})
        self.assertEqual(first, again)
        self.assertEqual(len(self.server.provider.receipts), 1)

    def test_receipt_tampering(self):
        body = self.authorized()
        commit = self.post('/commit', body)
        execution = self.post('/execute', {'commitId': commit['commitId']})
        receipt = call(self.base, execution['receiptUrl'])
        manifest = call(self.base, '/.well-known/acx.json')
        for field in ('requestHash', 'resultHash', 'provider', 'capability'):
            altered = copy.deepcopy(receipt)
            altered[field] = 'tampered'
            with self.subTest(field=field), self.assertRaises(ValueError):
                verify_receipt(altered, manifest, self.request, execution['result'])


if __name__ == '__main__':
    unittest.main()
