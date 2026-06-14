from pathlib import Path
import argparse
import re
import pandas as pd


def parse_bids_entities(path):
    """
    Parse basic BIDS-like entities from a file path.

    Expected examples:
    sub-PC211_ses-02_task-rest_run-1_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz
    sub-PC211_ses-02_task-rest_run-1_desc-confounds_timeseries.tsv
    """
    name = path.name

    entities = {
        "subject": None,
        "session": None,
        "task": None,
        "run": None,
    }

    patterns = {
        "subject": r"(sub-[A-Za-z0-9]+)",
        "session": r"(ses-[A-Za-z0-9]+)",
        "task": r"task-([A-Za-z0-9]+)",
        "run": r"run-([A-Za-z0-9]+)",
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, name)
        if match:
            if key == "task":
                entities[key] = f"task-{match.group(1)}"
            elif key == "run":
                entities[key] = f"run-{match.group(1)}"
            else:
                entities[key] = match.group(1)

    return entities


def make_key(entities):
    return (
        entities["subject"],
        entities["session"],
        entities["task"],
        entities["run"],
    )


def safe_relative_path(path, root):
    """
    Return a path relative to root if possible.
    If path is None, return an empty string.
    """
    if path is None:
        return ""

    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def main():
    parser = argparse.ArgumentParser(
        description="Build a resting-state fMRIPrep file index for PsiConnect."
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        required=True,
        help="Path to local ds006110 dataset directory."
    )
    parser.add_argument(
        "--output",
        type=str,
        default="outputs/file_index/rest_file_index.csv",
        help="Output CSV path."
    )
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    fmriprep_dir = data_dir / "derivatives" / "fmriprep-22.0.2"

    if not fmriprep_dir.exists():
        raise FileNotFoundError(f"fMRIPrep directory not found: {fmriprep_dir}")

    bold_files = sorted(
        fmriprep_dir.glob(
            "**/*task-rest*space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"
        )
    )

    confound_files = sorted(
        fmriprep_dir.glob(
            "**/*task-rest*desc-confounds_timeseries.tsv"
        )
    )

    mask_files = sorted(
        fmriprep_dir.glob(
            "**/*task-rest*space-MNI152NLin2009cAsym_desc-brain_mask.nii.gz"
        )
    )

    confound_map = {}
    for path in confound_files:
        entities = parse_bids_entities(path)
        confound_map[make_key(entities)] = path

    mask_map = {}
    for path in mask_files:
        entities = parse_bids_entities(path)
        mask_map[make_key(entities)] = path

    rows = []

    for bold_path in bold_files:
        entities = parse_bids_entities(bold_path)
        key = make_key(entities)

        confound_path = confound_map.get(key)
        mask_path = mask_map.get(key)

        bold_exists = bold_path.exists()
        confounds_exists = confound_path.exists() if confound_path else False
        mask_exists = mask_path.exists() if mask_path else False

        ready_for_analysis = bool(
            bold_exists
            and confounds_exists
            and mask_exists
        )

        row = {
            "subject": entities["subject"],
            "session": entities["session"],
            "task": entities["task"],
            "run": entities["run"],

            "bold_mni_path": str(bold_path),
            "confounds_path": str(confound_path) if confound_path else "",
            "brain_mask_path": str(mask_path) if mask_path else "",

            "bold_mni_relpath": safe_relative_path(bold_path, data_dir),
            "confounds_relpath": safe_relative_path(confound_path, data_dir),
            "brain_mask_relpath": safe_relative_path(mask_path, data_dir),

            "bold_exists": bold_exists,
            "confounds_exists": confounds_exists,
            "mask_exists": mask_exists,
            "ready_for_analysis": ready_for_analysis,
        }

        rows.append(row)

    df = pd.DataFrame(rows)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    print("=" * 70)
    print("Resting-state file index generated")
    print("=" * 70)
    print(f"Dataset directory: {data_dir}")
    print(f"fMRIPrep directory: {fmriprep_dir}")
    print(f"Output: {output_path}")
    print(f"Rows: {len(df)}")

    print()
    print("Ready for analysis:")
    print(df["ready_for_analysis"].value_counts(dropna=False))

    print()
    print("Session counts:")
    print(df["session"].value_counts(dropna=False).sort_index())

    print()
    print("File existence summary:")
    print(f"BOLD exists:      {df['bold_exists'].sum()} / {len(df)}")
    print(f"Confounds exists: {df['confounds_exists'].sum()} / {len(df)}")
    print(f"Masks exists:     {df['mask_exists'].sum()} / {len(df)}")

    print()
    print("First 10 rows:")
    print(df.head(10).to_string(index=False))


if __name__ == "__main__":
    main()
