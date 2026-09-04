#!/usr/bin/env python3
"""Validate structural invariants of domain-map.json."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ALLOWED_TYPES = ("module", "topic", "chapter", "knowledge_point")
TYPE_RANK = {name: rank for rank, name in enumerate(ALLOWED_TYPES)}
ALLOWED_RELATIONS = {"prerequisite", "supports", "contrasts", "interfaces", "applies_to"}
ALLOWED_VOLATILITY = {"slow", "moderate", "fast"}
ALLOWED_CHANGE_STATUS = {"stable", "new", "experimental", "deprecated", "removed", "planned"}
ALLOWED_MAP_ACTION = {"add", "modify", "downgrade", "remove", "none"}
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def validate(path: Path) -> tuple[list[str], list[str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    warnings: list[str] = []
    required = {
        "schema_version", "domain_map_id", "version", "generated_at", "domain", "freshness",
        "modules", "relationships", "typical_traversal", "sources"
    }
    missing = sorted(required - data.keys())
    if missing:
        errors.append(f"missing top-level fields: {', '.join(missing)}")
    if not SEMVER.match(str(data.get("version", ""))):
        errors.append("version must be semantic version x.y.z")

    nodes: dict[str, dict] = {}
    knowledge_points = 0

    def walk(node: object, parent_rank: int, trail: str) -> None:
        nonlocal knowledge_points
        if not isinstance(node, dict):
            errors.append(f"{trail}: node must be an object")
            return
        node_id = node.get("id")
        node_type = node.get("type")
        if not isinstance(node_id, str) or not node_id:
            errors.append(f"{trail}: missing id")
            return
        if node_id in nodes:
            errors.append(f"duplicate node id: {node_id}")
        nodes[node_id] = node
        if node_type not in TYPE_RANK:
            errors.append(f"{node_id}: invalid type {node_type!r}")
            return
        rank = TYPE_RANK[node_type]
        if rank <= parent_rank:
            errors.append(f"{node_id}: {node_type} cannot appear under rank {parent_rank}")
        children = node.get("children", [])
        if node_type == "knowledge_point":
            knowledge_points += 1
            if children:
                errors.append(f"{node_id}: knowledge_point cannot have children")
            for field in ("title", "definition", "importance", "source_ids"):
                if field not in node:
                    errors.append(f"{node_id}: missing {field}")
            return
        if not isinstance(children, list) or not children:
            errors.append(f"{node_id}: non-leaf node needs children")
            return
        if node_type in {"topic", "chapter"} and len(children) < 2:
            errors.append(f"{node_id}: optional intermediate nodes need at least two children")
        for index, child in enumerate(children):
            walk(child, rank, f"{trail}/{index}")

    modules = data.get("modules", [])
    if not isinstance(modules, list) or not modules:
        errors.append("modules must be a non-empty array")
    else:
        for index, module in enumerate(modules):
            if isinstance(module, dict) and module.get("type") != "module":
                errors.append(f"modules[{index}] must have type module")
            walk(module, -1, f"modules/{index}")
    if knowledge_points == 0:
        errors.append("map must contain at least one knowledge_point")

    source_ids: set[str] = set()
    for index, source in enumerate(data.get("sources", [])):
        if not isinstance(source, dict):
            errors.append(f"sources[{index}] must be an object")
            continue
        source_id = source.get("id")
        if not source_id:
            errors.append(f"sources[{index}] missing id")
        elif source_id in source_ids:
            errors.append(f"duplicate source id: {source_id}")
        else:
            source_ids.add(source_id)
        for field in ("title", "url", "verified_at"):
            if not source.get(field):
                errors.append(f"source {source_id or index}: missing {field}")

    for source in data.get("sources", []):
        if not isinstance(source, dict):
            continue
        for node_id in source.get("supports", []):
            if node_id not in nodes:
                errors.append(f"source {source.get('id')}: unknown supported node {node_id}")

    freshness = data.get("freshness")
    if not isinstance(freshness, dict):
        errors.append("freshness must be an object")
    else:
        for field in ("as_of", "volatility", "window_from", "window_reason", "current_baseline", "recent_changes"):
            if field not in freshness:
                errors.append(f"freshness: missing {field}")
        for field in ("as_of", "window_from"):
            if not ISO_DATE.match(str(freshness.get(field, ""))):
                errors.append(f"freshness.{field} must be YYYY-MM-DD")
        if freshness.get("volatility") not in ALLOWED_VOLATILITY:
            errors.append("freshness.volatility must be slow, moderate, or fast")
        baseline = freshness.get("current_baseline")
        if not isinstance(baseline, dict) or not baseline.get("label"):
            errors.append("freshness.current_baseline needs label")
        else:
            for source_id in baseline.get("source_ids", []):
                if source_id not in source_ids:
                    errors.append(f"freshness.current_baseline: unknown source id {source_id}")
        changes = freshness.get("recent_changes")
        if not isinstance(changes, list):
            errors.append("freshness.recent_changes must be an array")
        else:
            change_ids: set[str] = set()
            for index, change in enumerate(changes):
                if not isinstance(change, dict):
                    errors.append(f"freshness.recent_changes[{index}] must be an object")
                    continue
                change_id = change.get("id")
                if not change_id:
                    errors.append(f"freshness.recent_changes[{index}] missing id")
                elif change_id in change_ids:
                    errors.append(f"duplicate change id: {change_id}")
                else:
                    change_ids.add(change_id)
                if change.get("status") not in ALLOWED_CHANGE_STATUS:
                    errors.append(f"change {change_id or index}: invalid status {change.get('status')!r}")
                if change.get("map_action") not in ALLOWED_MAP_ACTION:
                    errors.append(f"change {change_id or index}: invalid map_action {change.get('map_action')!r}")
                for node_id in change.get("affected_node_ids", []):
                    if node_id not in nodes:
                        errors.append(f"change {change_id or index}: unknown affected node {node_id}")
                for source_id in change.get("source_ids", []):
                    if source_id not in source_ids:
                        errors.append(f"change {change_id or index}: unknown source id {source_id}")

    for node_id, node in nodes.items():
        for source_id in node.get("source_ids", []):
            if source_id not in source_ids:
                errors.append(f"{node_id}: unknown source id {source_id}")
        for target in node.get("prerequisites", []) + node.get("leads_to", []):
            if target not in nodes:
                errors.append(f"{node_id}: unknown node reference {target}")

    for index, relation in enumerate(data.get("relationships", [])):
        if not isinstance(relation, dict):
            errors.append(f"relationships[{index}] must be an object")
            continue
        for endpoint in ("from", "to"):
            if relation.get(endpoint) not in nodes:
                errors.append(f"relationships[{index}]: unknown {endpoint} {relation.get(endpoint)!r}")
        if relation.get("type") not in ALLOWED_RELATIONS:
            errors.append(f"relationships[{index}]: invalid type {relation.get('type')!r}")

    for node_id in data.get("typical_traversal", []):
        if node_id not in nodes:
            errors.append(f"typical_traversal: unknown node {node_id}")

    stages = {module.get("stage") for module in modules if isinstance(module, dict)}
    for expected in ("foundation", "core"):
        if expected not in stages:
            warnings.append(f"no top-level module tagged {expected}")
    return errors, warnings


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_domain_map.py DOMAIN_MAP_JSON", file=sys.stderr)
        return 2
    try:
        errors, warnings = validate(Path(sys.argv[1]))
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
