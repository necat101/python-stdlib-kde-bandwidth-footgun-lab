# VERIFY.md – python-stdlib-kde-bandwidth-footgun-lab

## Repository

https://github.com/necat101/python-stdlib-kde-bandwidth-footgun-lab

## Verified implementation commit

`107344e3c51a81ecebe17e9a83ce3ac69f46f5a0`

This verification covers commit `107344e3c51a81ecebe17e9a83ce3ac69f46f5a0`. A later documentation commit adding this `VERIFY.md` was **not** itself fresh-clone verified.

## Clean-clone verification

```
git clone https://github.com/necat101/python-stdlib-kde-bandwidth-footgun-lab.git kde_verify
cd kde_verify
git checkout 107344e3c51a81ecebe17e9a83ce3ac69f46f5a0
```

Interpreter discovery (required order: `$PYTHON_BIN`, `python3.14`, `python3.13`, `python3`, `python`):

- Selected: `python3.14`
- Resolved executable (sanitized in artifacts): `/python-lab/.local/bin/python3.14`
- Python version: `3.14.6`
- Implementation: CPython
- Platform: Linux
- `statistics.kde` available: True
- `statistics.kde_random` available: True

Validation commands:

```
python3.14 -m py_compile run_lab.py test_lab.py
# exit 0

python3.14 run_lab.py
# exit 0

python3.14 -m unittest -v
# exit 0, 16 tests
```

## Results

- Cases: 20
- Methods: 5 (`inspect_api`, `evaluate_pdf`, `evaluate_cdf`, `draw_seeded_samples`, `ml_context_observation`)
- Rows: 100
- Classifications:
  - pass: 14
  - local_observation: 6
  - expected_error: 3
  - context_only: 8
  - not_applicable: 69
  - version_skip: 0
  - fail: 0

Key checks:
- Empty-data errors: `statistics.kde([], h=…)` and `statistics.kde_random([], h=…)` raise StatisticsError (exact type enforced by runner and asserted by unittest), classified `expected_error`
- Single-point normal reference: max absolute error vs `math.exp`/`math.sqrt`/`math.pi` = 0.0 (within 1e-12)
- Symmetry: mirrored densities agree to 0.0 (within 1e-12)
- Nonnegative grid: all finite, all ≥ 0
- CDF monotonic: min_adjacent_diff ≥ -1e-14
- Compact-support tail: uniform kernel CDF tail low ≈ 0, high ≈ 1
- Kernel aliases: `normal`/`gauss`, `rectangular`/`uniform`, `parabolic`/`epanechnikov`, `quartic`/`biweight` – max_diff = 0.0
- Seeded repeatability: sequences match, SHA-256 digests match
- Tiny density classifier: all 3 query points (-2.0, 0.0, 2.0) recorded with left/right scores, label, and tie flag; unittest verifies query values, label correctness vs scores, tie flag consistency, and finite/nonnegative densities; no accuracy claimed

JSON, CSV, and RESULTS.md counts agree (100 rows).

Artifact scan passed: credential patterns (GitHub PAT, API keys, bearer tokens, password assignments, session IDs) checked in all files; filesystem path patterns checked in structured data files; no leaks detected.

## Verification wall-clock time

Clone + checkout + compile + lab run + unittest: ~1.6 seconds.

## Skips / failures

- Version skips: 0 (Python 3.14 has `statistics.kde` / `statistics.kde_random`)
- Failures: 0
- Unittest: 16/16 pass

## Notes

- Interpreter path in committed artifacts uses sanitized prefix `/python-lab/...` (see README)
- HN thread evidence captured before README sentiment summary: HN #46120611, via `python3 ./hackernews get-item --id 46120611`
- No NumPy, SciPy, pandas, scikit-learn, plots, datasets, or network calls
- Lab runtime: ~0.00s, unittest: ~0.04s
