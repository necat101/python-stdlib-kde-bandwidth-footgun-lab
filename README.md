# python-stdlib-kde-bandwidth-footgun-lab

A tiny, stdlib-only correctness lab for Python 3.13+ `statistics.kde()` / `statistics.kde_random()`. Bandwidth sensitivity, kernel aliases, PDF/CDF evaluation, seeded sampling, and the gap between a density-score demo and a real ML model.

No NumPy, SciPy, pandas, scikit-learn, plots, datasets, or network calls. ~0 seconds runtime. 20 cases × 5 methods = 100 rows.

## What this tests

- `statistics.kde` / `statistics.kde_random` API availability
- Empty-data error handling
- Single-point normal-kernel reference vs `math.exp` / `math.sqrt` / `math.pi`
- Symmetric-data PDF symmetry
- Nonnegative grid check
- Finite-grid mass (trapezoidal, local observation only)
- CDF monotonicity
- Compact-kernel tail bounds (uniform)
- PDF/CDF finite-difference check (same implementation, local observation)
- Narrow vs wide bandwidth (local roughness, not optimal selection)
- Compact-support zero-outside check
- Kernel alias equivalence: `normal`/`gauss`, `rectangular`/`uniform`, `parabolic`/`epanechnikov`, `quartic`/`biweight`
- Duplicate samples peak
- Outlier reweighting (mixture-weight change)
- Seeded `kde_random()` repeatability
- Cross-version seed disclaimer (context_only)
- Tiny 1-D density-threshold "classifier" (scores only, no accuracy)
- No-global-ML-validity claim (context_only)

## Run

```sh
python3 run_lab.py
python3 -m unittest -v
```

## Results

See [RESULTS.md](RESULTS.md).

## Hacker News thread access

Thread: [Python Data Science Handbook – HN #46120611](https://news.ycombinator.com/item?id=46120611)

Evidence was captured via the bundled OpenClaw Hacker News CLI:

```
python3 ./hackernews get-item --id 46120611
```

Full comment tree fetched recursively via the Hacker News Firebase API. Evidence files (`hn_thread_evidence.md`, `hn_comments_sanitized.json`) were committed **before** the README sentiment summary was prepared.

### What the linked handbook teaches

The [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/) by Jake VanderPlas covers NumPy, pandas, Matplotlib, and scikit-learn, with introductory material on data manipulation, visualization, and machine learning. It is an approachable entry-level resource, not a comprehensive reference manual.

### What HN commenters praised or criticized

Commenters widely praised the book as an accessible introduction to data science and ML (ellisv, __rito__, trio8453, mayankkaizen). One commenter (pantsforbirds) specifically remembered the kernel density estimation material as useful in real work at their first job.

Several commenters said the linked edition was old / introductory rather than a true "handbook" (wiz21c, msto, maxnoe, synergy20), noting the original 2016 publication date. The existence of a second edition (2023, O'Reilly) came up repeatedly (synergy20, phone_book / mkl, mayankkaizen).

### pandas vs Polars debate

pandas vs Polars dominated the thread. Reasons for defending pandas: ecosystem maturity, deep library integration, familiar workflows, "it gets the job done" (dahcryn, this_user, refactor_master, mttpgn, jononor). Reasons for preferring Polars: better API consistency / composability, Expression system making programmatic queries easier, no multi-index footguns, speed, nested data / JSON support, simpler maintenance (crystal_revenge, rbartelme, minimaxir, jononor).

Disagreements covered: dataframe composability (Polars Expressions vs pandas method chaining), indexing (pandas multi-index criticized, Polars having no index at all), performance (Polars faster, but some argued speed isn't the point for DS), testing/readability (pid-1 called pandas "untestable, unreadable", mttpgn/physicsguy countered with data-integrity tests and Pandera), and the Polars `maintain_order=False` default footgun (jmpeax, jononor).

### R, Matlab, and ecosystem stability

R and Matlab workflows came up as alternative mental models (biofox, isolatedsystem, kelipso). R was described as stable for a decade but also carrying three OO systems and a major tidyverse transition (crystal_revenge). Matlab was noted as expensive outside academia, with Octave extending its syntax with NumPy/R-inspired improvements (fluidcruft). Some commenters valued stable familiar tools (pandas, R, Matlab loops) while others preferred newer APIs (Polars, declarative operations).

Declarative dataframe operations (`apply`, `join`, etc. – "what" not "how") were contrasted with ordinary explicit loops (isolatedsystem coming from Matlab, fifilura defending declarative style).

### Why praise for a teaching resource does not prove every technique is appropriate

The thread makes clear that praise for VanderPlas as a teacher, and for the handbook as an entry point, does not establish that pandas is the right tool for every project, that KDE is appropriate for every dataset, that any specific bandwidth is optimal, or that density estimation equals calibrated classification. Ecosystem opinions (pandas vs Polars vs R vs Matlab) do not establish the correctness or suitability of a statistical method.

### Scope of this repository

This repository tests **only** the Python 3.13+ standard-library `statistics.kde` / `statistics.kde_random` API. It does **not** recreate the handbook's third-party stack (NumPy, pandas, Matplotlib, scikit-learn). It does **not** validate KDE as an ML model. It is a narrow stdlib API footgun lab.

## Disclaimers

- KDE is not appropriate for every dataset.
- Bandwidth tested is not proven optimal.
- Kernel choice can matter.
- Finite-grid integration does not prove exact normalization.
- Seeded samples are locally repeatable, not cross-version bit-identical.
- Density estimate is not a calibrated class probability.
- Tiny density comparison is not a valid production classifier.
- stdlib KDE does not replace NumPy, SciPy, pandas, scikit-learn, or specialist statistics tooling.
- Praise for a data-science book does not validate every technique or library it discusses.

## Interpreter path sanitization

Committed result artifacts record the Python executable with a sanitized prefix (`/python-lab/...`). Any home-directory prefix present in the local environment was replaced with `/python-lab` before writing results, to avoid exposing local filesystem paths in committed artifacts.
