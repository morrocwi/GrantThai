# examples/both-routes-fictional/ — FICTIONAL

One FICTIONAL work object built through two routes. It is the
`lecturer-no-ai` example migrated to `work.yaml` 0.3, plus the `ARTICLE.*`
fields of the academic-article route. Every name, number and source is
synthetic; no real journal is named.

```
grantthai build examples/both-routes-fictional                            # -> build/NRIIS_SUBMISSION.md
grantthai build examples/both-routes-fictional --route academic-article   # -> build/ACADEMIC_ARTICLE.md
```

The researcher chose both routes (`routing.declared_routes`); the tool never
picks one. Each build writes exactly one file and leaves the other route's
file byte-identical, and the shared-core fields (titles, keywords, team,
problem, method, references) are authored once and print identically in
both files. Acceptance test AT-R3: `tests/test_article_route.py`.
