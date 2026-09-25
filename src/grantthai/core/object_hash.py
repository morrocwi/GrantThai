"""grantthai.core.object_hash — reference implementation of
spec/common/object-hash.md (content_sha256 and state_sha256).

Deliberately small and stdlib-only apart from PyYAML for loading. The
v0.1 core may replace it, but must produce the same bytes and hashes for
every vector in tests/golden/object-hash/.
"""
from __future__ import annotations

import copy
import hashlib
import math
import re
import unicodedata
from typing import Any

# Keys that carry review/validation STATE, not authored content
# (spec/common/object-hash.md, "What the content hash excludes").
TOP_LEVEL_STATE_KEYS = ("review_records", "lock")
RECORD_STATE_KEYS = ("status",)
MAPPING_STATE_KEYS = ("acceptance_state", "review")


def yaml12_safe_loader():
    """A PyYAML SafeLoader restricted towards YAML 1.2 core-schema behaviour:
    no implicit timestamps (dates stay strings) and booleans only for
    true/false (not yes/no/on/off)."""
    import yaml

    class Loader(yaml.SafeLoader):
        pass

    resolvers = {}
    for first, entries in yaml.SafeLoader.yaml_implicit_resolvers.items():
        kept = [(tag, rx) for tag, rx in entries
                if tag not in ("tag:yaml.org,2002:timestamp", "tag:yaml.org,2002:bool")]
        resolvers[first] = kept
    Loader.yaml_implicit_resolvers = resolvers
    Loader.add_implicit_resolver(
        "tag:yaml.org,2002:bool",
        re.compile(r"^(?:true|True|TRUE|false|False|FALSE)$"),
        list("tTfF"),
    )
    return Loader


def load_project_text(text: str) -> Any:
    import yaml
    return yaml.load(text, Loader=yaml12_safe_loader())  # noqa: S506 - SafeLoader subclass


def _nfc(obj: Any) -> Any:
    if isinstance(obj, str):
        return unicodedata.normalize("NFC", obj)
    if isinstance(obj, list):
        return [_nfc(x) for x in obj]
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if not isinstance(k, str):
                raise TypeError(f"non-string key {k!r}: quote it in project.yaml")
            nk = unicodedata.normalize("NFC", k)
            if nk in out:
                raise ValueError(f"two keys normalise to the same NFC key {nk!r}")
            out[nk] = _nfc(v)
        return out
    return obj


def _jcs_number(x: Any) -> str:
    """ECMAScript Number::toString, as RFC 8785 section 3.2.2.3 requires."""
    if isinstance(x, bool):
        raise TypeError("bool is not a number")
    if isinstance(x, int):
        if abs(x) > 2 ** 53:
            raise ValueError(f"integer {x} is outside the IEEE-754 safe range")
        return str(x)
    if not math.isfinite(x):
        raise ValueError("NaN/Infinity are not allowed")
    if x == 0:
        return "0"
    sign = "-" if x < 0 else ""
    r = repr(abs(x))  # shortest round-trip digits
    if "e" in r:
        mant, exp = r.split("e")
        exp = int(exp)
    else:
        mant, exp = r, 0
    if "." in mant:
        ip, fp = mant.split(".")
    else:
        ip, fp = mant, ""
    digits = (ip + fp).lstrip("0")
    # n = position of the decimal point relative to the digit string
    lead_zeros = len(ip + fp) - len((ip + fp).lstrip("0"))
    n = len(ip) + exp - lead_zeros
    digits = digits.rstrip("0") or "0"
    k = len(digits)
    if k <= n <= 21:
        s = digits + "0" * (n - k)
    elif 0 < n <= 21:
        s = digits[:n] + "." + digits[n:]
    elif -6 < n <= 0:
        s = "0." + "0" * (-n) + digits
    else:
        e = n - 1
        es = ("+" if e >= 0 else "-") + str(abs(e))
        s = digits[0] + ("." + digits[1:] if k > 1 else "") + "e" + es
    return sign + s


def _jcs_string(s: str) -> str:
    out = ['"']
    for ch in s:
        o = ord(ch)
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif ch == "\b":
            out.append("\\b")
        elif ch == "\f":
            out.append("\\f")
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        elif o < 0x20:
            out.append("\\u%04x" % o)
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def jcs(obj: Any) -> str:
    """RFC 8785 JSON Canonicalization Scheme serialisation."""
    if obj is None:
        return "null"
    if obj is True:
        return "true"
    if obj is False:
        return "false"
    if isinstance(obj, (int, float)):
        return _jcs_number(obj)
    if isinstance(obj, str):
        return _jcs_string(obj)
    if isinstance(obj, list):
        return "[" + ",".join(jcs(x) for x in obj) + "]"
    if isinstance(obj, dict):
        keys = sorted(obj, key=lambda k: k.encode("utf-16-be"))
        return "{" + ",".join(_jcs_string(k) + ":" + jcs(obj[k]) for k in keys) + "}"
    raise TypeError(f"type {type(obj).__name__} cannot appear in project.yaml; quote dates as strings")


def _iter_records(project: dict):
    for rec in project.get("fields") or []:
        if isinstance(rec, dict):
            yield rec
    for recs in (project.get("chain") or {}).values():
        for rec in recs or []:
            if isinstance(rec, dict):
                yield rec


def content_view(project: dict) -> dict:
    """The project object with every review/validation STATE key removed."""
    obj = copy.deepcopy(project)
    for k in TOP_LEVEL_STATE_KEYS:
        obj.pop(k, None)
    for rec in _iter_records(obj):
        for k in RECORD_STATE_KEYS:
            rec.pop(k, None)
    for m in obj.get("mappings") or []:
        if isinstance(m, dict):
            for k in MAPPING_STATE_KEYS:
                m.pop(k, None)
    return obj


def canonical_bytes(obj: Any) -> bytes:
    return jcs(_nfc(obj)).encode("utf-8")


def content_sha256(project: dict) -> str:
    return hashlib.sha256(canonical_bytes(content_view(project))).hexdigest()


def state_sha256(project: dict) -> str:
    return hashlib.sha256(canonical_bytes(project)).hexdigest()
