#!/usr/bin/env python3
"""tools/registry/build_nriis_fields.py

Generate registry/nriis-fields.jsonl (render-only NRIIS.<TAB>.<FIELD>
records) from two committed files:

  - registry/fields.jsonl               (core field records)
  - mappings/nriis/section_to_tab.yaml  (the single section -> tab table)

nriis-fields.jsonl is never edited by hand. Run this script after changing
either input; `--check` exits non-zero when the committed file is out of
date (used by tests/test_registry.py).

Every generated record keeps the NEEDS_VERIFICATION marker: the tab, the
tab order and the labels come from one observed form and are not confirmed
from a public document (founder ruling K14, see GOVERNANCE.md).

Usage:
    python tools/registry/build_nriis_fields.py [--root .] [--check]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml


def build(root: Path) -> str:
    fields = [
        json.loads(line)
        for line in (root / "registry" / "fields.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    s2t = yaml.safe_load((root / "mappings" / "nriis" / "section_to_tab.yaml").read_text(encoding="utf-8"))
    tab_of = {m["section"]: m["tab"] for m in s2t["mappings"]}
    order = {tab: 0 for tab in s2t["tab_order"]}
    lines = []
    for f in fields:
        tab = tab_of[f["section"]]
        order[tab] += 1
        rec = {
            "field_id": "NRIIS." + tab + "." + f["field_id"].replace(".", "_"),
            "tab": tab,
            "entry_order": order[tab],
            "label_en": f["label_en"],
            "label_en_basis": f["label_en_basis"],
            "label_th": f["label_th"],
            "observed_form": s2t["observed_form"],
            "required": f["required"],
            "input_control": f["input_control"],
            "dependencies": f["dependencies"],
            "core_field_id": f["field_id"],
            "markers": ["NEEDS_VERIFICATION"],
        }
        lines.append(json.dumps(rec, ensure_ascii=False))
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    target = root / "registry" / "nriis-fields.jsonl"
    text = build(root)
    if args.check:
        current = target.read_text(encoding="utf-8") if target.exists() else ""
        if current != text:
            print("registry/nriis-fields.jsonl is out of date; run tools/registry/build_nriis_fields.py")
            return 1
        print("registry/nriis-fields.jsonl is up to date")
        return 0
    target.write_text(text, encoding="utf-8")
    print(f"wrote {target.relative_to(root)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
