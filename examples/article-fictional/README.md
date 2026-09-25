# examples/article-fictional/ — FICTIONAL

A fully FICTIONAL work object for the academic-article route. Every name,
number, source and venue in `work.yaml` is synthetic; the target venue is an
invented name, and no real journal, publisher, index, place or institution
is named.

```
grantthai build examples/article-fictional        # routing.default_route: academic-article
```

writes exactly one file, `build/ACADEMIC_ARTICLE.md`: a manuscript overview
arranged from the researcher's own records. GrantThai composes no section
text and never says a manuscript is publishable; `manuscript_ready: true`
means only that no BLOCK finding is open.

Three REVIEW findings are seeded on purpose (ART002 keyword count, ART006 an
author with no contribution role, ART010 a venue requirement with no
source), so the readiness summary shows what a person should look at. The
article titles are left empty on purpose: the output copies the shared
`CORE.GENERAL.TITLE_*` values and says so. Acceptance test AT-R2:
`tests/test_article_route.py`.
