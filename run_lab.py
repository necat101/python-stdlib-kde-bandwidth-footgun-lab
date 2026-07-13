#!/usr/bin/env python3
"""python-stdlib-kde-bandwidth-footgun-lab runner"""
import json, sys, time, math, hashlib, inspect, platform
from pathlib import Path

ROOT = Path(__file__).parent
CASES_PATH = ROOT / "cases.json"

with open(CASES_PATH) as f:
    cases_def = json.load(f)

case_expect = {c["id"]: c["method_expectations"] for c in cases_def}
METHODS = ["inspect_api", "evaluate_pdf", "evaluate_cdf", "draw_seeded_samples", "ml_context_observation"]

# env info
py_exe = sys.executable
# sanitize home-directory prefix in committed artifacts
if py_exe.startswith("/home/ubuntu"):
    py_exe = py_exe.replace("/home/ubuntu", "/python-lab", 1)
py_version = sys.version
py_impl = platform.python_implementation()
plat = platform.platform()

try:
    import statistics as stats_mod
    kde_available = hasattr(stats_mod, "kde")
    kde_random_available = hasattr(stats_mod, "kde_random")
    if kde_available:
        try:
            kde_sig = str(inspect.signature(stats_mod.kde))
        except Exception:
            kde_sig = "?"
    else:
        kde_sig = None
    if kde_random_available:
        try:
            kde_random_sig = str(inspect.signature(stats_mod.kde_random))
        except Exception:
            kde_random_sig = "?"
    else:
        kde_random_sig = None
except Exception:
    stats_mod = None
    kde_available = False
    kde_random_available = False
    kde_sig = None
    kde_random_sig = None

def data_hash(data):
    if data is None:
        return None
    s = json.dumps(data, separators=(",",":"))
    return hashlib.sha256(s.encode()).hexdigest()[:16]

def make_row(method, case_id, expected_classification, **fields):
    row = {
        "method": method,
        "case_id": case_id,
        "python_executable": py_exe,
        "python_version": py_version,
        "implementation": py_impl,
        "platform": plat,
        "statistics_kde_available": kde_available,
        "statistics_kde_random_available": kde_random_available,
        "expected_classification": expected_classification,
        "actual_classification": None,
        "api_exercised": None,
        "kernel": None,
        "bandwidth": None,
        "cumulative_flag": None,
        "input_count": None,
        "input_data_hash": None,
        "evaluation_point": None,
        "grid_summary": None,
        "density_value": None,
        "cdf_value": None,
        "reference_value": None,
        "absolute_error": None,
        "relative_error": None,
        "estimated_grid_mass": None,
        "monotonicity_result": None,
        "alias_pair_result": None,
        "seed": None,
        "sample_count": None,
        "seeded_sequence_digest": None,
        "repeated_sequence_match": None,
        "left_density_score": None,
        "right_density_score": None,
        "local_density_label": None,
        "density_query_results": None,
        "exception_type": None,
        "exception_message": None,
        "elapsed_time": None,
        "skip_reason": None,
        "failure_reason": None,
        "narrow_local_conclusion": None,
    }
    row.update(fields)
    return row

rows = []

def run_method(method, case_id, fn):
    expected = case_expect[case_id][method]["expected_classification"]
    start = time.perf_counter()
    try:
        result = fn()
        elapsed = time.perf_counter() - start
        if not isinstance(result, dict):
            result = {}
        row = make_row(method, case_id, expected, **result)
        if row["actual_classification"] is None:
            row["actual_classification"] = "fail"
            row["failure_reason"] = "missing actual_classification from case handler"
        row["elapsed_time"] = elapsed
        rows.append(row)
    except Exception as e:
        elapsed = time.perf_counter() - start
        row = make_row(method, case_id, expected,
            actual_classification="fail",
            exception_type=type(e).__name__,
            exception_message=str(e)[:200],
            failure_reason=f"unhandled: {e}",
            elapsed_time=elapsed)
        rows.append(row)

# ---- helpers ----
def trapezoidal(xs, ys):
    if len(xs) < 2: return 0.0
    s = 0.0
    for i in range(len(xs)-1):
        dx = xs[i+1]-xs[i]
        s += 0.5 * (ys[i]+ys[i+1]) * dx
    return s

def normal_pdf(x, mu=0.0, sigma=1.0):
    return math.exp(-0.5*((x-mu)/sigma)**2) / (sigma*math.sqrt(2*math.pi))

