# Dataset Status

## Dataset
- Name: PsiConnect
- OpenNeuro ID: ds006110
- Format: BIDS + BIDS Derivatives
- Download method: DataLad / git-annex

## Confirmed Available
- Raw multi-echo fMRI
- Resting-state fMRI
- Two sessions
- fMRIPrep 22.0.2 derivatives
- MNI152NLin2009cAsym preprocessed BOLD
- Confounds timeseries TSV
- Brain masks
- MRIQC
- FreeSurfer
- tedana/SPM derivatives

## Still Needs Verification
- Exact session meaning: ses-01 vs ses-02
- Number of subjects with complete rest data
- Whether all subjects have both BOLD and confounds
- Whether `datalad get` works via available remotes

## Updated fMRIPrep Resting-State Availability

Local DataLad file-tree inspection confirmed the presence of resting-state fMRIPrep derivatives.

Command used:

```bash
find derivatives/fmriprep-22.0.2 -name "*task-rest*space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz" | wc -l
find derivatives/fmriprep-22.0.2 -name "*task-rest*desc-confounds_timeseries.tsv" | wc -l
```

Results:

| File type | Count |
|---|---:|
| MNI-space resting-state preprocessed BOLD | 127 |
| Resting-state confounds timeseries TSV | 127 |

This confirms that the dataset contains sufficient fMRIPrep outputs to support ROI-based resting-state functional connectivity and dynamic functional connectivity analyses.
