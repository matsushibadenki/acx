# /src/acx/__main__.py
import argparse
from .validator import validate

def main():
    p=argparse.ArgumentParser(prog='acx',description='ACX conformance utilities')
    s=p.add_subparsers(dest='cmd',required=True)
    v=s.add_parser('validate'); v.add_argument('manifest'); v.add_argument('--schema',default='schemas/acx-manifest.schema.json')
    a=p.parse_args()
    errors=validate(a.manifest,a.schema)
    if errors:
        print('\n'.join('ERROR '+e for e in errors)); raise SystemExit(1)
    print('ACX manifest valid')

if __name__=='__main__': main()
