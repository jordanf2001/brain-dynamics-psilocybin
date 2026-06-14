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
