from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


SIMPLE_KEYS = ["typo", "rename", "doc", "comment", "log", "small", "tiny"]
HARD_KEYS = ["architecture", "refactor", "protocol", "schema", "api", "multi", "redesign"]


@dataclass
class BuildResult:
    run_id: str
    contract_path: str
    used_llm: bool
    difficulty: str
    need_input: bool = False
    event_lines: list[str] | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        if self.event_lines is None:
            payload.pop("event_lines", None)
        return payload


def _classify(query: str) -> str:
    q = (query or "").lower()
    if not q.strip():
        return "medium"
    if any(k in q for k in HARD_KEYS):
        return "hard"
    if any(k in q for k in SIMPLE_KEYS):
        return "simple"
    return "medium"


def _default_contract(query: str, repo_root: Path, difficulty: str) -> dict[str, Any]:
    goal = (query or "").strip().splitlines()[0][:200] or "Please fill goal"
    scope_allow: list[str] = []
    # best-effort keyword match on filesystem
    try:
        names = [p for p in repo_root.rglob("*") if p.is_file() and len(str(p).split("/")) <= 6]
        lower_q = goal.lower()
        hits = [p for p in names if p.name.lower() in lower_q]
        scope_allow = [str(p.parent.relative_to(repo_root)) for p in hits][:5]
    except Exception:
        scope_allow = []
    deny = [".git", "node_modules", "dist", "build"]
    acceptance = [
        "No lint/build errors (if applicable).",
        "Behavior matches the goal.",
    ]
    return {
        "goal": goal,
        "scope_allow": scope_allow,
        "scope_deny": deny,
        "acceptance": acceptance,
        "questions": [],
        "risk_flags": [],
        "context_budget": {"max_files": 20, "max_lines_per_file": 400, "max_snippets": 10},
    }


def build_contract(*, cwd: str, query: str, mode: str) -> BuildResult:
    repo_root = Path(cwd).resolve()
    contract_path = repo_root / ".codex" / "contract.json"
    difficulty = _classify(query)

    if mode not in {"simple", "auto", "llm"}:
        return BuildResult(
            run_id="",
            contract_path=str(contract_path),
            used_llm=False,
            difficulty=difficulty,
            need_input=True,
            event_lines=["error: mode must be simple|auto|llm"],
        )

    effective_mode = mode
    if mode == "auto":
        effective_mode = "simple" if difficulty == "simple" else "llm"

    if effective_mode == "simple":
        contract = _default_contract(query, repo_root, difficulty)
        contract_path.parent.mkdir(parents=True, exist_ok=True)
        contract_path.write_text(json.dumps(contract, ensure_ascii=False, indent=2), encoding="utf-8")
        return BuildResult(
            run_id="cb-" + repo_root.name,
            contract_path=str(contract_path),
            used_llm=False,
            difficulty=difficulty,
            event_lines=[f"contract written (mode=simple, difficulty={difficulty})"],
        )

    # LLM branch is stubbed as need_input to avoid executing here; placeholder for future impl.
    return BuildResult(
        run_id="",
        contract_path=str(contract_path),
        used_llm=True,
        difficulty=difficulty,
        need_input=True,
        event_lines=["LLM mode not implemented; provide contract manually or use mode=simple/auto"],
    )
