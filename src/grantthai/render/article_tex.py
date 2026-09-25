"""grantthai.render.article_tex — `build --route academic-article --format tex`.

    render(raw, project_dir, *, route, export, sub_profile, as_of, structure_profile, glosa_audit) -> (text, Result)

Fills a sha256-pinned, byte-identical copy of the glosa-registered GLOSA-7SSA
LaTeX template (templates/tex/glosa_7ssa_v1.tex; provenance in
templates/tex/SOURCE.yaml) from the work object, through the fill map
(templates/tex/glosa_7ssa_v1.fillmap.yaml, one row per [FILL token).
Literal, LaTeX-escaped replacement only: GrantThai composes no text, runs no
LaTeX engine and writes exactly one file, build/ACADEMIC_ARTICLE.tex
(through grantthai.render.build_route). A value the fill map cannot resolve
prints [NEEDS_INPUT: ...]; review and audit state is always NEEDS_INPUT;
the publisher-policy cells print NEEDS_VERIFICATION.

English only: pdflatex cannot set Thai script, so a Thai value prints a
NEEDS_INPUT note instead and a Thai-heading structure profile adds one note
that the Thai layout is not exported (docs/deviations.md; CX-7SSA-06).

Deterministic: no timestamps. This module MUST NEVER import grantthai.assist,
grantthai.mcp, grantthai.api, or any LLM SDK (tools/ci/check_no_ai_import.py).
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

from grantthai.core import project as P
from grantthai.render import article as A
from grantthai.routes import registry as R
from grantthai.routes import structure as ST
from grantthai.validators import article as ART
from grantthai.validators import engine as E

THAI_RE = re.compile(r"[\u0E00-\u0E7F]")
_ESC = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
        "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}"}
POLICY_WORDS = ("check", "recommended", "documented", "journal-dependent")
TOOL_KEYS = ("name", "developer", "version", "used_on", "purpose", "stages")


def escape(text: str) -> str:
    return "".join(_ESC.get(c, c) for c in text)


def fill_tokens(text: str) -> list[tuple[int, int]]:
    """(start, end) of every [FILL ...] token, brackets balanced, in order."""
    out, i = [], 0
    while True:
        j = text.find("[FILL", i)
        if j < 0:
            return out
        depth, k = 0, j
        while k < len(text):
            if text[k] == "[":
                depth += 1
            elif text[k] == "]":
                depth -= 1
                if depth == 0:
                    break
            k += 1
        out.append((j, k + 1))
        i = k + 1


def _anchor(text: str, span: tuple[int, int]) -> str:
    return " ".join(text[span[0]:span[1]].split())[:40]


def load_template(export: dict) -> tuple[str, dict]:
    """(template text, fill map); refuses a template whose sha256, token
    count or token anchors do not match the pinned data."""
    src = P._read_yaml(export["source"]) or {}
    pin = next((f for f in src.get("files") or [] if f.get("path") == export["template"]), None)
    if pin is None:
        raise R.RouteError(f"{export['source']} does not pin {export['template']}")
    raw = (P.DATA_ROOT / export["template"]).read_bytes()
    if hashlib.sha256(raw).hexdigest() != pin.get("sha256"):
        raise R.RouteError(f"{export['template']} does not match its pinned sha256 in {export['source']}; "
                           "nothing was written")
    text = raw.decode("utf-8")
    fm = P._read_yaml(export["fillmap"]) or {}
    rows = fm.get("rows") or []
    spans = fill_tokens(text)
    if fm.get("template_sha256") != pin["sha256"] or len(rows) != len(spans):
        raise R.RouteError(f"{export['fillmap']} does not match {export['template']} "
                           f"({len(rows)} rows, {len(spans)} tokens); nothing was written")
    for row, span in zip(rows, spans):
        if row.get("anchor") != _anchor(text, span):
            raise R.RouteError(f"{export['fillmap']} row {row.get('n')} anchor does not match the template")
    return text, fm


class _Values:
    """Resolves fill-map sources against one work object."""

    def __init__(self, raw: dict, recs: dict, route, profile: dict | None):
        self.raw, self.recs, self.route, self.profile = raw, recs, route, profile
        self.team = {m.get("id"): m for m in self._items("PROFILE.TEAM.MEMBERS")}
        authors = sorted(self._items("ARTICLE.FRONT.AUTHORS"),
                         key=lambda a: (a.get("order") if isinstance(a.get("order"), int) else 10 ** 6,
                                        str(a.get("id"))))
        self.authors = authors
        auth = raw.get("authoring") if isinstance(raw.get("authoring"), dict) else {}
        self.decl = auth.get("ai_use_declaration") if isinstance(auth.get("ai_use_declaration"), dict) else {}
        self.tools = [t for t in self.decl.get("tools") or [] if isinstance(t, dict)]
        self.body = self._items(ST.BODY_SECTIONS)
        self.ces = A.core_epistemic(raw, recs)
        self.disclosed = [t.get("name") for t in self.tools if t.get("name")] + \
            list(auth.get("tools_disclosed") or [])

    def value(self, fid: str) -> Any:
        return (self.recs.get(fid) or {}).get("value")

    def _items(self, fid: str) -> list[dict]:
        v = self.value(fid)
        return [x for x in v if isinstance(x, dict)] if isinstance(v, list) else []

    @staticmethod
    def _text(v: Any) -> list[str]:
        """Strings of a value: a string, a list's strings, an object's filled
        string values in key order."""
        if isinstance(v, str):
            return [v] if ST.filled(v) else []
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            return [str(v)]
        if isinstance(v, list):
            vals = [x for x in v if isinstance(x, str) and ST.filled(x)]
            return ["; ".join(vals)] if vals else []
        if isinstance(v, dict):
            return [x for x in v.values() if isinstance(x, str) and ST.filled(x)]
        return []

    def _author_name(self, a: dict) -> str | None:
        n = (self.team.get(a.get("member_id")) or {}).get("full_name")
        return n if ST.filled(n) else None

    def _is_ai(self, name: str) -> bool:
        return ART._generic_ai_name(name) or any(ART._names_tool_in_name(name, t) for t in self.disclosed if t)

    def one(self, src: str) -> list[str]:
        kind, _, arg = src.partition(":")
        if kind == "field":
            fid, _, key = arg.partition("#")
            v = self.value(fid)
            if key:
                v = v.get(key) if isinstance(v, dict) else None
            return self._text(v)
        if kind == "slot":
            spec, _, k = arg.partition("@")
            sid, _, slot = spec.partition(".")
            texts = [it.get("text") for it in self.body
                     if it.get("ssa_sector") == sid and it.get("ssa_slot") == slot and ST.filled(it.get("text"))]
            if k:
                idx = int(k) - 1
                return [texts[idx]] if 0 <= idx < len(texts) else []
            if texts:
                return texts
            sec = next((s for s in ST.sectors(self.route) if s["id"] == sid), {}) if ST.has_profiles(self.route) \
                else {}
            ref = next((s.get("from_field") for s in sec.get("slots") or [] if s["slot"] == slot), None)
            return self.one("field:" + ref) if ref else []
        if kind == "author":
            which, _, key = arg.partition(".")
            if which == "corresponding":
                a = next((x for x in self.authors if x.get("corresponding") is True), None)
                n = self._author_name(a) if a else None
                return [n] if n and not self._is_ai(n) else []
            idx = int(which) - 1
            if not 0 <= idx < len(self.authors):
                return []
            a = self.authors[idx]
            if key == "name":
                n = self._author_name(a)
                return [n] if n and not self._is_ai(n) else []
            if key == "orcid":
                return self._text((self.team.get(a.get("member_id")) or {}).get("orcid"))
            if key == "affiliation":
                return self._text(a.get("affiliation_as_typed")) or \
                    self._text((self.team.get(a.get("member_id")) or {}).get("organization"))
            return []
        if kind == "authors" and arg == "human_names":
            names = [n for n in (self._author_name(a) for a in self.authors) if n and not self._is_ai(n)]
            return [", ".join(names)] if names else []
        if kind == "credit":
            ids = [c.get("member_id") for c in self._items("ARTICLE.FRONT.CONTRIBUTIONS")
                   if arg in (c.get("roles") or [])]
            names = [(self.team.get(i) or {}).get("full_name") for i in ids]
            names = [n for n in names if ST.filled(n) and not self._is_ai(n)]
            return [", ".join(names)] if names else []
        if kind == "ces":
            v = {"experience": self.ces["experience_based_expert"], "interactional": self.ces["interactional_expert"],
                 "ai": self.ces["ai_models"]}.get(arg, "")
            return [] if not ST.filled(v) or v.startswith("NEEDS_INPUT") else [v]
        if kind == "ai_tool":
            which, _, key = arg.partition(".")
            idx = int(which) - 1
            if not 0 <= idx < len(self.tools) or key not in TOOL_KEYS:
                return []
            return self._text(self.tools[idx].get(key))
        if kind == "ai_decl":
            return self._text(self.decl.get(arg))
        if kind == "statement":
            return [it.get("text") for it in self._items("ARTICLE.STATEMENT.OTHER")
                    if it.get("kind") == arg and ST.filled(it.get("text"))]
        if kind in ("reference", "references_from"):
            refs = self.value("CORE.NARRATIVE.REFERENCES")
            refs = [r for r in refs if isinstance(r, str) and ST.filled(r)] if isinstance(refs, list) else \
                ([refs] if isinstance(refs, str) and ST.filled(refs) else [])
            idx = int(arg) - 1
            if kind == "reference":
                return [refs[idx]] if 0 <= idx < len(refs) else []
            return refs[idx:]
        if kind == "claim":
            claims = [r for r in ((P.normalized(self.raw).get("chain") or {}).get("Claim") or [])
                      if isinstance(r, dict)]
            idx = int(arg) - 1
            return self._text(claims[idx].get("value")) if 0 <= idx < len(claims) else []
        if kind == "work" and arg == "content_sha256":
            from grantthai.core.object_hash import content_sha256
            return [f"work object content_sha256 {content_sha256(self.raw)}"]
        return []

    def resolve(self, source: str) -> list[str]:
        if "|" in source:
            for alt in source.split("|"):
                got = self.resolve(alt)
                if got:
                    return got
            return []
        out = []
        for part in source.split("+"):
            out += self.one(part)
        return out


def _needs(label: str, why: str = "") -> str:
    return r"[NEEDS\_INPUT: " + escape(" ".join(label.split())) + (f"; {escape(why)}" if why else "") + "]"


def _fold(s: str, block: bool) -> str:
    if block:
        paras = [" ".join(p.split()) for p in re.split(r"\n\s*\n", s)]
        return "\n\n".join(p for p in paras if p)
    return " ".join(s.split())


def _value_text(row: dict, vals: list[str], label: str) -> str:
    if any(THAI_RE.search(v) for v in vals):
        return _needs(label, "the value is Thai text; pdflatex cannot set Thai script; supply an English value")
    joined = "\n\n".join(vals) if row.get("block") else "; ".join(vals)
    return escape(_fold(joined, bool(row.get("block"))))


def resolved_headings(route, profile: dict | None, article_type: str | None) -> dict:
    """S1..S7 -> English heading: the article-type overlay, else the world
    profile's headings (the same resolver as the Markdown body, CX-7SSA-02)."""
    world = ST.load_profile(route, "7ssa-world")
    base = {s["sectors"][0]: s["heading"] for s in world["visible_sections"]}
    ov = ST.overlay(route, article_type)
    return dict(ov["headings_en"]) if ov else base


