#!/usr/bin/env python3
"""Initialize, record, validate, and render an anything-tutor learner workspace."""

from __future__ import annotations

import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

LEVELS = ("unassessed", "recognition", "recall", "near_transfer", "far_transfer", "retained")
CONFIDENCE = {"low", "medium", "high"}
HINTS = {"none", "restate", "focus", "principle", "partial_step", "full_demo"}
PHASES = {"orient", "review", "diagnose", "attempt", "instruct", "practice", "assess", "remediate", "close"}
RESULTS = {"pass", "partial", "fail", "ungradable"}
ERRORS = {None, "knowledge_gap", "misconception", "procedure_failure", "condition_omission", "transfer_failure", "ambiguous_task", "unreliable_grading"}


def now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_json(path: Path, data: dict) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    os.replace(temp, path)


def resolve_domain_path(learning_path: Path, ref: dict) -> Path:
    candidate = Path(str(ref.get("path", "")))
    return candidate if candidate.is_absolute() else (learning_path.parent / candidate).resolve()


def init_workspace(learning_path: Path, workspace: Path) -> None:
    learning_path = learning_path.resolve()
    route = load_json(learning_path)
    workspace.mkdir(parents=True, exist_ok=True)
    state_path = workspace / "learner-state.json"
    if state_path.exists():
        raise FileExistsError(f"workspace already initialized: {state_path}")
    created = now()
    cap_states = {}
    for cap in route.get("capabilities", []):
        initial = cap.get("initial_evidence") or {}
        cap_states[cap["id"]] = {
            "level": initial.get("level", "unassessed"),
            "confidence": initial.get("confidence", "low"),
            "last_evidence_at": initial.get("timestamp"),
            "evidence_refs": [],
            "last_error_type": None,
            "last_hint_level": "none",
            "next_review_at": None,
        }
    domain_ref = dict(route.get("domain_map_ref", {}))
    if domain_ref.get("path"):
        domain_ref["path"] = str(resolve_domain_path(learning_path, domain_ref))
    state = {
        "schema_version": "1.0",
        "learner_id": route.get("learner", {}).get("learner_id", "learner-local"),
        "roadmap_ref": {"roadmap_id": route.get("roadmap_id"), "version": route.get("version"), "path": str(learning_path)},
        "domain_map_ref": domain_ref,
        "created_at": created,
        "updated_at": created,
        "session": {"phase": "orient", "current_capability_id": None, "teaching_mode": "attempt_first"},
        "capability_states": cap_states,
        "route_overrides": [],
        "review_queue": [],
        "last_session_summary": None,
    }
    atomic_json(state_path, state)
    (workspace / "evidence.jsonl").write_text("", encoding="utf-8")
    render_progress(workspace)


def validate_event(event: dict, known_caps: set[str]) -> list[str]:
    errors = []
    required = {"event_id", "timestamp", "capability_id", "task_id", "evidence_type", "result", "resulting_level", "hint_level", "confidence", "summary"}
    missing = sorted(required - event.keys())
    if missing:
        errors.append(f"event missing fields: {', '.join(missing)}")
    if event.get("capability_id") not in known_caps:
        errors.append(f"unknown capability: {event.get('capability_id')!r}")
    if event.get("result") not in RESULTS:
        errors.append(f"invalid result: {event.get('result')!r}")
    if event.get("resulting_level") not in LEVELS:
        errors.append(f"invalid resulting_level: {event.get('resulting_level')!r}")
    if event.get("hint_level") not in HINTS:
        errors.append(f"invalid hint_level: {event.get('hint_level')!r}")
    if event.get("confidence") not in CONFIDENCE:
        errors.append(f"invalid confidence: {event.get('confidence')!r}")
    if event.get("error_type") not in ERRORS:
        errors.append(f"invalid error_type: {event.get('error_type')!r}")
    if not str(event.get("summary", "")).strip():
        errors.append("event summary cannot be empty")
    return errors


def record(workspace: Path, event_path: Path) -> None:
    state_path = workspace / "learner-state.json"
    state = load_json(state_path)
    event = load_json(event_path)
    errors = validate_event(event, set(state.get("capability_states", {})))
    existing_ids = set()
    evidence_path = workspace / "evidence.jsonl"
    if evidence_path.exists():
        for line in evidence_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                existing_ids.add(json.loads(line).get("event_id"))
    if event.get("event_id") in existing_ids:
        errors.append(f"duplicate event_id: {event.get('event_id')}")
    if errors:
        raise ValueError("; ".join(errors))

    cap = state["capability_states"][event["capability_id"]]
    cap["level"] = event["resulting_level"]
    cap["confidence"] = event["confidence"]
    cap["last_evidence_at"] = event["timestamp"]
    cap["evidence_refs"].append(event["event_id"])
    cap["last_error_type"] = event.get("error_type")
    cap["last_hint_level"] = event["hint_level"]
    cap["next_review_at"] = event.get("next_review_at")
    state["updated_at"] = now()
    state["review_queue"] = sorted(
        [{"capability_id": cap_id, "due_at": value["next_review_at"]} for cap_id, value in state["capability_states"].items() if value.get("next_review_at")],
        key=lambda item: item["due_at"],
    )
    temp_state = state_path.with_suffix(".json.tmp")
    temp_state.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    with evidence_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")
    os.replace(temp_state, state_path)
    render_progress(workspace)