# ---- case implementations ----
def case_python_version_marker(method):
    if method == "inspect_api":
        return {"actual_classification": "pass", "api_exercised": "sys.version/platform"}
    if method == "ml_context_observation":
        return {"actual_classification": "pass", "narrow_local_conclusion": "version recorded, no ML claim"}
    return {"actual_classification": "not_applicable"}

def case_statistics_kde_api_marker(method):
    if method == "inspect_api":
        if not kde_available:
            return {"actual_classification": "version_skip", "skip_reason": "statistics.kde missing", "api_exercised": "statistics.kde"}
        return {"actual_classification": "pass", "api_exercised": f"statistics.kde {kde_sig}"}
    return {"actual_classification": "not_applicable"}

def case_statistics_kde_random_api_marker(method):
    if method == "inspect_api":
        if not kde_random_available:
            return {"actual_classification": "version_skip", "skip_reason": "statistics.kde_random missing", "api_exercised": "statistics.kde_random"}
        return {"actual_classification": "pass", "api_exercised": f"statistics.kde_random {kde_random_sig}"}
    if method == "ml_context_observation":
        return {"actual_classification": "context_only", "narrow_local_conclusion": "kde_random is sampling, not ML training"}
    return {"actual_classification": "not_applicable"}

def case_empty_data_errors_marker(method):
    if method not in ("evaluate_pdf", "evaluate_cdf", "draw_seeded_samples"):
        return {"actual_classification": "not_applicable"}
    if not kde_available:
        return {"actual_classification": "version_skip", "skip_reason": "statistics.kde missing"}
    data = []
    try:
        if method == "evaluate_pdf":
            f = stats_mod.kde(data, h=1.0)
            _ = f(0.0)
        elif method == "evaluate_cdf":
            f = stats_mod.kde(data, h=1.0, cumulative=True)
            _ = f(0.0)
        elif method == "draw_seeded_samples":
            if not kde_random_available:
                return {"actual_classification": "version_skip", "skip_reason": "kde_random missing"}
            f = stats_mod.kde_random(data, h=1.0, seed=42)
            _ = f()
        return {"actual_classification": "fail", "failure_reason": "empty data did not raise", "input_count": 0, "input_data_hash": data_hash(data)}
    except stats_mod.StatisticsError as e:
        et = type(e).__name__
        return {"actual_classification": "expected_error", "exception_type": et, "exception_message": str(e)[:200], "input_count": 0, "input_data_hash": data_hash(data), "api_exercised": "statistics.kde" if method != "draw_seeded_samples" else "statistics.kde_random"}
    except Exception as e:
        et = type(e).__name__
        return {"actual_classification": "fail", "exception_type": et, "exception_message": str(e)[:200], "input_count": 0, "input_data_hash": data_hash(data), "failure_reason": f"wrong exception type for empty data: {et}, expected StatisticsError"}

def case_single_point_normal_reference_marker(method):
    if method != "evaluate_pdf":
        return {"actual_classification": "not_applicable"}
    if not kde_available:
        return {"actual_classification": "version_skip", "skip_reason": "statistics.kde missing"}
    data = [0.0]
    h = 1.0
    f = stats_mod.kde(data, h=h, kernel="normal")
    points = [-1.0, 0.0, 1.0]
    vals = [f(x) for x in points]
    refs = [normal_pdf(x, 0.0, h) for x in points]
    errs = [abs(a-b) for a,b in zip(vals, refs)]
    max_err = max(errs)
    tol = 1e-12
    passed = max_err <= tol
    return {
        "actual_classification": "pass" if passed else "fail",
        "api_exercised": "statistics.kde",
        "kernel": "normal",
        "bandwidth": h,
        "input_count": len(data),
        "input_data_hash": data_hash(data),
        "evaluation_point": f"points={points}",
        "density_value": vals[1],
        "reference_value": refs[1],
        "absolute_error": max_err,
        "failure_reason": None if passed else f"max_err {max_err} > {tol}",
        "narrow_local_conclusion": "single normal kernel matches math.exp reference",
    }