def fill(text: str, fm: dict, values: _Values, *, headings: dict, glosa_audit: bool, header: str,
         thai_profile: str | None) -> str:
    spans = fill_tokens(text)
    out, last = [], 0
    for row, (a, b) in zip(fm["rows"], spans):
        out.append(text[last:a])
        src, label = row["source"], row.get("label") or f"item {row['n']}"
        if src == "keep":
            out.append(text[a:b])
        elif src == "empty":
            pass
        elif src == "NEEDS_INPUT":
            out.append(_needs(label))
        elif src == "profile:target_note":
            if thai_profile:
                out.append(escape(f"Thai-journal layout {thai_profile} selected") + " "
                           + _needs("Thai headings and Thai script are not in this pdflatex export; this file uses "
                                    "the English 7SSA headings. Use a XeLaTeX derivative for Thai"))
            else:
                out.append(_needs(label))
        elif src == "references_from:2":
            vals = values.resolve(src)
            if not vals:
                out.append(_needs(label))
            else:
                first = _value_text(row, [vals[0]], label)
                rest = "".join(f"\n\n\\bibitem{{grantthai-ref{i}}}\n" + _value_text(row, [v], label)
                               for i, v in enumerate(vals[1:], start=3))
                out.append(first + rest)
        else:
            vals = values.resolve(src)
            out.append(_value_text(row, vals, label) if vals else _needs(label, "from " + src.replace("|", " or ")))
        last = b
    out.append(text[last:])
    filled = "".join(out)
    # sector section titles -> the resolved English 7SSA headings
    for sid, head in headings.items():
        n = sid[1:]
        filled = re.sub(r"\\section\{[^}]*\}(\n\\label\{sec:s" + n + r"\})",
                        lambda m, h=head: "\\section{" + escape(h) + "}" + m.group(1), filled, count=1)
    if not glosa_audit:
        filled = filled.replace("\n\\glosaaudittrue\n", "\n\\glosaauditfalse\n", 1)
    filled = _policy_cells(filled)
    return header + filled


