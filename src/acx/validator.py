# /src/acx/validator.py
import json
from pathlib import Path
from jsonschema import Draft202012Validator, FormatChecker

def validate(instance_path: str, schema_path: str) -> list[str]:
    instance=json.loads(Path(instance_path).read_text())
    schema=json.loads(Path(schema_path).read_text())
    v=Draft202012Validator(schema, format_checker=FormatChecker())
    return [f"{'.'.join(map(str,e.absolute_path)) or '$'}: {e.message}" for e in sorted(v.iter_errors(instance), key=lambda e:list(e.absolute_path))]
