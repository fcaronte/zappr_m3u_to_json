#!/usr/bin/env python3
"""Valida il JSON generato contro schema.json (se presente nel repository)."""
import json
import sys
from jsonschema import Draft7Validator

schema = json.load(open(sys.argv[1], encoding="utf-8"))
data = json.load(open(sys.argv[2], encoding="utf-8"))
errors = sorted(Draft7Validator(schema).iter_errors(data), key=lambda e: list(e.absolute_path))
for e in errors:
    print("::error::" + "/".join(map(str, e.absolute_path)) + ": " + e.message)
if errors:
    sys.exit(f"{len(errors)} errori di validazione")
print("JSON valido secondo lo schema")
