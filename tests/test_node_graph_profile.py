import copy
import json
from pathlib import Path
import unittest
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
class NodeGraphProfileTests(unittest.TestCase):
    def setUp(self):
        self.schema=json.loads((ROOT/'schemas/profiles/acx-node-graph-intent.schema.json').read_text())
        Draft202012Validator.check_schema(self.schema)
        self.validator=Draft202012Validator(self.schema,format_checker=FormatChecker())
        self.intent=json.loads((ROOT/'examples/node-graph-intent.json').read_text())
    def test_example(self): self.validator.validate(self.intent)
    def test_revision_and_document_are_required(self):
        for key in ['document_id','expected_revision']:
            invalid=copy.deepcopy(self.intent); del invalid[key]
            self.assertTrue(list(self.validator.iter_errors(invalid)))
    def test_ports_cannot_be_forged(self):
        self.intent['operations'][0]['outputs']=[]
        self.assertTrue(list(self.validator.iter_errors(self.intent)))
    def test_invalid_operation_and_batch_limit(self):
        self.intent['operations'][0]['kind']='shell'
        self.assertTrue(list(self.validator.iter_errors(self.intent)))
        self.intent['operations']=[]
        self.assertTrue(list(self.validator.iter_errors(self.intent)))
    def test_run_and_negative_revision(self):
        run={k:v for k,v in self.intent.items() if k!='operations'}; run['kind']='run'
        self.validator.validate(run); run['expected_revision']=-1
        self.assertTrue(list(self.validator.iter_errors(run)))
if __name__=='__main__': unittest.main()
