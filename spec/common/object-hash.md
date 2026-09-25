# Project object hashes (`content_sha256`, `state_sha256`)

Draft, version 0.3. Two hashes of the work object (`work.yaml` 0.3, or a
legacy `project.yaml` 0.2, read unchanged), defined once and used everywhere
a hash of the object appears. 0.3 adds one exclusion, `routing` (item 4
below); a 0.2 file has no `routing` key, so its hashes are unchanged.

| Hash | Covers | Used by |
|---|---|---|
| `content_sha256` | what the person **authored**: every value, marker, hold reason, provenance, link, source reference and source entry | review records (`content_sha256`), `lock.locked_content_sha256`, output frontmatter `project_content_sha256`, validation reports |
| `state_sha256` | the whole file, including statuses, review records and the lock | output frontmatter `project_state_sha256`, validation reports (a fingerprint of exactly what was rendered) |

Why two: a review record binds to what was reviewed. Recording the review,
promoting field statuses through it, a validator persisting
`STRUCTURE_CHECKED`/`LOGIC_LINKED`, and applying the object LOCK are all
**state** changes. They must not change the hash the review bound to, or
every review would go stale the moment it took effect and the LOCK gate
("every required field at `HUMAN_REVIEWED` or above") could never be met.

## What `content_sha256` excludes

Exactly these keys, and nothing else:

1. the top-level keys `review_records` and `lock`;
2. `status` on every field record (under `fields` and under every
   `chain.<Node>`, including Evidence records);
3. `acceptance_state` and `review` on every item of `mappings` (accepting
   or reviewing a mapping is a review act);
4. the top-level key `routing` (0.3, decision K-R3). Choosing an output
   route is not authored content: declaring, adding or changing a route or
   a sub-profile makes no review record and no lock stale. `work_type`
   stays inside the hash (it is part of what the person declares about the
   work). The legacy top-level `form_profile` also stays inside the hash,
   exactly as in 0.2; only the 0.3 `routing.sub_profiles` spelling is
   excluded, so a `migrate` that moves it reports the gates that go stale.

Everything else is content, including `work_type`, `markers` and `hold_reason` (an
edit to them is an authored change and regresses the field to `DRAFT`,
`spec/common/status_permissions.yaml`), `links`, `source_ids` and the
top-level `sources`.

## Algorithm (both hashes)

1. **Load.** Parse the work object (`work.yaml` or `project.yaml`) with a YAML 1.2 core-schema safe loader
   into plain data (maps, lists, strings, numbers, booleans, null).
   Booleans are only `true`/`false` (never `yes`/`no`/`on`/`off`) and
   there are no implicit timestamps: dates are written as quoted strings
   (`"2026-09-25"`); an unquoted date loads as a string under this loader,
   and the schemas require the `YYYY-MM-DD` string form. Map keys must be
   strings. Reference loader: `grantthai.core.object_hash.yaml12_safe_loader`
   (PyYAML `SafeLoader` with the timestamp resolver removed and the bool
   resolver restricted to true/false).
2. **Select.** For `content_sha256`, remove the keys listed above. For
   `state_sha256`, remove nothing.
3. **Normalise.** Normalise every string (keys and values) to Unicode NFC.
   Two keys of one map that normalise to the same string are an error.
4. **Canonicalise.** Serialise with the JSON Canonicalization Scheme
   (RFC 8785, "JCS"): keys sorted by their UTF-16 code units, no
   insignificant whitespace, numbers in ECMAScript `Number.prototype.toString`
   form (`1500.0` -> `1500`, `12.50` -> `12.5`), strings escaped as JSON
   requires with non-ASCII characters written as UTF-8. Integers beyond
   ±2^53 and NaN/Infinity are errors.
5. **Hash.** `sha256` over the UTF-8 bytes, written as 64 lowercase hex
   characters.

Reference implementation: `src/grantthai/core/object_hash.py`
(`TOP_LEVEL_STATE_KEYS` must list `routing` for 0.3). Golden
vectors: `tests/golden/object-hash/` (input YAML, the exact canonical
content JSON for the small vector, and both expected hashes); an
implementation conforms when it reproduces every vector
(`tests/test_object_hash.py`).

## Staleness and the LOCK

- A review record is **current** when its `content_sha256` equals the
  project's current `content_sha256`, and **stale** otherwise. A stale
  record still exists and is rendered as stale, but no longer counts
  toward its gate. Only an authored change makes a record stale.
- When the object LOCK is applied, `lock.locked_content_sha256` records the
  `content_sha256` at that moment. If the current `content_sha256` differs,
  the lock is broken. Status changes (for example a field moving from
  `LOCKED` to `SUBMITTED`) do not break the lock.
- The output frontmatter carries `project_locked: true|false`, and both
  hashes, so a reader can tell which object was rendered.
