#!/usr/bin/env python3
"""Embed a domain map and learning path into the offline roadmap viewer."""

from __future__ import annotations

import json
import sys
from pathlib import Path

DM_START = "/* DOMAIN_MAP_DATA_START */"
DM_END = "/* DOMAIN_MAP_DATA_END */"
LP_START = "/* LEARNING_PATH_DATA_START */"
LP_END = "/* LEARNING_PATH_DATA_END */"


def replace_block(text: str, start: str, end: str, declaration: str) -> str:
    if text.count(start) != 1 or text.count(end) != 1 or text.index(start) >= text.index(end):
        raise ValueError(f"template needs exactly one ordered marker pair: {start}, {end}")
    return text[: text.index(start)] + f"{start}\n{declaration}\n{end}" + text[text.index(end) + len(end) :]


def main() -> int:
    if len(sys.argv) not in (4, 5):
        print("usage: render_roadmap.py DOMAIN_MAP_JSON LEARNING_PATH_JSON OUTPUT_HTML [TEMPLATE_HTML]", file=sys.stderr)
        return 2
    domain_path, learning_path, output_path = map(lambda p: Path(p).resolve(), sys.argv[1:4])
    template = Path(sys.argv[4]).resolve() if len(sys.argv) == 5 else Path(__file__).resolve().parent.parent / "references" / "template.html"
    domain = json.loads(domain_path.read_text(encoding="utf-8"))
    learning = json.loads(learning_path.read_text(encoding="utf-8"))
    html = template.read_text(encoding="utf-8")
    domain_json = json.dumps(domain, ensure_ascii=False, indent=2).replace("</", "<\\/")
    learning_json = json.dumps(learning, ensure_ascii=False, indent=2).replace("</", "<\\/")
    html = replace_block(html, DM_START, DM_END, f"const DOMAIN_MAP = {domain_json};")
    html = replace_block(html, LP_START, LP_END, f"const LEARNING_PATH = {learning_json};")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8", newline="\n")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

