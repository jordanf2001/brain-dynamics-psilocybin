# Dataset Status

## Dataset

- Name: PsiConnect
- OpenNeuro ID: ds006110
- Format: BIDS + BIDS Derivatives
- Download method: DataLad / git-annex
- Local development path: `/Users/macbookair/ds006110`

---

## Confirmed Available

The following components were identified in the local DataLad dataset structure:

- Raw multi-echo fMRI
- Resting-state fMRI
- Two sessions
- fMRIPrep 22.0.2 derivatives
- MNI152NLin2009cAsym preprocessed BOLD
- Confounds timeseries TSV
- MNI-space brain masks
- MRIQC derivatives
- FreeSurfer derivatives
- tedana/SPM derivatives

---

## fMRIPrep Directory

The main derivative directory used in this project is:

```text
/Users/macbookair/ds006110/derivatives/fmriprep-22.0.2
```

---

## Automated Inspection

The dataset was inspected using:

```bash
python src/check_dataset.py --data-dir /Users/macbookair/ds006110
```

The inspection searched for resting-state fMRIPrep outputs matching the following file patterns:

```text
*task-rest*space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz
*task-rest*desc-confounds_timeseries.tsv
*task-rest*space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz
```

---

## Updated fMRIPrep Resting-State Availability

Automated inspection confirmed the following file counts:

| Item | Count |
|---|---:|
| Resting-state MNI-space preprocessed BOLD | 127 |
| Resting-state confounds TSV | 127 |
| Resting-state MNI-space brain masks | 127 |
| All resting-state derivative files | 5877 |
| ses-01 resting-state MNI BOLD | 65 |
| ses-02 resting-state MNI BOLD | 62 |
| ses-01 resting-state confounds | 65 |
| ses-02 resting-state confounds | 62 |

Summary:

```text
BOLD/confounds count match: YES
BOLD/mask count match: YES
FC/dFC pipeline feasibility: YES
```

These results indicate that the dataset contains the core files required for ROI-based resting-state functional connectivity and dynamic functional connectivity analyses.

---

## File Index

A resting-state file index has been generated:

```text
outputs/file_index/rest_file_index.csv
```

The file index includes:

- subject
- session
- task
- run
- MNI-space BOLD absolute path
- confounds absolute path
- brain mask absolute path
- MNI-space BOLD relative path
- confounds relative path
- brain mask relative path
- file existence indicators
- readiness for analysis

This file will serve as the main input table for subsequent QC, ROI time-series extraction, static FC, and dynamic FC analyses.

---

## Current Interpretation

The dataset is currently suitable for the following next-stage analyses:

- BOLD metadata quality control
- confounds alignment checks
- ROI time-series extraction
- static functional connectivity
- sliding-window dynamic functional connectivity

However, the current status should be interpreted as **file-level feasibility**, not yet as completed image-level quality control.

---

## Still Needs Verification

Although the dataset has sufficient file coverage for FC/dFC analysis, the following issues still require verification:

- Exact experimental meaning of `ses-01` and `ses-02`
- Whether sessions correspond to pre/post, drug/placebo, or other experimental design factors
- Whether all git-annexed NIfTI files have been fully downloaded and are readable
- Whether BOLD timepoints match confounds rows
- Whether BOLD images have consistent shapes and TRs
- Motion quality, especially framewise displacement distributions
- Subject-level completeness across sessions
- Which participants have complete paired ses-01 and ses-02 resting-state data

---

## Next Dataset-Level Task

The next dataset-level task is to generate a BOLD metadata QC table:

```text
outputs/qc/rest_bold_qc.csv
```

The planned QC table should include:

- BOLD readability
- image shape
- number of volumes
- TR
- confounds row count
- BOLD/confounds timepoint alignment
- brain mask readability
- framewise displacement summaries
- readiness for ROI extraction
