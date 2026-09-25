#!/usr/bin/env python3
"""tools/ci/make_negative_fixtures.py

Write seeded-bad fixtures at TEST RUN TIME, so that no personal-data-shaped
or secret-shaped value is ever committed to this repository.

  pii       a file with an e-mail address on a reserved test domain
            (RFC 2606 ".test"), a phone number that cannot be issued
            (000-000-0000), and a 13-digit number that passes the Thai
            national-ID checksum but starts with 0, which no real Thai ID
            does. It is regenerated with random digits on every run.
  gitleaks  a file with an AWS-access-key-shaped string built from random
            characters on every run.
  case      two files whose paths differ only by letter case (generated,
            never committed, because committing them is the defect).

Usage:
    python tools/ci/make_negative_fixtures.py <pii|gitleaks|case> <out_dir>
"""
from __future__ import annotations

import random
import string
import sys
from pathlib import Path


def thai_id_check_digit(first12: str) -> str:
    total = sum(int(d) * (13 - i) for i, d in enumerate(first12))
    return str((11 - (total % 11)) % 10)


def synthetic_thai_id(rng: random.Random) -> str:
    first12 = "0" + "".join(rng.choice(string.digits) for _ in range(11))
    return first12 + thai_id_check_digit(first12)


def make_pii(out: Path, rng: random.Random) -> Path:
    user = "fixture" + "".join(rng.choice(string.ascii_lowercase) for _ in range(6))
    email = user + "@" + "mailbox.test"
    phone = "-".join(["000", "000", "0000"])
    body = (
        "FIXTURE - generated at test time; every value is synthetic.\n"
        f"Contact: {email}, phone {phone}, ID {synthetic_thai_id(rng)}\n"
    )
    path = out / "generated_contact.md"
    path.write_text(body, encoding="utf-8")
    return path


def make_gitleaks(out: Path, rng: random.Random) -> Path:
    key = "AK" + "IA" + "".join(rng.sample(string.ascii_uppercase + "234567", 16))
    path = out / "generated_secret.env"
    path.write_text(f"AWS_ACCESS_KEY_ID={key}\n", encoding="utf-8")
    return path


def make_case(out: Path, rng: random.Random) -> Path:
    for name in ("notes.md", "NOTES.md"):
        (out / name).write_text("FIXTURE - case-collision pair.\n", encoding="utf-8")
    return out / "NOTES.md"


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] not in {"pii", "gitleaks", "case"}:
        print(__doc__)
        return 2
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    rng = random.Random()
    maker = {"pii": make_pii, "gitleaks": make_gitleaks, "case": make_case}[sys.argv[1]]
    path = maker(out, rng)
    print(f"wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
