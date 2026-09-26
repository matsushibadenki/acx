"""Run and verify all six lifecycle steps against the local demo provider."""
import argparse
import json
from urllib.request import Request, urlopen

from provider import digest, schema, validate


def call(base, path, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = Request(base + path, data=data, headers={'Content-Type': 'application/json'})
    with urlopen(req, timeout=5) as response:
        return json.load(response)


def verify_receipt(receipt, manifest, request, result):
    validate(receipt, schema('receipt'))
    expected = {'provider': manifest['provider']['id'],
                'capability': manifest['capabilities'][0]['id'], 'status': 'succeeded',
                'requestHash': digest(request), 'resultHash': digest(result)}
    for key, value in expected.items():
        if receipt.get(key) != value:
            raise ValueError(f'receipt {key} mismatch')


def run(base):
    manifest = call(base, '/.well-known/acx.json')
    validate(manifest, schema('manifest'))
    print('1 discover  PASS — ' + manifest['capabilities'][0]['id'])
    request = {'text': 'Hello ACX / こんにちは / 你好', 'copies': 1}
    pf = call(base, '/preflight', {'input': request})
    unsigned = {k: v for k, v in pf.items() if k != 'preflightDigest'}
    if digest(unsigned) != pf['preflightDigest'] or digest(request) != pf['requestHash']:
        raise ValueError('preflight digest mismatch')
    binding = {k: pf[k] for k in ('preflightId', 'preflightDigest')}
    print('2 preflight PASS — maximum USD ' + pf['cost']['max'])
    auth = call(base, '/authorize', binding)
    print('3 authorize PASS — local policy approved')
    commit = call(base, '/commit', {**binding, 'authorization': auth['authorization'], 'input': request})
    print('4 commit    PASS — bound to approved preflight')
    execution = call(base, '/execute', {'commitId': commit['commitId']})
    validate(execution['result'], manifest['capabilities'][0]['outputSchema'])
    print('5 execute   PASS — simulated job ' + execution['result']['jobId'])
    receipt = call(base, execution['receiptUrl'])
    verify_receipt(receipt, manifest, request, execution['result'])
    print('6 receipt   PASS — request/result hashes verified')
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', default='http://127.0.0.1:8765')
    run(parser.parse_args().base_url.rstrip('/'))