def case_symmetric_data_pdf_symmetry_marker(method):
    if method != "evaluate_pdf":
        return {"actual_classification": "not_applicable"}
    if not kde_available:
        return {"actual_classification": "version_skip", "skip_reason": "statistics.kde missing"}
    data = [-2.0, -1.0, 0.0, 1.0, 2.0]
    f = stats_mod.kde(data, h=0.5, kernel="normal")
    pairs = [(-1.5, 1.5), (-0.5, 0.5)]
    diffs = []
    for a,b in pairs:
        diffs.append(abs(f(a)-f(b)))
    max_diff = max(diffs)
    tol = 1e-12
    passed = max_diff <= tol
    return {
        "actual_classification": "pass" if passed else "fail",
        "api_exercised": "statistics.kde",
        "kernel": "normal",
        "bandwidth": 0.5,
        "input_count": len(data),
        "input_data_hash": data_hash(data),
        "absolute_error": max_diff,
        "narrow_local_conclusion": "mirrored densities agree for symmetric data",
        "failure_reason": None if passed else f"max_diff {max_diff} > {tol}",
    }

def case_pdf_nonnegative_grid_marker(method):
    if method != "evaluate_pdf":
        return {"actual_classification": "not_applicable"}
    if not kde_available:
        return {"actual_classification": "version_skip", "skip_reason": "statistics.kde missing"}
    data = [-2.0, -1.0, 0.0, 1.0, 2.0]
    f = stats_mod.kde(data, h=0.8, kernel="normal")
    grid = [x/2.0 for x in range(-12, 13)]
    vals = [f(x) for x in grid]
    vmin = min(vals); vmax = max(vals)
    all_finite = all(math.isfinite(v) for v in vals)
    all_nonneg = all(v >= -1e-15 for v in vals)
    passed = all_finite and all_nonneg
    return {
        "actual_classification": "pass" if passed else "fail",
        "api_exercised": "statistics.kde",
        "kernel": "normal",
        "bandwidth": 0.8,
        "input_count": len(data),
        "input_data_hash": data_hash(data),
        "grid_summary": f"start=-6.0 stop=6.0 n={len(grid)}",
        "density_value": vmax,
        "narrow_local_conclusion": f"grid min={vmin:.6g} max={vmax:.6g}, all finite nonnegative",
        "failure_reason": None if passed else "negative or nonfinite value",
    }

def case_pdf_grid_mass_local_observation_marker(method):
    if method != "evaluate_pdf":
        return {"actual_classification": "not_applicable"}
    if not kde_available:
        return {"actual_classification": "version_skip", "skip_reason": "statistics.kde missing"}
    data = [-2.0, -1.0, 0.0, 1.0, 2.0]
    f = stats_mod.kde(data, h=0.6, kernel="normal")
    start, stop, step = -8.0, 8.0, 0.05
    n = int((stop-start)/step)+1
    xs = [start + i*step for i in range(n)]
    ys = [f(x) for x in xs]
    mass = trapezoidal(xs, ys)
    dist = abs(mass - 1.0)
    return {
        "actual_classification": "local_observation",
        "api_exercised": "statistics.kde",
        "kernel": "normal",
        "bandwidth": 0.6,
        "input_count": len(data),
        "input_data_hash": data_hash(data),
        "grid_summary": f"start={start} stop={stop} step={step} n={n}",
        "estimated_grid_mass": mass,
        "narrow_local_conclusion": f"finite-grid mass ≈ {mass:.6f}, distance from 1.0 = {dist:.6f}",
    }

def case_cdf_monotonic_marker(method):
    if method != "evaluate_cdf":
        return {"actual_classification": "not_applicable"}
    if not kde_available:
        return {"actual_classification": "version_skip", "skip_reason": "statistics.kde missing"}
    data = [-2.0, -1.0, 0.0, 1.0, 2.0]
    f = stats_mod.kde(data, h=0.5, kernel="normal", cumulative=True)
    xs = [x/2.0 for x in range(-12, 13)]
    ys = [f(x) for x in xs]
    diffs = [ys[i+1]-ys[i] for i in range(len(ys)-1)]
    min_diff = min(diffs) if diffs else 0.0
    passed = min_diff >= -1e-14
    return {
        "actual_classification": "pass" if passed else "fail",
        "api_exercised": "statistics.kde",
        "kernel": "normal",
        "bandwidth": 0.5,
        "cumulative_flag": True,
        "input_count": len(data),
        "input_data_hash": data_hash(data),
        "monotonicity_result": f"min_adjacent_diff={min_diff:.3g}",
        "narrow_local_conclusion": "CDF values non-decreasing on grid",
        "failure_reason": None if passed else f"decreasing step {min_diff}",
    }