def _policy_cells(text: str) -> str:
    """The internal policy-interoperability table: every relayed publisher
    cell becomes NEEDS_VERIFICATION (never a GrantThai fact)."""
    start = text.find("\\label{app:policy-map}")
    if start < 0:
        return text
    mid = text.find("\\midrule", start)
    end = text.find("\\bottomrule", mid)
    if mid < 0 or end < 0:
        return text
    rows = text[mid:end].split("\n")
    fixed = []
    for line in rows:
        if "&" in line and line.rstrip().endswith("\\\\"):
            cells = line.rstrip()[:-2].split("&")
            cells = [cells[0]] + [(" NEEDS\\_VERIFICATION " if c.strip() in POLICY_WORDS else c) for c in cells[1:]]
            line = "&".join(cells).rstrip() + "\\\\"
        fixed.append(line)
    return text[:mid] + "\n".join(fixed) + text[end:]


def render(raw: dict, project_dir: Path | None = None, *, route, export: dict, sub_profile=None, as_of=None,
           structure_profile=None, glosa_audit: bool = False):
    result = E.run(raw, project_dir, as_of, route=route.id, sub_profile=sub_profile,
                   structure_profile=structure_profile)
    pid = result.structure_profile
    family = export.get("requires_structure_profile_family")
    if family and not pid:
        cands = ", ".join(ST.profile_ids(route)) or "none"
        raise R.RouteError(f"--format {export['format']} needs a {family} structure profile; none is selected. "
                           f"Choose one yourself (routing.structure_profiles.{route.id} or --structure-profile: "
                           f"{cands}); GrantThai never chooses. Nothing was written")
    if pid not in ST.profile_ids(route):
        raise R.RouteError(f"structure profile {pid!r} is not shipped for route {route.id}; nothing was written")
    profile = ST.load_profile(route, pid)
    text, fm = load_template(export)
    recs = P.records_by_id(P.normalized(raw))
    atype = (recs.get(ST.ARTICLE_TYPE) or {}).get("value")
    values = _Values(raw, recs, route, profile)
    thai = pid if profile.get("heading_lang") == "th" else None
    header_lines = [
        P.notice_constant(), route.route_notice_en or "",
        f"Generated by GrantThai from work object {P.work_id(raw)} (route {route.id}, structure profile {pid}).",
        "FICTIONAL example: nothing here is a manuscript for any real venue." if raw.get("fictional") is True else
        "A draft for the researcher to check; it submits nothing. Human final approval is always required.",
        f"Template {export['template']} sha256 {fm['template_sha256']} (provenance: {export['source']}).",
        f"Validation: BLOCK {result.report['summary']['block']} / REVIEW {result.report['summary']['review']} / "
        f"INFO {result.report['summary']['info']} (see the Markdown overview for the findings).",
    ]
    header = "".join(f"% {ln}\n" for line in header_lines if line for ln in line.splitlines()) + "%\n"
    filled = fill(text, fm, values, headings=resolved_headings(route, profile, atype if isinstance(atype, str) else None),
                  glosa_audit=glosa_audit, header=header, thai_profile=thai)
    return filled, result
