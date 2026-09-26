import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]


class PrintProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads(
            (ROOT / "schemas/profiles/acx-print-intent.schema.json").read_text()
        )
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())

    def test_example_is_valid(self):
        intent = json.loads((ROOT / "examples/print-intent.json").read_text())
        self.validator.validate(intent)

    def test_printer_destination_requires_printer_id(self):
        intent = json.loads((ROOT / "examples/print-intent.json").read_text())
        intent["output"] = {"destination": "printer"}
        self.assertTrue(list(self.validator.iter_errors(intent)))

    def test_requirement_mode_is_explicit(self):
        intent = json.loads((ROOT / "examples/print-intent.json").read_text())
        intent["dpi"] = {"value": 600}
        self.assertTrue(list(self.validator.iter_errors(intent)))


if __name__ == "__main__":
    unittest.main()