def case_compact_kernel_tail_bounds_marker(method):
    if method != "evaluate_cdf":
        return {"actual_classification": "not_applicable"}
    if not kde_available:
        return {"actual_classification": "version_skip", "skip_reason": "statistics.kde missing"}
    data = [-1.0, 0.0, 1.0]
    h = 0.5
    f = stats_mod.kde(data, h=h, kernel="uniform", cumulative=True)
    low = min(data) - h - 2.0
    high = max(data) + h + 2.0
    vlo = f(low); vhi = f(high)
    # uniform kernel compact support: tails should be ~0 and ~1
    tol = 1e-12
    passed = abs(vlo - 0.0) <= tol and abs(vhi - 1.0) <= tol
    return {
        "actual_classification": "pass" if passed else "fail",
        "api_exercised": "statistics.kde",
        "kernel": "uniform",
        "bandwidth": h,
        "cumulative_flag": True,
        "input_count": len(data),
        "input_data_hash": data_hash(data),
        "cdf_value": vhi,
        "narrow_local_conclusion": f"tail low={vlo:.3g} high={vhi:.3g}",
        "failure_reason": None if passed else f"tail out of bounds low={vlo} high={vhi}",
    }

def case_pdf_cdf_finite_difference_marker(method):
    if not kde_available:
        return {"actual_classification": "version_skip", "skip_reason": "statistics.kde missing", "api_exercised": "statistics.kde"}
    data = [-2.0, -1.0, 0.0, 1.0, 2.0]
    h = 0.6
    x0 = 0.5
    eps = 1e-4
    if method == "evaluate_pdf":
        f_pdf = stats_mod.kde(data, h=h, kernel="normal", cumulative=False)
        pdf_val = f_pdf(x0)
        return {
            "actual_classification": "local_observation",
            "api_exercised": "statistics.kde",
            "kernel": "normal",
            "bandwidth": h,
            "input_count": len(data),
            "input_data_hash": data_hash(data),
            "evaluation_point": str(x0),
            "density_value": pdf_val,
            "narrow_local_conclusion": "pdf at interior point recorded",
        }
    elif method == "evaluate_cdf":
        f_cdf = stats_mod.kde(data, h=h, kernel="normal", cumulative=True)
        f_pdf = stats_mod.kde(data, h=h, kernel="normal", cumulative=False)
        cdf_plus = f_cdf(x0 + eps)
        cdf_minus = f_cdf(x0 - eps)
        fd = (cdf_plus - cdf_minus) / (2*eps)
        pdf_val = f_pdf(x0)
        abs_err = abs(pdf_val - fd)
        rel_err = abs_err / abs(pdf_val) if pdf_val != 0 else None
        return {
            "actual_classification": "local_observation",
            "api_exercised": "statistics.kde",
            "kernel": "normal",
            "bandwidth": h,
            "cumulative_flag": True,
            "input_count": len(data),
            "input_data_hash": data_hash(data),
            "evaluation_point": str(x0),
            "cdf_value": f_cdf(x0),
            "density_value": pdf_val,
            "absolute_error": abs_err,
            "relative_error": rel_err,
            "narrow_local_conclusion": f"pdf={pdf_val:.6g} fd={fd:.6g} abs_err={abs_err:.3g}",
        }
    return {"actual_classification": "not_applicable"}

def case_narrow_vs_wide_bandwidth_marker(method):
    if method != "evaluate_pdf":
        return {"actual_classification": "not_applicable"}
    if not kde_available:
        return {"actual_classification": "version_skip", "skip_reason": "statistics.kde missing"}
    data = [-2.0, -1.0, 0.0, 1.0, 2.0]
    h_narrow = 0.2
    h_wide = 1.5
    f_n = stats_mod.kde(data, h=h_narrow, kernel="normal")
    f_w = stats_mod.kde(data, h=h_wide, kernel="normal")
    xs = [x/4.0 for x in range(-16, 17)]
    yn = [f_n(x) for x in xs]
    yw = [f_w(x) for x in xs]
    rough_n = sum(abs(yn[i+1]-yn[i]) for i in range(len(yn)-1))
    rough_w = sum(abs(yw[i+1]-yw[i]) for i in range(len(yw)-1))
    return {
        "actual_classification": "local_observation",
        "api_exercised": "statistics.kde",
        "kernel": "normal",
        "bandwidth": h_narrow,
        "input_count": len(data),
        "input_data_hash": data_hash(data),
        "grid_summary": f"n={len(xs)} narrow_rough={rough_n:.4g} wide_rough={rough_w:.4g}",
        "narrow_local_conclusion": "narrow bandwidth preserves more local variation for this sample; not a universal rule",
    }

