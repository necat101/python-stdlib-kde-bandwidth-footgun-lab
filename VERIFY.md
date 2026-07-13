# VERIFY.md – python-stdlib-kde-bandwidth-footgun-lab

## Repository

https://github.com/necat101/python-stdlib-kde-bandwidth-footgun-lab

## Verified implementation commit

`20747aa` – "run_lab: sanitize /home/ubuntu → /python-lab in python_executable"

This verification covers commit `20747aa`. A later documentation commit adds this `VERIFY.md` file; that later commit was **not** itself fresh-clone verified.

## Clean-clone verification

```
git clone https://github.com/necat101/python-stdlib-kde-bandwidth-footgun-lab.git kde_verify
cd kde_verify
git checkout 20747aa
```

Interpreter discovery (required order: `$PYTHON_BIN`, `python3.14`, `python3.13`, `python3`, `python`):

- Selected: `python3.14`
- Resolved executable (sanitized in artifacts): `/python-lab/.local/bin/python3.14`
- Real local interpreter: `/home/ubuntu/.local/bin/python3.14` (prefix sanitized per README)
- Python version: `3.14.6`
- Implementation: CPython
- Platform: Linux-6.17.0-1009-aws-x86_64-with-glibc2.39
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
- Empty-data errors: `statistics.kde([], h=…)` and `statistics.kde_random([], h=…)` raise expected StatisticsError, classified `expected_error`
- Single-point normal reference: max absolute error vs `math.exp`/`math.sqrt`/`math.pi` = 0.0 (within 1e-12)
- Symmetry: mirrored densities agree to 0.0 (within 1e-12)
- Nonnegative grid: all finite, all ≥ 0
- CDF monotonic: min_adjacent_diff ≥ -1e-14
- Compact-support tail: uniform kernel CDF tail low ≈ 0, high ≈ 1
- Kernel aliases: `normal`/`gauss`, `rectangular`/`uniform`, `parabolic`/`epanechnikov`, `quartic`/`biweight` – max_diff = 0.0
- Seeded repeatability: sequences match, SHA-256 digests match
- Tiny density classifier: left/right scores recorded, no accuracy claimed

JSON, CSV, and RESULTS.md counts agree (100 rows).

Artifact scan passed: no committed credentials, home-directory paths (sanitized), tokens, session metadata, or unrelated logs.

## Verification wall-clock time

Clone + checkout + compile + lab run + unittest: **~1.6 seconds** (full wall-clock including git clone: **~1.57 s**).

## Skips / failures

- Version skips: 0 (Python 3.14 has `statistics.kde` / `statistics.kde_random`)
- Failures: 0
- Unittest: 16/16 pass

## Notes

- Interpreter path in committed artifacts: `/python-lab/.local/bin/python3.14` (sanitized from `/home/ubuntu/.local/bin/python3.14`, documented in README)
- HN thread evidence captured before README sentiment summary: HN #46120611, via `python3 ./hackernews get-item --id 46120611`
- No NumPy, SciPy, pandas, scikit-learn, plots, datasets, or network calls
- Lab runtime: ~0.00s, unittest: ~0.04s
