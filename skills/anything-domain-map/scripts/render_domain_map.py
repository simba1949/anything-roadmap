#!/usr/bin/env python3
"""Embed a validated domain-map.json into the offline HTML template."""

from __future__ import annotations

import json
import sys
from pathlib import Path

START = "/* DOMAIN_MAP_DATA_START */"
END = "/* DOMAIN_MAP_DATA_END */"


def main() -> int:
    if len(sys.argv) not in (3, 4):
        print("usage: render_domain_map.py DOMAIN_MAP_JSON OUTPUT_HTML [TEMPLATE_HTML]", file=sys.stderr)
        return 2

    source = Path(sys.argv[1]).resolve()
    output = Path(sys.argv[2]).resolve()
    template = (
        Path(sys.argv[3]).resolve()
        if len(sys.argv) == 4
        else Path(__file__).resolve().parent.parent / "references" / "template.html"
    )

    data = json.loads(source.read_text(encoding="utf-8"))
    html = template.read_text(encoding="utf-8")
    if html.count(START) != 1 or html.count(END) != 1:
        raise ValueError("template must contain exactly one domain-map marker pair")
    if html.index(START) >= html.index(END):
        raise ValueError("domain-map markers are reversed")

    payload = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")
    replacement = f"{START}\nconst DOMAIN_MAP = {payload};\n{END}"
    rendered = html[: html.index(START)] + replacement + html[html.index(END) + len(END) :]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8", newline="\n")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