def case_compact_support_zero_outside_marker(method):
    if method != "evaluate_pdf":
        return {"actual_classification": "not_applicable"}
    if not kde_available:
        return {"actual_classification": "version_skip", "skip_reason": "statistics.kde missing"}
    data = [0.0]
    h = 0.5
    f = stats_mod.kde(data, h=h, kernel="uniform")
    outside = [2.0, -2.0]
    inside = 0.0
    vals_out = [f(x) for x in outside]
    val_in = f(inside)
    passed = all(abs(v) < 1e-15 for v in vals_out) and val_in > 0
    return {
        "actual_classification": "pass" if passed else "fail",
        "api_exercised": "statistics.kde",
        "kernel": "uniform",
        "bandwidth": h,
        "input_count": 1,
        "input_data_hash": data_hash(data),
        "density_value": val_in,
        "narrow_local_conclusion": f"outside={vals_out} inside={val_in:.3g}",
        "failure_reason": None if passed else "compact support check failed",
    }

def case_kernel_alias_equivalence_marker(method):
    if method == "inspect_api":
        if not kde_available:
            return {"actual_classification": "version_skip", "skip_reason": "statistics.kde missing"}
        return {"actual_classification": "pass", "api_exercised": "statistics.kde kernel aliases"}
    if method != "evaluate_pdf":
        return {"actual_classification": "not_applicable"}
    if not kde_available:
        return {"actual_classification": "version_skip", "skip_reason": "statistics.kde missing"}
    data = [-1.0, 0.0, 1.0]
    h = 0.5
    pairs = [("normal","gauss"), ("rectangular","uniform"), ("parabolic","epanechnikov"), ("quartic","biweight")]
    grid = [x/4.0 for x in range(-8, 9)]
    max_diffs = {}
    missing = []
    for a,b in pairs:
        try:
            fa = stats_mod.kde(data, h=h, kernel=a)
            fb = stats_mod.kde(data, h=h, kernel=b)
            diffs = [abs(fa(x)-fb(x)) for x in grid]
            max_diffs[f"{a}/{b}"] = max(diffs)
        except Exception as e:
            missing.append(f"{a}/{b}:{type(e).__name__}")
    if missing:
        return {"actual_classification": "fail", "failure_reason": "missing alias: " + ", ".join(missing), "alias_pair_result": json.dumps(max_diffs)}
    max_overall = max(max_diffs.values()) if max_diffs else 0.0
    passed = max_overall <= 1e-14
    return {
        "actual_classification": "pass" if passed else "fail",
        "api_exercised": "statistics.kde",
        "input_count": len(data),
        "input_data_hash": data_hash(data),
        "alias_pair_result": json.dumps(max_diffs),
        "absolute_error": max_overall,
        "narrow_local_conclusion": f"alias max_diff={max_overall:.3g}",
        "failure_reason": None if passed else f"alias_diff {max_overall}",
    }

def case_duplicate_samples_peak_marker(method):
    if method != "evaluate_pdf":
        return {"actual_classification": "not_applicable"}
    if not kde_available:
        return {"actual_classification": "version_skip", "skip_reason": "statistics.kde missing"}
    data = [0.0, 0.0, 0.0]
    f = stats_mod.kde(data, h=0.5, kernel="normal")
    v_center = f(0.0)
    v_far = f(2.0)
    passed = v_center > v_far
    return {
        "actual_classification": "pass" if passed else "fail",
        "api_exercised": "statistics.kde",
        "kernel": "normal",
        "bandwidth": 0.5,
        "input_count": len(data),
        "input_data_hash": data_hash(data),
        "density_value": v_center,
        "narrow_local_conclusion": f"center={v_center:.4g} far={v_far:.4g}, duplicated input is not independent evidence",
        "failure_reason": None if passed else "peak not at duplicate location",
    }

