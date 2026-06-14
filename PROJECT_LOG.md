# Project Log

### Repository Setup

- Created GitHub repository: `altered-states-dfc`.
- Confirmed local repository path:

```text
/Users/macbookair/altered-states-dfc
```

- Confirmed local dataset path:

```text
/Users/macbookair/ds006110
```

- Confirmed that the repository contains the initial project structure, documentation, and inspection scripts.

---

### Dataset Inspection

Ran:

```bash
python src/check_dataset.py --data-dir /Users/macbookair/ds006110
```

Results:

| Item | Count |
|---|---:|
| Rest MNI preprocessed BOLD | 127 |
| Rest confounds TSV | 127 |
| Rest MNI brain masks | 127 |
| All rest derivatives | 5877 |
| ses-01 rest MNI BOLD | 65 |
| ses-02 rest MNI BOLD | 62 |
| ses-01 rest confounds | 65 |
| ses-02 rest confounds | 62 |

Summary:

```text
BOLD/confounds count match: YES
BOLD/mask count match: YES
FC/dFC pipeline feasibility: YES
```

---

### File Index

Generated resting-state file index:

```text
outputs/file_index/rest_file_index.csv
```

The file index contains subject/session-level paths for:

- MNI-space preprocessed BOLD images
- confounds TSV files
- MNI-space brain masks

The file index was successfully pushed to GitHub.

---

### Current Interpretation

The project has completed the initial dataset inspection and file-index generation stages.

Current status:

```text
Dataset structure inspection: completed
File index generation: completed
DataLad content retrieval test: completed
Single-run local readiness: completed
Image-level QC: next step
ROI time-series extraction: not yet started
Static FC: not yet started
Dynamic FC: not yet started

```

The dataset appears feasible for downstream ROI-based FC/dFC analyses, but image-level quality control is still required before formal analysis.

---

### Next Steps

- Update README, dataset status, and analysis plan.
- Standardize dependency file name from `requirement.txt` to `requirements.txt`.
- Update `src/check_dataset.py` to include BOLD/mask count matching.
- Update `src/build_file_index.py` to include relative paths.
- Build BOLD metadata QC script:

```text
src/qc_bold_metadata.py
```

- Generate BOLD metadata QC output:

```text
outputs/qc/rest_bold_qc.csv
```

- Confirm the experimental meaning of `ses-01` and `ses-02`.
- Test single-subject ROI time-series extraction.
