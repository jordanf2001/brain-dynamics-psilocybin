# Analysis Plan

## Project Goal

This project aims to develop a reproducible resting-state functional connectivity and dynamic functional connectivity pipeline for the PsiConnect dataset.

The primary scientific goal is to examine whether psilocybin-associated altered states of consciousness are related to changes in the static and dynamic organization of large-scale brain networks.

---

## Main Research Questions

1. How does resting-state functional connectivity differ across experimental sessions?
2. Do dynamic functional connectivity measures capture temporal network changes beyond static FC?
3. Which large-scale brain networks show the strongest changes in connectivity or temporal variability?
4. Can dynamic features provide additional information about altered states of consciousness beyond average connectivity strength?

---

## Current Completed Stages

### Stage 1. Dataset Inspection

Completed using:

```bash
python src/check_dataset.py --data-dir /Users/macbookair/ds006110
```

Confirmed:

- 127 resting-state MNI-space preprocessed BOLD files
- 127 resting-state confounds TSV files
- 127 MNI-space brain masks
- 65 ses-01 rest BOLD files
- 62 ses-02 rest BOLD files
- BOLD/confounds count match
- BOLD/mask count match
- Initial FC/dFC pipeline feasibility

### Stage 2. File Index Generation

Completed using:

```bash
python src/build_file_index.py --data-dir /Users/macbookair/ds006110
```

Generated:

```text
outputs/file_index/rest_file_index.csv
```

The file index provides the subject/session-level map for downstream analyses.

---

## Planned Analysis Pipeline

```text
OpenNeuro / DataLad dataset
↓
BIDS and fMRIPrep inspection
↓
Resting-state file index generation
↓
BOLD/confounds/mask QC
↓
ROI parcellation
↓
ROI time-series extraction
↓
Static FC estimation
↓
Sliding-window dFC estimation
↓
Dynamic feature extraction
↓
Session-level comparison
```

---

## Stage 3. Quality Control

The next planned stage is to create a metadata QC table for all indexed resting-state runs.

Planned checks:

- BOLD image readability
- BOLD image shape
- number of timepoints
- repetition time, TR
- confounds file readability
- number of confounds rows
- BOLD/confounds temporal alignment
- framewise displacement summary
- brain mask readability
- readiness for ROI extraction

Planned output:

```text
outputs/qc/rest_bold_qc.csv
```

This stage is necessary because file existence alone does not guarantee that the NIfTI files are fully downloaded, readable, or temporally aligned with confounds.

---

## Stage 4. ROI Time-Series Extraction

After QC, ROI time series will be extracted from MNI-space preprocessed BOLD images using a standard atlas.

Candidate atlases:

- Schaefer 100 parcels
- Schaefer 200 parcels
- AAL
- Harvard-Oxford

Initial plan:

```text
Schaefer 100 parcels
```

The first implementation will focus on one subject and one session to validate the pipeline before scaling to all available runs.

Planned output:

```text
outputs/timeseries/
```

Expected format:

```text
timepoints × ROIs
```

---

## Stage 5. Static Functional Connectivity

Static FC will be estimated by computing Pearson correlations between ROI time series.

For ROI signals $$x_i$$ and $$x_j$$:

$$FC_{ij} = corr(x_i, x_j)$$

Correlation coefficients may be transformed using Fisher z-transform:

$$z_{ij} = \frac{1}{2}\ln\left(\frac{1+r_{ij}}{1-r_{ij}}\right)$$

Planned outputs:

```text
outputs/fc_matrices/
outputs/figures/
```

Possible outputs:

- ROI-by-ROI static FC matrix
- Fisher z-transformed FC matrix
- static FC heatmap
- network-level summary measures

---

## Stage 6. Dynamic Functional Connectivity

Dynamic FC will be estimated using sliding-window correlation.

For the $$t$$-th window:

$$dFC_t = corr(X_{t:t+w})$$

where $$w$$ is the window length.

Potential dynamic features:

- FC variability
- mean connectivity across windows
- temporal variance of each edge
- dwell time in connectivity states
- transition probability between states
- network flexibility
- metastability-like measures

The exact window length and step size will be determined after confirming TR and number of timepoints during QC.

---

## Stage 7. Statistical Comparison

Potential comparisons:

- ses-01 vs ses-02
- complete-case within-subject comparison
- session-level differences in static FC
- session-level differences in dFC variability
- network-level summary comparison

Potential statistical methods:

- paired t-test
- permutation testing
- linear mixed-effects models
- FDR correction
- network-level summary statistics

Before formal statistical analysis, the experimental meaning of `ses-01` and `ses-02` must be confirmed.

---

## Minimal Viable Analysis

The minimal viable analysis for this project is:

```text
1 subject × 1 session × 1 resting-state run
↓
ROI time-series extraction
↓
static FC matrix
↓
simple sliding-window dFC
↓
basic dynamic feature visualization
```

After this minimal pipeline is validated, the analysis can be extended to:

```text
all available subjects × available sessions × resting-state runs
```

---

## Current Priority

The immediate next step is:

```text
Build a BOLD metadata QC table before ROI time-series extraction.
```

The next script planned for the repository is:

```text
src/qc_bold_metadata.py
```

The expected output is:

```text
outputs/qc/rest_bold_qc.csv
```