def case_outlier_reweighting_local_observation_marker(method):
    if method != "evaluate_pdf":
        return {"actual_classification": "not_applicable"}
    if not kde_available:
        return {"actual_classification": "version_skip", "skip_reason": "statistics.kde missing"}
    base = [-1.0, 0.0, 1.0]
    with_outlier = [-1.0, 0.0, 1.0, 20.0]
    h = 0.6
    fb = stats_mod.kde(base, h=h, kernel="normal")
    fo = stats_mod.kde(with_outlier, h=h, kernel="normal")
    pts = [0.0, 20.0]
    vals_b = [fb(x) for x in pts]
    vals_o = [fo(x) for x in pts]
    return {
        "actual_classification": "local_observation",
        "api_exercised": "statistics.kde",
        "kernel": "normal",
        "bandwidth": h,
        "input_count": len(with_outlier),
        "input_data_hash": data_hash(with_outlier),
        "narrow_local_conclusion": f"base@[0,20]={vals_b} outlier@[0,20]={vals_o}; outlier changes all mixture weights",
    }

def case_seeded_kde_random_repeatability_marker(method):
    if method != "draw_seeded_samples":
        return {"actual_classification": "not_applicable"}
    if not kde_random_available:
        return {"actual_classification": "version_skip", "skip_reason": "kde_random missing"}
    data = [-2.0, -1.0, 0.0, 1.0, 2.0]
    h = 0.5
    seed = 42
    f1 = stats_mod.kde_random(data, h=h, kernel="normal", seed=seed)
    f2 = stats_mod.kde_random(data, h=h, kernel="normal", seed=seed)
    n = 10
    s1 = [f1() for _ in range(n)]
    s2 = [f2() for _ in range(n)]
    match = s1 == s2
    d1 = hashlib.sha256(json.dumps(s1).encode()).hexdigest()
    d2 = hashlib.sha256(json.dumps(s2).encode()).hexdigest()
    return {
        "actual_classification": "pass" if match and d1==d2 else "fail",
        "api_exercised": "statistics.kde_random",
        "kernel": "normal",
        "bandwidth": h,
        "input_count": len(data),
        "input_data_hash": data_hash(data),
        "seed": seed,
        "sample_count": n,
        "seeded_sequence_digest": d1,
        "repeated_sequence_match": bool(match),
        "narrow_local_conclusion": "seeded sequences match locally",
        "failure_reason": None if match else "sequences differ",
    }

def case_seeded_sequence_cross_version_disclaimer_marker(method):
    if method == "draw_seeded_samples" or method == "ml_context_observation":
        return {"actual_classification": "context_only", "narrow_local_conclusion": "seed gives local repeatability, not cross-version bit identity"}
    return {"actual_classification": "not_applicable"}

def case_tiny_density_threshold_classifier_marker(method):
    if method != "ml_context_observation":
        return {"actual_classification": "not_applicable"}
    if not kde_available:
        return {"actual_classification": "version_skip", "skip_reason": "statistics.kde missing"}
    left_class = [-2.2, -2.0, -1.8]
    right_class = [1.8, 2.0, 2.2]
    h = 0.3
    fl = stats_mod.kde(left_class, h=h, kernel="normal")
    fr = stats_mod.kde(right_class, h=h, kernel="normal")
    queries = [-2.0, 0.0, 2.0]
    results = []
    for q in queries:
        dl = fl(q); dr = fr(q)
        equal_within_tol = abs(dl - dr) <= 1e-15
        label = "left" if dl > dr and not equal_within_tol else "right" if dr > dl and not equal_within_tol else "tie"
        results.append({"query": q, "left_density": dl, "right_density": dr, "label": label, "equal_within_tolerance": equal_within_tol})
    # record first query in legacy scalar fields for backwards compat
    q0 = results[0]
    return {
        "actual_classification": "local_observation",
        "api_exercised": "statistics.kde",
        "kernel": "normal",
        "bandwidth": h,
        "left_density_score": q0["left_density"],
        "right_density_score": q0["right_density"],
        "local_density_label": q0["label"],
        "density_query_results": json.dumps(results),
        "narrow_local_conclusion": "density comparison is not a validated classifier; no accuracy computed; 1-D toy only; 3 queries recorded",
    }

def case_no_global_ml_validity_claim_marker(method):
    return {"actual_classification": "context_only", "narrow_local_conclusion": "no global ML validity claim"}

