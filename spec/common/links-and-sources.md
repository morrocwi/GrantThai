# Links, the project chain graph, and resolvable sources

Draft, contract for v0.1. It defines three things a validator needs and
that the schemas alone cannot say:

1. **nodes**: what in `project.yaml` can be referred to;
2. **links**: how one node refers to another, and how the project's
   chain graph `project:chain_edges` is derived from those references;
3. **sources**: what a "resolvable source reference" is.

Machine-readable half: `spec/registry/structured_fields.schema.json`
(item schemas, `x-grantthai-node`, `x-grantthai-ref`),
`spec/common/field_record.schema.json` (`links`, `source_ids`),
`spec/common/source.schema.json` and `spec/common/chain.yaml`.
`tools/ci/check_schema_lint.py` checks the annotations and the shipped
examples; `src/grantthai/core/links.py` is the reference implementation
of this file (the v0.1 validator must give the same nodes and edges on
`examples/lecturer-no-ai/project.yaml`; `tests/test_example_project.py`).

## 1. Nodes

A **node** is one of the following:

| Node | Node id | Node type |
|---|---|---|
| A field record under `chain.<Node>` | its `field_id` | `<Node>` (a chain.yaml core/bridge node) |
| A field record under `fields` | its `field_id` | none (it is referable, but it is never part of the chain graph) |
| An **item**: an object inside an array whose item schema carries `x-grantthai-node` (at any depth inside a record's `value`) | the item's `id` | `x-grantthai-node.node_type` |

- Item ids have the form `<id_prefix><digits>` (for example `OBJ1`,
  `ACT3`, `BI12`, `MP1`); each structured field has its own prefix, and
  prefixes are unique across the whole contract (lint-checked).
- **Every node id is unique in the whole `project.yaml`.** Item ids never
  contain a dot and field ids always do, so the two cannot collide. A
  repeated item id is a BLOCK finding (rule S007).
- An item's `node_type` equals its field's registry `chain_node` when that
  is set (for example every `WORK.PLAN.ACTIVITIES` item is an `Activity`).
  Items of fields whose `chain_node` is null get a non-chain type
  (`Person`, `Site`, `Attachment`, ...; the list is
  `x-grantthai-nonchain-node-types`) and never enter the chain graph.
- Each registry field appears as **at most one** record in `project.yaml`.
  For array types the registry `cardinality` bounds the number of items in
  that one record's `value` (`1..N` means at least one item).
- Chain content that has no registry field (PriorKnowledge, Evidence,
  Claim, Observation, Experience, ...) is written as one record per
  statement, with ids `CORE.<NODE>.<NAME>` (for example
  `CORE.PRIORKNOWLEDGE.PK1`, `CORE.CLAIM.C1`), under `chain.<Node>`.

## 2. Links

A **reference** is a node id written in a property whose name ends in
`_id` or `_ids` (other than `id` itself). References are written in two
places:

- inside an item or object value, as the keys declared in
  `structured_fields.schema.json` (for example an activity's
  `objective_ids`, a budget line's `activity_ids`);
- on a field record, in its `links` object
  (`structured_fields.schema.json#/$defs/record_links`, for example
  `links.gap_ids` on the `CORE.RESEARCH.RQ.PRIMARY` record).

Evidence records keep their existing `supports_claim_id`
(`spec/common/evidence.schema.json`); it is a built-in causal reference
`Evidence -> Claim` (direction `source_to_target`).

Every reference property carries an `x-grantthai-ref` annotation:

| Key | Meaning |
|---|---|
| `targets` | where the referenced node must live: a registry `field_id` (the record itself or any item inside its value) or `chain:<Node>` (any record under `chain.<Node>`) |
| `edge` | `causal`, `feedback` or `attribute` |
| `direction` | for causal and feedback edges: `target_to_source` (the referenced node is upstream, e.g. an activity's `objective_ids`: Objective -> Activity) or `source_to_target` (the referenced node is downstream, e.g. an activity's `output_ids`: Activity -> Output) |
| `source_types` | record-level `links` only: the chain nodes of the records on which this key is allowed |

### Resolution

A reference `r` written under key `k` on node `s` **resolves** when all of
these hold:

1. exactly one node in the project has id `r`;
2. that node satisfies one of `k`'s `targets` (it is the named record, an
   item inside the named record's value, or a record under the named
   `chain:<Node>`);
3. for a record-level `links` key, the record's chain node is in
   `source_types`.

A reference that does not resolve is a BLOCK finding (rule S006) and
creates no edge. An empty list is not a finding by itself; the rules that
need a link (below) report missing links.

### Deriving `project:chain_edges`

`project:chain_edges` is the set of directed edges `(from, to, kind)`
obtained from every **resolved** reference whose `edge` is `causal` or
`feedback`:

- `direction: source_to_target` gives `(s, r, kind)`;
- `direction: target_to_source` gives `(r, s, kind)`;
- `kind` is the annotation's `edge` value. The same edge written on both
  sides (for example `activity.output_ids` and `output.activity_ids`) is
  **one** edge: the graph is a set. A link may be written on either side.
- `attribute` references (for example `responsible_person_ids`) must
  resolve, but add no chain edge.

Edge kinds follow `spec/common/chain.yaml`:

- Every `causal` annotation is **type-consistent** with the chain: the
  upstream node's type reaches the downstream node's type through
  `edges.causal` (reflexively; an activity may depend on an activity).
  `check_schema_lint.py` verifies this for every annotation, so a project
  can only produce causal edges that run with the chain.
- Every `feedback` annotation matches a pair in `edges.feedback`
  (`Impact -> KR` via an impact's `kr_ids`; `KR -> Need` via the Need
  record's `links.kr_ids`).

**CH001** checks that the subgraph of `causal` edges is acyclic. Because
annotations are type-consistent, in practice a cycle can only come from
same-type references (for example `depends_on_activity_ids` looping).
`feedback` edges are exempt.

### What each v0.1 link rule reads

All "linked" wording in `validators/rules.yaml` means: there is an edge in
`project:chain_edges` between the named nodes.

| Rule | Passes when |
|---|---|
| R003 | the `CORE.RESEARCH.RQ.PRIMARY` record has an incoming causal edge from the `CORE.RESEARCH.GAP` record (written as `links.gap_ids` on the RQ record) |
| R004 | every `CORE.RESEARCH.OBJECTIVES` item has an incoming causal edge from an RQ record (`rq_ids`) |
| R005 | every objective item has an outgoing causal edge to `METHOD.PLAN.DESIGN` or one of its phase items `MPn` (`method_ids`) |
| R006 | every method phase item of `METHOD.PLAN.DESIGN` (or the `METHOD.PLAN.DESIGN` record itself when it has no phases) has an outgoing causal edge to a `METHOD.PLAN.DATA_COLLECTION` item (written as the data-collection item's `method_ids`) |
| R007 | the `METHOD.PLAN.ANALYSIS` record has an incoming causal edge from a data-collection item (`data_ids`) |
| W001 | every activity item has an incoming causal edge from an objective item, or from the design or a phase item |
| W002 | every activity item has at least one resolved `responsible_person_ids` entry (attribute reference, not an edge) |
| W004 | every `RESULTS.CHAIN.OUTPUTS` item has an incoming causal edge from an activity item |
| B001 | every `BUDGET.PLAN.ITEMS` item has an incoming causal edge from an activity item |
| CH001 | the causal subgraph is acyclic |
| CH002 | each `required_stages` node has at least one record under `chain.<Node>` whose value is not null |
| R001 | the `CORE.RESEARCH.PROBLEM` record has at least one resolvable `source_ids` entry |
| R002 | the Gap record has an incoming causal edge from at least one PriorKnowledge record, and each such record has at least one resolvable `source_ids` entry |

## 3. Sources

`project.yaml` has a top-level `sources` list
(`spec/common/source.schema.json`). A field record points at it with
`source_ids`.

A `source_ids` entry is **resolvable** when, **offline and without any
network access**:

1. it matches `^SRC-[A-Z0-9][A-Z0-9-]{0,62}$`;
2. exactly one entry in `sources` has that `source_id`;
3. that entry is schema-valid (so it has a non-empty `citation`, a `kind`
   and `contains_personal_data`);
4. if the entry has `file`, that path, taken relative to the directory
   containing `project.yaml`, exists; and if it also has `sha256`, the
   file's sha256 equals it.

`url` is never fetched and never checked; being reachable on the internet
is not part of "resolvable". A source that is resolvable is only
*present and findable*: it does not mean the source supports the value
(spec/common/status.yaml).

An unresolvable `source_ids` entry is a BLOCK finding (rule S008).

### Which records need a source

- A record whose `provenance.provenance_class` is `SOURCE` needs **at least
  one** resolvable `source_ids` entry to reach `STRUCTURE_CHECKED`.
- Records with class `DECISION`, `INFERENCE` or `DERIVED` (titles, budget
  numbers, objectives, the workplan, ...) may have no source at all and
  still reach `STRUCTURE_CHECKED`. If they list `source_ids`, every entry
  must resolve.
- R001 and R002 are REVIEW rules that ask for sources on the Problem and
  PriorKnowledge records whatever their class.

### Source manifest in the output

The appendix of `build/NRIIS_SUBMISSION.md` lists every `sources` entry in
`source_id` order with `kind`, `citation`, `locator`, `url`, `sha256` and
the field ids that cite it. For an entry with
`contains_personal_data: true` only `source_id`, `kind` and `[private]`
are printed.
