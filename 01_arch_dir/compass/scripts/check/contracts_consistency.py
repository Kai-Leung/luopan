#!/usr/bin/env python3
"""Check that runtime API contracts and critical frontend mirrors stay aligned."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable, get_args


CODE_ROOT = Path(__file__).resolve().parents[2]
API_ROOT = CODE_ROOT / "services" / "api"
OPENAPI_PATH = CODE_ROOT / "packages" / "contracts" / "openapi" / "openapi.json"
SCHEMA_ROOT = CODE_ROOT / "packages" / "contracts" / "schemas"
SHARED_TYPES_PATH = CODE_ROOT / "packages" / "shared-types" / "index.ts"
H5_ENUMS_PATH = CODE_ROOT / "apps" / "h5" / "src" / "modules" / "standard_governance" / "enums.ts"
H5_STATUSES_PATH = CODE_ROOT / "apps" / "h5" / "src" / "modules" / "standard_governance" / "statuses.ts"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write-openapi",
        action="store_true",
        help="replace the checked-in OpenAPI document with the runtime document",
    )
    args = parser.parse_args()

    runtime_openapi = load_runtime_openapi()
    if args.write_openapi:
        OPENAPI_PATH.write_text(
            json.dumps(runtime_openapi, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    errors = [
        *check_openapi(runtime_openapi),
        *check_json_schemas(),
        *check_critical_type_mirrors(),
    ]
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(
        "contracts consistent: "
        f"{len(runtime_openapi.get('paths', {}))} paths, "
        f"{len(runtime_openapi.get('components', {}).get('schemas', {}))} OpenAPI schemas, "
        f"{len(list(SCHEMA_ROOT.glob('*.json')))} JSON Schema files"
    )
    return 0


def load_runtime_openapi() -> dict:
    sys.path.insert(0, str(API_ROOT))
    from app.main import app

    return app.openapi()


def check_openapi(runtime_openapi: dict) -> list[str]:
    try:
        stored_openapi = json.loads(OPENAPI_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"cannot read checked-in OpenAPI: {exc}"]
    if stored_openapi != runtime_openapi:
        return ["checked-in OpenAPI differs from FastAPI runtime OpenAPI"]
    return []


def check_json_schemas() -> list[str]:
    errors: list[str] = []
    for schema_path in sorted(SCHEMA_ROOT.glob("*.json")):
        try:
            document = json.loads(schema_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{schema_path.relative_to(CODE_ROOT)} is invalid JSON: {exc}")
            continue
        if not isinstance(document, dict):
            errors.append(f"{schema_path.relative_to(CODE_ROOT)} must contain a JSON object")
    return errors


def check_critical_type_mirrors() -> list[str]:
    from app.modules.l2_fact.schemas import FactStatus
    from app.modules.s2_governance_gate.confirmation.schemas import (
        ReviewAction,
        ReviewStatus,
    )
    from app.modules.s2_governance_gate.schemas import (
        GovernanceStatus,
        NextAction,
        RiskLevelValue,
    )
    from app.modules.standard_governance.enums.source_types import SourceType
    from app.modules.standard_governance.enums.status_types import CandidateStatus
    from app.modules.standard_governance.processing import StandardProcessingDirection

    shared_types = SHARED_TYPES_PATH.read_text(encoding="utf-8")
    h5_enums = H5_ENUMS_PATH.read_text(encoding="utf-8")
    h5_statuses = H5_STATUSES_PATH.read_text(encoding="utf-8")

    expected_shared = {
        "SourceType": enum_values(SourceType),
        "CandidateStatus": enum_values(CandidateStatus),
        "GovernanceStatus": literal_values(GovernanceStatus),
        "ReviewAction": literal_values(ReviewAction),
        "ReviewStatus": literal_values(ReviewStatus),
        "FactStatus": literal_values(FactStatus),
        "RiskLevel": literal_values(RiskLevelValue),
        "NextAction": literal_values(NextAction),
        "StandardProcessingDirection": literal_values(StandardProcessingDirection),
    }

    errors: list[str] = []
    for type_name, expected in expected_shared.items():
        actual = extract_type_union(shared_types, type_name)
        if actual != expected:
            errors.append(
                f"shared type {type_name} differs: expected {sorted(expected)}, got {sorted(actual)}"
            )

    h5_source_types = extract_enum_values(h5_enums, "SourceType")
    if h5_source_types != enum_values(SourceType):
        errors.append("H5 SourceType enum differs from backend SourceType")

    h5_candidate_statuses = extract_enum_values(h5_statuses, "CandidateStatus")
    if h5_candidate_statuses != enum_values(CandidateStatus):
        errors.append("H5 CandidateStatus enum differs from backend CandidateStatus")
    return errors


def enum_values(enum_type: type) -> set[str]:
    return {str(item.value) for item in enum_type}


def literal_values(literal_type: object) -> set[str]:
    return {str(item) for item in get_args(literal_type)}


def extract_type_union(source: str, type_name: str) -> set[str]:
    match = re.search(
        rf"export\s+type\s+{re.escape(type_name)}\s*=\s*(.*?);",
        source,
        flags=re.DOTALL,
    )
    if not match:
        return set()
    return quoted_values(match.group(1))


def extract_enum_values(source: str, enum_name: str) -> set[str]:
    match = re.search(
        rf"export\s+enum\s+{re.escape(enum_name)}\s*\{{(.*?)\}}",
        source,
        flags=re.DOTALL,
    )
    if not match:
        return set()
    return quoted_values(match.group(1))


def quoted_values(source: str) -> set[str]:
    return set(re.findall(r'["\']([^"\']+)["\']', source))


if __name__ == "__main__":
    raise SystemExit(main())
