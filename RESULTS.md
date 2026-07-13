# Results – python-stdlib-kde-bandwidth-footgun-lab

Python: 3.14.6  
Implementation: CPython  
Platform: Linux-6.17.0-1009-aws-x86_64-with-glibc2.39  
statistics.kde available: True  
statistics.kde_random available: True  

Cases: 20  
Methods: 5  
Rows: 100  

Classifications:
- pass: 14
- expected_error: 3
- local_observation: 6
- context_only: 8
- not_applicable: 69
- version_skip: 0
- fail: 0

Total runtime: 0.002s

## Observations

- python_version_marker / ml_context_observation: version recorded, no ML claim
- statistics_kde_random_api_marker / ml_context_observation: kde_random is sampling, not ML training
- single_point_normal_reference_marker / evaluate_pdf: single normal kernel matches math.exp reference
- symmetric_data_pdf_symmetry_marker / evaluate_pdf: mirrored densities agree for symmetric data
- pdf_nonnegative_grid_marker / evaluate_pdf: grid min=3.72008e-07 max=0.199824, all finite nonnegative
- pdf_grid_mass_local_observation_marker / evaluate_pdf: finite-grid mass ≈ 1.000000, distance from 1.0 = 0.000000
- cdf_monotonic_marker / evaluate_cdf: CDF values non-decreasing on grid
- compact_kernel_tail_bounds_marker / evaluate_cdf: tail low=0 high=1
- pdf_cdf_finite_difference_marker / evaluate_pdf: pdf at interior point recorded
- pdf_cdf_finite_difference_marker / evaluate_cdf: pdf=0.199649 fd=0.199649 abs_err=1.97e-11
- narrow_vs_wide_bandwidth_marker / evaluate_pdf: narrow bandwidth preserves more local variation for this sample; not a universal rule
- compact_support_zero_outside_marker / evaluate_pdf: outside=[0.0, 0.0] inside=1
- kernel_alias_equivalence_marker / evaluate_pdf: alias max_diff=0
- duplicate_samples_peak_marker / evaluate_pdf: center=0.7979 far=0.0002677, duplicated input is not independent evidence
- outlier_reweighting_local_observation_marker / evaluate_pdf: base@[0,20]=[0.3321647544371834, 3.937402644738488e-219] outlier@[0,20]=[0.24912356582788756, 0.16622595016726363]; outlier changes all mixture weights
- seeded_kde_random_repeatability_marker / draw_seeded_samples: seeded sequences match locally
- seeded_sequence_cross_version_disclaimer_marker / draw_seeded_samples: seed gives local repeatability, not cross-version bit identity
- seeded_sequence_cross_version_disclaimer_marker / ml_context_observation: seed gives local repeatability, not cross-version bit identity
- tiny_density_threshold_classifier_marker / ml_context_observation: density comparison is not a validated classifier; no accuracy computed; 1-D toy only; 3 queries recorded
- no_global_ml_validity_claim_marker / inspect_api: no global ML validity claim
- no_global_ml_validity_claim_marker / evaluate_pdf: no global ML validity claim
- no_global_ml_validity_claim_marker / evaluate_cdf: no global ML validity claim
- no_global_ml_validity_claim_marker / draw_seeded_samples: no global ML validity claim
- no_global_ml_validity_claim_marker / ml_context_observation: no global ML validity claim

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
