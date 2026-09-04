#!/usr/bin/env python3
"""Validate learning-path.json and its optional domain-map references."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROLES = {"core", "support", "branch", "deferred"}
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


def domain_ids(data: dict) -> set[str]:
    result: set[str] = set()
    def walk(node: dict) -> None:
        if node.get("id"):
            result.add(node["id"])
        for child in node.get("children", []):
            walk(child)
    for module in data.get("modules", []):
        walk(module)
    return result


def validate(path: Path, domain_path: Path | None) -> tuple[list[str], list[str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    warnings: list[str] = []
    required = {"schema_version", "roadmap_id", "version", "generated_at", "domain_map_ref", "learner", "learning_contract", "capabilities", "recommended_sequence", "projects", "sources"}
    missing = sorted(required - data.keys())
    if missing:
        errors.append(f"missing top-level fields: {', '.join(missing)}")
    if not SEMVER.match(str(data.get("version", ""))):
        errors.append("version must be semantic version x.y.z")
    contract = data.get("learning_contract", {})
    for field in ("goal_context", "graduation_task", "constraints", "completion_evidence"):
        if not contract.get(field):
            errors.append(f"learning_contract missing {field}")

    capabilities: dict[str, dict] = {}
    for index, cap in enumerate(data.get("capabilities", [])):
        if not isinstance(cap, dict):
            errors.append(f"capabilities[{index}] must be an object")
            continue
        cap_id = cap.get("id")
        if not cap_id:
            errors.append(f"capabilities[{index}] missing id")
            continue
        if cap_id in capabilities:
            errors.append(f"duplicate capability id: {cap_id}")
        capabilities[cap_id] = cap
        if cap.get("role") not in ROLES:
            errors.append(f"{cap_id}: invalid role {cap.get('role')!r}")
        for field in ("title", "statement", "selection_reason", "knowledge_links"):
            if not cap.get(field):
                errors.append(f"{cap_id}: missing {field}")
        if cap.get("role") == "core":
            for field in ("lesson_file", "mastery_requirement", "diagnostic", "assessment", "remediation"):
                if not cap.get(field):
                    errors.append(f"{cap_id}: core capability missing {field}")

    for cap_id, cap in capabilities.items():
        for prereq in cap.get("prerequisite_capability_ids", []):
            if prereq not in capabilities:
                errors.append(f"{cap_id}: unknown prerequisite capability {prereq}")
        for branch in cap.get("remediation", {}).get("branch_capability_ids", []):
            if branch not in capabilities:
                errors.append(f"{cap_id}: unknown remediation branch {branch}")

    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(cap_id: str) -> None:
        if cap_id in visiting:
            errors.append(f"capability dependency cycle at {cap_id}")
            return
        if cap_id in visited or cap_id not in capabilities:
            return
        visiting.add(cap_id)
        for prereq in capabilities[cap_id].get("prerequisite_capability_ids", []):
            visit(prereq)
        visiting.remove(cap_id)
        visited.add(cap_id)
    for cap_id in capabilities:
        visit(cap_id)

    sequence = data.get("recommended_sequence", [])
    positions = {cap_id: index for index, cap_id in enumerate(sequence)}
    if len(positions) != len(sequence):
        errors.append("recommended_sequence contains duplicate ids")
    for cap_id in sequence:
        if cap_id not in capabilities:
            errors.append(f"recommended_sequence: unknown capability {cap_id}")
    for cap_id, cap in capabilities.items():
        if cap.get("role") in {"core", "support"} and cap_id not in positions:
            errors.append(f"{cap_id}: core/support capability missing from recommended_sequence")
        for prereq in cap.get("prerequisite_capability_ids", []):
            if cap_id in positions and prereq in positions and positions[prereq] > positions[cap_id]:
                errors.append(f"recommended_sequence places {cap_id} before prerequisite {prereq}")
            if cap_id in positions and prereq not in positions:
                errors.append(f"recommended_sequence omits prerequisite {prereq} required by {cap_id}")
        if cap.get("role") == "deferred" and cap_id in positions:
            errors.append(f"{cap_id}: deferred capability cannot appear in recommended_sequence")

    graduation = [p for p in data.get("projects", []) if isinstance(p, dict) and p.get("type") == "graduation"]
    if not graduation:
        errors.append("projects must contain at least one graduation project")
    for project in data.get("projects", []):
        if not isinstance(project, dict):
            continue
        for cap_id in project.get("capability_ids", []):
            if cap_id not in capabilities:
                errors.append(f"project {project.get('id')}: unknown capability {cap_id}")
    graduation_caps = {cap_id for project in graduation for cap_id in project.get("capability_ids", [])}
    for cap_id, cap in capabilities.items():
        if cap.get("role") == "core" and cap_id not in graduation_caps:
            errors.append(f"{cap_id}: core capability is not exercised by a graduation project")

    if domain_path:
        domain = json.loads(domain_path.read_text(encoding="utf-8"))
        expected = data.get("domain_map_ref", {})
        if expected.get("domain_map_id") != domain.get("domain_map_id"):
            errors.append("domain_map_ref.domain_map_id does not match supplied domain map")
        if expected.get("version") != domain.get("version"):
            errors.append("domain_map_ref.version does not match supplied domain map")
        known = domain_ids(domain)
        for cap_id, cap in capabilities.items():
            for link in cap.get("knowledge_links", []):
                kp = link.get("knowledge_point_id") if isinstance(link, dict) else None
                if kp not in known:
                    errors.append(f"{cap_id}: unknown knowledge point {kp!r}")
    else:
        warnings.append("domain map not supplied; knowledge-point references were not checked")

    roles_present = {c.get("role") for c in capabilities.values()}
    for role in ("core", "support"):
        if role not in roles_present:
            warnings.append(f"no capability with role {role}")
    return errors, warnings


def main() -> int:
    if len(sys.argv) not in (2, 3):
        print("usage: validate_learning_path.py LEARNING_PATH_JSON [DOMAIN_MAP_JSON]", file=sys.stderr)
        return 2
    try:
        errors, warnings = validate(Path(sys.argv[1]), Path(sys.argv[2]) if len(sys.argv) == 3 else None)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        return 1
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"FAIL: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    print(f"PASS: 0 errors, {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
