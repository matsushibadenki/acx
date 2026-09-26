"""Local, experimental ACX HTTP binding; no printer or payment integration."""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import secrets
import time

from jsonschema import Draft202012Validator, FormatChecker, ValidationError

ROOT = Path(__file__).resolve().parents[2]
CAPABILITY = 'org.example.print.simulate'
PROVIDER = 'urn:acx:example:local-print'


def digest(value):
    # Demo encoding only, not a cross-language canonicalization standard.
    encoded = json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    return 'sha256:' + hashlib.sha256(encoded.encode('utf-8')).hexdigest()


def validate(value, schema):
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(value)


def schema(name):
    return json.loads((ROOT / 'schemas' / f'acx-{name}.schema.json').read_text())


def manifest(base):
    return {'acx': '0.1', 'provider': {'id': PROVIDER, 'name': 'Local print simulator'},
            'capabilities': [{
                'id': CAPABILITY, 'version': '1.0.0',
                'description': 'Simulate a print job in memory; no physical printing.',
                'inputSchema': {'type': 'object', 'required': ['text', 'copies'],
                    'properties': {'text': {'type': 'string', 'minLength': 1, 'maxLength': 4096},
                                   'copies': {'type': 'integer', 'minimum': 1, 'maximum': 10}},
                    'additionalProperties': False},
                'outputSchema': {'type': 'object', 'required': ['jobId', 'copies', 'simulated'],
                    'properties': {'jobId': {'type': 'string'}, 'copies': {'type': 'integer'},
                                   'simulated': {'const': True}}, 'additionalProperties': False},
                'bindings': [{'type': 'other', 'profile': 'experimental-local-http', 'endpoint': base}],
                'risk': 'consequential', 'authority': {'approval': 'policy', 'scopes': ['print:simulate']},
                'effects': ['simulated-print-job'],
                'economics': {'model': 'free', 'currency': 'USD', 'max': '0.00'},
                'evidence': {'receipt': 'plain'}, 'recovery': {'reversible': False}}]}


class Rejected(Exception):
    def __init__(self, message, status=409):
        self.status = status
        super().__init__(message)


class Provider:
    def __init__(self, base, ttl=120, clock=time.time):
        self.manifest = manifest(base)
        validate(self.manifest, schema('manifest'))
        self.ttl, self.clock = ttl, clock
        self.preflights, self.authorizations, self.commits, self.receipts = {}, {}, {}, {}

    def preflight_for(self, body):
        pf = self.preflights.get(body.get('preflightId'))
        if pf is None:
            raise Rejected('unknown preflight', 404)
        if self.clock() >= pf['expiresAt']:
            raise Rejected('expired preflight', 410)
        if body.get('preflightDigest') != digest(pf):
            raise Rejected('preflight digest mismatch')
        return pf

    def dispatch(self, method, path, body):
        if method == 'GET' and path == '/.well-known/acx.json':
            return self.manifest
        if method == 'GET' and path.startswith('/receipts/'):
            receipt = self.receipts.get(path.removeprefix('/receipts/'))
            if receipt is None:
                raise Rejected('unknown receipt', 404)
            return receipt
        if method != 'POST':
            raise Rejected('unknown endpoint', 404)
        if path == '/preflight':
            request = body.get('input')
            validate(request, self.manifest['capabilities'][0]['inputSchema'])
            pf = {'preflightId': secrets.token_hex(16), 'capability': CAPABILITY,
                  'version': '1.0.0', 'input': deepcopy(request), 'requestHash': digest(request),
                  'effects': ['simulated-print-job'],
                  'cost': {'currency': 'USD', 'estimated': '0.00', 'max': '0.00'},
                  'approval': {'type': 'policy', 'scope': 'print:simulate'},
                  'recovery': {'reversible': False}, 'expiresAt': self.clock() + self.ttl}
            self.preflights[pf['preflightId']] = pf
            return {**pf, 'preflightDigest': digest(pf)}
        if path == '/authorize':
            pf = self.preflight_for(body)
            # Explicit demo policy: at most two copies, zero actual charge.
            if pf['input']['copies'] > 2:
                raise Rejected('demo policy permits at most two copies', 403)
            token = secrets.token_urlsafe(32)
            self.authorizations[token] = pf['preflightId']
            return {'authorization': token, 'scope': 'print:simulate', 'expiresAt': pf['expiresAt']}
        if path == '/commit':
            pf = self.preflight_for(body)
            if self.authorizations.get(body.get('authorization')) != pf['preflightId']:
                raise Rejected('missing or unrelated authorization', 403)
            if digest(body.get('input')) != pf['requestHash']:
                raise Rejected('request digest mismatch')
            if pf['preflightId'] in self.commits:
                raise Rejected('preflight already committed')
            commit = {'commitId': secrets.token_urlsafe(32), 'preflightId': pf['preflightId']}
            self.commits[pf['preflightId']] = commit
            return commit
        if path == '/execute':
            commit = next((c for c in self.commits.values()
                           if c['commitId'] == body.get('commitId')), None)
            if commit is None:
                raise Rejected('unknown commit', 403)
            if 'execution' in commit:
                return commit['execution']  # Retry returns the same job and receipt.
            pf = self.preflights[commit['preflightId']]
            if self.clock() >= pf['expiresAt']:
                raise Rejected('expired preflight', 410)
            result = {'jobId': secrets.token_hex(12), 'copies': pf['input']['copies'], 'simulated': True}
            validate(result, self.manifest['capabilities'][0]['outputSchema'])
            receipt = {'acx': '0.1', 'receiptId': secrets.token_hex(16), 'capability': CAPABILITY,
                       'provider': PROVIDER, 'status': 'succeeded',
                       'issuedAt': datetime.now(timezone.utc).isoformat(),
                       'requestHash': pf['requestHash'], 'resultHash': digest(result),
                       'effects': pf['effects'], 'cost': {'currency': 'USD', 'amount': '0.00'},
                       'recovery': pf['recovery']}
            validate(receipt, schema('receipt'))
            self.receipts[receipt['receiptId']] = receipt
            commit['execution'] = {'result': result, 'receiptUrl': '/receipts/' + receipt['receiptId']}
            return commit['execution']
        raise Rejected('unknown endpoint', 404)


def make_server(port=0, ttl=120, clock=time.time):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def handle_request(self):
            try:
                size = int(self.headers.get('Content-Length', '0'))
                if size < 0 or size > 16384:
                    raise Rejected('body too large', 413)
                body = json.loads(self.rfile.read(size)) if size else {}
                if not isinstance(body, dict):
                    raise Rejected('expected JSON object', 400)
                result = self.server.provider.dispatch(self.command, self.path, body)
                status = 200
            except Rejected as exc:
                status, result = exc.status, {'error': str(exc)}
            except (ValueError, TypeError, ValidationError):
                status, result = 400, {'error': 'invalid request'}
            payload = json.dumps(result).encode()
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        do_GET = do_POST = handle_request

    server = HTTPServer(('127.0.0.1', port), Handler)
    server.provider = Provider(f'http://127.0.0.1:{server.server_port}', ttl, clock)
    return server


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    with make_server(args.port) as server:
        print(f'ACX Provider: http://127.0.0.1:{server.server_port}', flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
