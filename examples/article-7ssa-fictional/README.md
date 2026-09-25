# examples/article-7ssa-fictional/ — FICTIONAL

A fully FICTIONAL conceptual article for the academic-article route with a
7SSA structure profile. Every name, source and venue in `work.yaml` is
synthetic; no real journal, publisher, index, person, place or institution
is named.

```
grantthai build examples/article-7ssa-fictional                                     # 7ssa-world (the researcher's selection in routing)
grantthai build examples/article-7ssa-fictional --structure-profile 7ssa-thai-4      # the same sectors in four Thai sections
grantthai build examples/article-7ssa-fictional --format tex                         # build/ACADEMIC_ARTICLE.tex instead
```

Each command writes exactly one file. The body items of
`ARTICLE.BODY.SECTIONS` carry `ssa_sector` and `ssa_slot`; the 7SSA records
(`ARTICLE.SSA.*`) hold the gap, the contribution and the before/after
statement. Every sector has content, so the build has BLOCK 0 and no 7SSA
finding; the negative fixtures `tests/fixtures/negative/7SSA-NN/` are
mutated copies of this file. Acceptance tests AT-7SSA-1..3:
`tests/test_7ssa.py`.
