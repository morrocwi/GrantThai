# Project object hash (`project_object_sha256`, review `object_sha256`)

Draft. One definition, used everywhere a "sha256 of the project object"
appears: the output frontmatter `project_object_sha256`, review records'
`object_sha256`, `lock.locked_object_sha256`, and validation reports.

## Algorithm

1. Parse `project.yaml` with a YAML 1.2 safe loader into plain data (maps,
   lists, strings, numbers, booleans, null). Dates must be written as
   quoted strings (`"2026-09-25"`), so no YAML-specific types remain.
2. Remove the top-level keys `review_records` and `lock`. Reviews and the
   lock *refer to* the object, so they are not part of it.
3. Normalise every string (keys and values) to Unicode NFC.
4. Serialise with the JSON Canonicalization Scheme (RFC 8785, "JCS"):
   sorted keys, no insignificant whitespace, canonical number form, UTF-8.
5. `sha256` over those bytes, written as 64 lowercase hex characters.

## Locked and unlocked objects

- The hash is always of the **current** object, whether or not it is
  locked. The output frontmatter carries `project_locked: true|false` so a
  reader can tell which it is.
- When the object is locked, `lock.locked_object_sha256` records the hash at
  lock time. If the current hash differs, the lock is broken (any edit
  breaks the lock; see `spec/common/status_permissions.yaml`).
- A review record whose `object_sha256` differs from the current hash is
  **stale**: it still exists and is rendered as stale, but it no longer
  counts toward its gate.
