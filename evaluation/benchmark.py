"""Small, dependency-light portfolio benchmark for the AI Coding Agent."""
from __future__ import annotations

import json
import py_compile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    started = time.perf_counter()
    python_files = [p for p in ROOT.rglob("*.py") if ".venv" not in p.parts]
    compile_failures: list[str] = []

    for path in python_files:
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError:
            compile_failures.append(str(path.relative_to(ROOT)))

    required_task_types = {
        "issue_fix",
        "repository_qa",
        "code_review",
        "bug_triage",
        "documentation",
    }
    request_source = (ROOT / "app/models/requests.py").read_text(encoding="utf-8")
    supported = sorted(task for task in required_task_types if task in request_source)

    results = {
        "benchmark_type": "static engineering baseline",
        "python_files_checked": len(python_files),
        "python_syntax_passed": not compile_failures,
        "compile_failures": compile_failures,
        "supported_task_types": supported,
        "task_type_coverage": f"{len(supported)}/{len(required_task_types)}",
        "security_tests_present": (ROOT / "tests/test_security.py").exists(),
        "api_test_present": (ROOT / "tests/test_api.py").exists(),
        "ci_workflow_present": (ROOT / ".github/workflows/ci.yml").exists(),
        "elapsed_seconds": round(time.perf_counter() - started, 4),
        "limitations": "This baseline validates project structure and syntax. It does not claim LLM accuracy."
    }

    output = ROOT / "evaluation/results.json"
    output.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
