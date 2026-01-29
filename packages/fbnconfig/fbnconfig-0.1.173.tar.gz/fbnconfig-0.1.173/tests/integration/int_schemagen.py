import difflib
import json
import os
import pathlib

import jsonschema
import pytest

from fbnconfig import dump_deployment, schemagen
from fbnconfig.load_module import load_module


@pytest.fixture()
def this_folder():
    return pathlib.Path(__file__).parent.resolve()


@pytest.fixture()
def repo_root(this_folder):
    return this_folder.parent.parent


def test_commited_schema_matches_generated(this_folder):
    def normalize_schema(value):
        """Normalize schema for stable semantic comparison.

        JSON object key ordering is not significant and can vary across platforms / versions.
        This normalization makes the comparison deterministic.
        """
        if isinstance(value, dict):
            return {k: normalize_schema(v) for k, v in sorted(value.items())}
        if isinstance(value, list):
            normalized_items = [normalize_schema(v) for v in value]
            if all(isinstance(v, (str, int, float, bool)) or v is None for v in normalized_items):
                return sorted(normalized_items, key=lambda x: (str(type(x)), str(x)))
            if all(isinstance(v, dict) for v in normalized_items):
                return sorted(normalized_items, key=lambda x: json.dumps(x, sort_keys=True))
            return normalized_items
        return value

    new_schema = schemagen.cmd_deployment_schema()
    schema_path = this_folder.parent.parent / "deployment.schema.json"
    raw_old_schema = schema_path.read_text()
    old_schema = json.loads(raw_old_schema)

    normalized_new = normalize_schema(new_schema)
    normalized_old = normalize_schema(old_schema)

    # Semantic comparison with useful diff output on failure
    if normalized_new != normalized_old:
        new_str = json.dumps(normalized_new, indent=2, sort_keys=True)
        old_str = json.dumps(normalized_old, indent=2, sort_keys=True)

        diff = list(difflib.unified_diff(
            old_str.splitlines(),
            new_str.splitlines(),
            fromfile='committed (deployment.schema.json)',
            tofile='generated (from code)',
            lineterm=''
        ))

        # Show first 200 lines of diff to avoid overwhelming output
        diff_preview = '\n'.join(diff[:200])
        if len(diff) > 200:
            diff_preview += f'\n\n... and {len(diff) - 200} more lines'

        pytest.fail(
            f"Schema mismatch!\n\n"
            f"The committed deployment.schema.json does not match the generated schema.\n"
            f"Run the following command to update it:\n\n"
            f"    uv run python -m fbnconfig.schemagen > deployment.schema.json\n\n"
            f"Diff ({len(diff)} lines total):\n{diff_preview}"
        )

    # Optional strict mode for developers who want byte-for-byte reproducibility checks.
    # Enable with: FBNCONFIG_SCHEMA_STRICT_BYTES=1
    if (os.getenv("FBNCONFIG_SCHEMA_STRICT_BYTES") or "").lower() in {"1", "true", "yes"}:
        new_str = json.dumps(new_schema, indent=2).strip()
        old_str = raw_old_schema.strip()
        if new_str != old_str:
            diff = list(difflib.unified_diff(
                old_str.splitlines(),
                new_str.splitlines(),
                fromfile='committed (deployment.schema.json)',
                tofile='generated (from code)',
                lineterm=''
            ))
            diff_preview = '\n'.join(diff[:200])
            if len(diff) > 200:
                diff_preview += f'\n\n... and {len(diff) - 200} more lines'

            pytest.fail(
                f"Strict byte-for-byte schema mismatch!\n\n"
                f"Run: uv run python -m fbnconfig.schemagen > deployment.schema.json\n\n"
                f"Diff ({len(diff)} lines total):\n{diff_preview}"
            )


def pytest_generate_tests(metafunc):
    if "example_path" in metafunc.fixturenames:
        this_dir = pathlib.Path(__file__).parent.resolve()
        repo_dir = this_dir.parent.parent
        examples_dir = repo_dir / "public_examples" / "examples"
        script_paths = examples_dir.glob("*.py")
        metafunc.parametrize("example_path", script_paths)


def test_examples_against_schema(repo_root, example_path):
    host_vars = {}
    module = load_module(example_path, str(example_path.parent))
    d = module.configure(host_vars)
    deployment_json = dump_deployment(d)

    schema_path = repo_root / "deployment.schema.json"
    with open(schema_path, "r") as schema_io:
        schema_json = json.load(schema_io)

    jsonschema.validate(instance=deployment_json, schema=schema_json)