CASE_FNS = {
    "python_version_marker": case_python_version_marker,
    "statistics_kde_api_marker": case_statistics_kde_api_marker,
    "statistics_kde_random_api_marker": case_statistics_kde_random_api_marker,
    "empty_data_errors_marker": case_empty_data_errors_marker,
    "single_point_normal_reference_marker": case_single_point_normal_reference_marker,
    "symmetric_data_pdf_symmetry_marker": case_symmetric_data_pdf_symmetry_marker,
    "pdf_nonnegative_grid_marker": case_pdf_nonnegative_grid_marker,
    "pdf_grid_mass_local_observation_marker": case_pdf_grid_mass_local_observation_marker,
    "cdf_monotonic_marker": case_cdf_monotonic_marker,
    "compact_kernel_tail_bounds_marker": case_compact_kernel_tail_bounds_marker,
    "pdf_cdf_finite_difference_marker": case_pdf_cdf_finite_difference_marker,
    "narrow_vs_wide_bandwidth_marker": case_narrow_vs_wide_bandwidth_marker,
    "compact_support_zero_outside_marker": case_compact_support_zero_outside_marker,
    "kernel_alias_equivalence_marker": case_kernel_alias_equivalence_marker,
    "duplicate_samples_peak_marker": case_duplicate_samples_peak_marker,
    "outlier_reweighting_local_observation_marker": case_outlier_reweighting_local_observation_marker,
    "seeded_kde_random_repeatability_marker": case_seeded_kde_random_repeatability_marker,
    "seeded_sequence_cross_version_disclaimer_marker": case_seeded_sequence_cross_version_disclaimer_marker,
    "tiny_density_threshold_classifier_marker": case_tiny_density_threshold_classifier_marker,
    "no_global_ml_validity_claim_marker": case_no_global_ml_validity_claim_marker,
}

total_start = time.perf_counter()
for case_id, fn in CASE_FNS.items():
    for method in METHODS:
        run_method(method, case_id, lambda m=method, f=fn: f(m))
total_elapsed = time.perf_counter() - total_start

# write results
with open(ROOT / "results_rows.json", "w") as f:
    json.dump(rows, f, indent=2)

# csv
import csv
if rows:
    keys = list(rows[0].keys())
    with open(ROOT / "results_rows.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)

# RESULTS.md
from collections import Counter
cnt = Counter(r["actual_classification"] for r in rows)
def cget(k): return cnt.get(k, 0)

with open(ROOT / "RESULTS.md", "w") as f:
    f.write("# Results – python-stdlib-kde-bandwidth-footgun-lab\n\n")
    f.write(f"Python: {py_version.split()[0]}  \n")
    f.write(f"Implementation: {py_impl}  \n")
    f.write(f"Platform: {plat}  \n")
    f.write(f"statistics.kde available: {kde_available}  \n")
    f.write(f"statistics.kde_random available: {kde_random_available}  \n\n")
    f.write(f"Cases: 20  \nMethods: 5  \nRows: {len(rows)}  \n\n")
    f.write("Classifications:\n")
    for k in ["pass","expected_error","local_observation","context_only","not_applicable","version_skip","fail"]:
        f.write(f"- {k}: {cget(k)}\n")
    f.write(f"\nTotal runtime: {total_elapsed:.3f}s\n\n")
    # brief per-case notes
    f.write("## Observations\n\n")
    for r in rows:
        if r["actual_classification"] in ("pass","local_observation","expected_error","context_only") and r["narrow_local_conclusion"]:
            f.write(f"- {r['case_id']} / {r['method']}: {r['narrow_local_conclusion']}\n")
    f.write("\n## Disclaimers\n\n")
    f.write("- KDE is not appropriate for every dataset.\n")
    f.write("- Bandwidth tested is not proven optimal.\n")
    f.write("- Kernel choice can matter.\n")
    f.write("- Finite-grid integration does not prove exact normalization.\n")
    f.write("- Seeded samples are locally repeatable, not cross-version bit-identical.\n")
    f.write("- Density estimate is not a calibrated class probability.\n")
    f.write("- Tiny density comparison is not a valid production classifier.\n")
    f.write("- stdlib KDE does not replace NumPy, SciPy, pandas, scikit-learn, or specialist statistics tooling.\n")
    f.write("- Praise for a data-science book does not validate every technique or library it discusses.\n")

print(f"rows={len(rows)} elapsed={total_elapsed:.2f}s pass={cget('pass')} local={cget('local_observation')} expected_error={cget('expected_error')} context={cget('context_only')} na={cget('not_applicable')} skip={cget('version_skip')} fail={cget('fail')}")
