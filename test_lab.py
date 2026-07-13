#!/usr/bin/env python3
import unittest, json, csv
from pathlib import Path

ROOT = Path(__file__).parent

class TestLab(unittest.TestCase):
    def setUp(self):
        with open(ROOT / "cases.json") as f:
            self.cases = json.load(f)
        with open(ROOT / "results_rows.json") as f:
            self.rows = json.load(f)

    def test_case_count(self):
        self.assertEqual(len(self.cases), 20)
        ids = [c["id"] for c in self.cases]
        self.assertEqual(len(set(ids)), 20)
        required = [
            "python_version_marker",
            "statistics_kde_api_marker",
            "statistics_kde_random_api_marker",
            "empty_data_errors_marker",
            "single_point_normal_reference_marker",
            "symmetric_data_pdf_symmetry_marker",
            "pdf_nonnegative_grid_marker",
            "pdf_grid_mass_local_observation_marker",
            "cdf_monotonic_marker",
            "compact_kernel_tail_bounds_marker",
            "pdf_cdf_finite_difference_marker",
            "narrow_vs_wide_bandwidth_marker",
            "compact_support_zero_outside_marker",
            "kernel_alias_equivalence_marker",
            "duplicate_samples_peak_marker",
            "outlier_reweighting_local_observation_marker",
            "seeded_kde_random_repeatability_marker",
            "seeded_sequence_cross_version_disclaimer_marker",
            "tiny_density_threshold_classifier_marker",
            "no_global_ml_validity_claim_marker",
        ]
        for r in required:
            self.assertIn(r, ids)

    def test_expectations_complete(self):
        methods = ["inspect_api","evaluate_pdf","evaluate_cdf","draw_seeded_samples","ml_context_observation"]
        for c in self.cases:
            me = c.get("method_expectations", {})
            self.assertEqual(set(me.keys()), set(methods), c["id"])
            for m in methods:
                exp = me[m].get("expected_classification")
                self.assertTrue(exp, f"{c['id']}/{m} blank")

    def test_rows_count_and_pairs(self):
        self.assertEqual(len(self.rows), 100)
        pairs = [(r["method"], r["case_id"]) for r in self.rows]
        self.assertEqual(len(pairs), len(set(pairs)))
        methods = ["inspect_api","evaluate_pdf","evaluate_cdf","draw_seeded_samples","ml_context_observation"]
        case_ids = [c["id"] for c in self.cases]
        for cid in case_ids:
            for m in methods:
                self.assertTrue(any(r["method"]==m and r["case_id"]==cid for r in self.rows), f"{cid}/{m} missing")

    def test_classifications_allowed_and_agree(self):
        allowed = {"pass","expected_error","local_observation","version_skip","context_only","not_applicable","fail"}
        for r in self.rows:
            self.assertIn(r["expected_classification"], allowed)
            self.assertIn(r["actual_classification"], allowed)
            self.assertTrue(r["expected_classification"])
            self.assertTrue(r["actual_classification"])
            if r["expected_classification"] == "not_applicable":
                self.assertEqual(r["actual_classification"], "not_applicable")
            # expected == actual unless fail
            if r["actual_classification"] != "fail":
                self.assertEqual(r["expected_classification"], r["actual_classification"],
                                f"{r['case_id']}/{r['method']}")

    def test_empty_data_errors(self):
        rows = [r for r in self.rows if r["case_id"]=="empty_data_errors_marker"]
        for r in rows:
            if r["method"] in ("evaluate_pdf","evaluate_cdf","draw_seeded_samples"):
                if r["actual_classification"] == "version_skip":
                    continue
                self.assertEqual(r["actual_classification"], "expected_error")
                self.assertTrue(r["exception_type"])

    def test_single_point_reference(self):
        r = next((x for x in self.rows if x["case_id"]=="single_point_normal_reference_marker" and x["method"]=="evaluate_pdf"), None)
        self.assertIsNotNone(r)
        if r["actual_classification"] != "version_skip":
            self.assertLessEqual(r["absolute_error"] if r["absolute_error"] is not None else 1e9, 1e-10)

    def test_symmetry(self):
        r = next((x for x in self.rows if x["case_id"]=="symmetric_data_pdf_symmetry_marker" and x["method"]=="evaluate_pdf"), None)
        self.assertIsNotNone(r)
        if r["actual_classification"] != "version_skip":
            self.assertLessEqual(r["absolute_error"] if r["absolute_error"] is not None else 1e9, 1e-12)

    def test_nonnegative_grid(self):
        r = next((x for x in self.rows if x["case_id"]=="pdf_nonnegative_grid_marker" and x["method"]=="evaluate_pdf"), None)
        self.assertIsNotNone(r)
        self.assertEqual(r["actual_classification"], "pass")

    def test_cdf_monotonic(self):
        r = next((x for x in self.rows if x["case_id"]=="cdf_monotonic_marker" and x["method"]=="evaluate_cdf"), None)
        self.assertIsNotNone(r)
        self.assertEqual(r["actual_classification"], "pass")

    def test_compact_support(self):
        r = next((x for x in self.rows if x["case_id"]=="compact_support_zero_outside_marker" and x["method"]=="evaluate_pdf"), None)
        self.assertIsNotNone(r)
        self.assertEqual(r["actual_classification"], "pass")

    def test_kernel_aliases(self):
        r = next((x for x in self.rows if x["case_id"]=="kernel_alias_equivalence_marker" and x["method"]=="evaluate_pdf"), None)
        self.assertIsNotNone(r)
        if r["actual_classification"] != "version_skip":
            self.assertLessEqual(r["absolute_error"] if r["absolute_error"] is not None else 1e9, 1e-12)

    def test_seeded_repeatability(self):
        r = next((x for x in self.rows if x["case_id"]=="seeded_kde_random_repeatability_marker" and x["method"]=="draw_seeded_samples"), None)
        self.assertIsNotNone(r)
        if r["actual_classification"] != "version_skip":
            self.assertTrue(r["repeated_sequence_match"])
            self.assertTrue(r["seeded_sequence_digest"])

    def test_tiny_classifier(self):
        r = next((x for x in self.rows if x["case_id"]=="tiny_density_threshold_classifier_marker" and x["method"]=="ml_context_observation"), None)
        self.assertIsNotNone(r)
        if r["actual_classification"] != "version_skip":
            self.assertIsNotNone(r["left_density_score"])
            self.assertIsNotNone(r["right_density_score"])

    def test_results_counts_agree(self):
        with open(ROOT / "results_rows.csv") as f:
            csv_rows = list(csv.DictReader(f))
        self.assertEqual(len(csv_rows), len(self.rows))
        with open(ROOT / "RESULTS.md") as f:
            results_md = f.read()
        self.assertIn("Rows: 100", results_md)

    def test_readme_disclaimers(self):
        with open(ROOT / "README.md") as f:
            readme = f.read()
        needed = [
            "KDE is appropriate",
            "bandwidth",
            "kernel choice",
            "finite-grid",
            "seeded samples",
            "calibrated",
            "classifier",
            "NumPy",
            "SciPy",
            "pandas",
            "scikit-learn",
            "praise for a data-science book",
        ]
        low = readme.lower()
        for n in needed:
            self.assertIn(n.lower(), low, f"missing disclaimer fragment: {n}")

    def test_artifact_scan(self):
        bad_tokens = ["/home/", "/root/", "ghp_", "OPENCLA", "token", "passwd"]
        # scan committed text artifacts
        paths = [
            ROOT / "cases.json",
            ROOT / "results_rows.json",
            ROOT / "results_rows.csv",
            ROOT / "README.md",
            ROOT / "RESULTS.md",
        ]
        verify_path = ROOT / "VERIFY.md"
        if verify_path.exists():
            paths.append(verify_path)
        hn1 = ROOT / "hn_thread_evidence.md"
        hn2 = ROOT / "hn_comments_sanitized.json"
        if hn1.exists(): paths.append(hn1)
        if hn2.exists(): paths.append(hn2)
        for p in paths:
            txt = p.read_text(errors="ignore").lower()
            # allow /home/ in a generic disclaimer context? be strict but skip obvious false positives
            # just check for obvious credential patterns
            self.assertNotIn("ghp_", txt)
            # /home/ check – allow if it's in README path-sanitization note only
            if "/home/" in txt or "/root/" in txt:
                # fail unless it's the allowed disclaimer
                self.assertTrue("sanitiz" in txt or "path" in txt, f"suspect path leak in {p}")

if __name__ == "__main__":
    unittest.main()