def validate_workspace(workspace: Path) -> list[str]:
    errors = []
    state = load_json(workspace / "learner-state.json")
    caps = state.get("capability_states", {})
    if state.get("session", {}).get("phase") not in PHASES:
        errors.append("invalid session phase")
    if state.get("session", {}).get("current_capability_id") not in {None, *caps.keys()}:
        errors.append("current capability does not exist")
    refs = set()
    for cap_id, cap in caps.items():
        if cap.get("level") not in LEVELS:
            errors.append(f"{cap_id}: invalid level")
        if cap.get("confidence") not in CONFIDENCE:
            errors.append(f"{cap_id}: invalid confidence")
        if cap.get("last_hint_level") not in HINTS:
            errors.append(f"{cap_id}: invalid hint level")
        refs.update(cap.get("evidence_refs", []))
    seen = set()
    evidence_path = workspace / "evidence.jsonl"
    if evidence_path.exists():
        for number, line in enumerate(evidence_path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                errors.append(f"evidence line {number}: invalid JSON")
                continue
            errors.extend(f"evidence line {number}: {e}" for e in validate_event(event, set(caps)))
            if event.get("event_id") in seen:
                errors.append(f"evidence line {number}: duplicate event_id")
            seen.add(event.get("event_id"))
    missing = refs - seen
    if missing:
        errors.append(f"state references missing evidence: {', '.join(sorted(missing))}")
    return errors


def render_progress(workspace: Path) -> None:
    state = load_json(workspace / "learner-state.json")
    route = load_json(Path(state["roadmap_ref"]["path"]))
    caps_by_id = {cap["id"]: cap for cap in route.get("capabilities", [])}
    counts = Counter(value.get("level", "unassessed") for value in state.get("capability_states", {}).values())
    current_id = state.get("session", {}).get("current_capability_id")
    current = caps_by_id.get(current_id, {})
    lines = [
        f"# {route.get('roadmap_id', '学习路线')} 学习进度",
        "",
        f"> 学习者：{state.get('learner_id')} | 更新时间：{state.get('updated_at')}",
        "",
        "## 当前定位",
        "",
        f"- 当前能力：{current.get('title', '尚未选择')} ({current_id or '无'})",
        f"- 会话阶段：{state.get('session', {}).get('phase')}",
        f"- 教学入口：{state.get('session', {}).get('teaching_mode')}",
        "",
        "## 能力证据",
        "",
    ]
    for level in LEVELS:
        lines.append(f"- {level}: {counts[level]}")
    lines.extend(["", "## 复习队列", ""])
    queue = state.get("review_queue", [])
    if queue:
        for item in queue:
            title = caps_by_id.get(item["capability_id"], {}).get("title", item["capability_id"])
            lines.append(f"- {item['due_at']}: {title} ({item['capability_id']})")
    else:
        lines.append("- 暂无已安排复习")
    lines.extend(["", "## 路线调整", ""])
    overrides = state.get("route_overrides", [])
    if overrides:
        for item in overrides:
            lines.append(f"- {item.get('type')}: {item.get('capability_id')}，原因：{item.get('reason')}")
    else:
        lines.append("- 暂无运行时调整")
    lines.extend(["", "## 最近会话", "", state.get("last_session_summary") or "尚无会话摘要", ""])
    (workspace / "progress.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: state_tool.py init LEARNING_PATH WORKSPACE | record WORKSPACE EVENT_JSON | validate WORKSPACE | render WORKSPACE", file=sys.stderr)
        return 2
    command = sys.argv[1]
    try:
        if command == "init" and len(sys.argv) == 4:
            init_workspace(Path(sys.argv[2]), Path(sys.argv[3]))
        elif command == "record" and len(sys.argv) == 4:
            record(Path(sys.argv[2]), Path(sys.argv[3]))
        elif command == "validate" and len(sys.argv) == 3:
            errors = validate_workspace(Path(sys.argv[2]))
            for error in errors:
                print(f"ERROR: {error}")
            if errors:
                print(f"FAIL: {len(errors)} error(s)")
                return 1
            print("PASS: learner workspace is valid")
        elif command == "render" and len(sys.argv) == 3:
            render_progress(Path(sys.argv[2]))
        else:
            print("invalid command or arguments", file=sys.stderr)
            return 2
    except (OSError, KeyError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
