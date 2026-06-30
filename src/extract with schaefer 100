from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import nibabel as nib
from nilearn import datasets
from nilearn.image import resample_to_img

def get_schaefer_atlas(mask_img, n_rois=100):
    """
    Fetch the Schaefer 2018 atlas and resample it to the subject's brain mask space.
    """
    print(f"Fetching Schaefer 2018 atlas with {n_rois} ROIs...")
    # 載入 Schaefer 100 圖譜 (7個預設網絡)
    schaefer = datasets.fetch_atlas_schaefer_2018(n_rois=n_rois, yeo_networks=7, resolution_mm=2)
    atlas_img = nib.load(schaefer.maps)

    print("Resampling atlas to match subject space...")
    # 將圖譜的空間維度 (Voxel size & Affine) 重採樣到與該受試者的 mask 一致
    resampled_atlas = resample_to_img(atlas_img, mask_img, interpolation='nearest')

    # 確保圖譜只套用在大腦範圍內 (過濾掉 mask 以外的雜訊)
    atlas_data = resampled_atlas.get_fdata().astype(int)
    mask_data = mask_img.get_fdata() > 0
    atlas_data[~mask_data] = 0

    final_atlas_img = nib.Nifti1Image(atlas_data, resampled_atlas.affine, resampled_atlas.header)
    
    return final_atlas_img

def extract_roi_timeseries(bold_img, atlas_img):
    """
    Extract mean BOLD signal within each ROI label.
    """
    bold_data = bold_img.get_fdata()
    atlas_data = atlas_img.get_fdata().astype(int)

    if bold_data.ndim != 4:
        raise ValueError(f"BOLD image must be 4D, got shape: {bold_data.shape}")

    if atlas_data.shape != bold_data.shape[:3]:
        raise ValueError(
            f"Atlas shape {atlas_data.shape} does not match BOLD spatial shape {bold_data.shape[:3]}"
        )

    labels = sorted([x for x in np.unique(atlas_data) if x > 0])
    n_t = bold_data.shape[3]
    ts = np.zeros((n_t, len(labels)), dtype=np.float32)

    for j, label in enumerate(labels):
        roi_mask = atlas_data == label
        roi_voxels = bold_data[roi_mask, :]
        ts[:, j] = np.nanmean(roi_voxels, axis=0)

    return ts, labels

def standardize_timeseries(ts):
    """
    Z-score each ROI time series.
    """
    mean = np.nanmean(ts, axis=0, keepdims=True)
    std = np.nanstd(ts, axis=0, keepdims=True)
    std[std == 0] = 1
    return (ts - mean) / std

def main():
    parser = argparse.ArgumentParser(description="Extract ROI time series from ready resting-state BOLD data.")
    parser.add_argument("--ready-index", type=str, default="outputs/qc/rest_ready_for_roi.csv")
    parser.add_argument("--output-dir", type=str, default="outputs/roi_timeseries")
    parser.add_argument("--atlas-mode", type=str, default="schaefer", choices=["schaefer"])
    args = parser.parse_args()

    ready_path = Path(args.ready_index)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not ready_path.exists():
        raise FileNotFoundError(f"Ready index not found: {ready_path}")

    df = pd.read_csv(ready_path)
    summary_rows = []

    for _, row in df.iterrows():
        subject = row["subject"]
        session = row["session"]
        task = row["task"]
        run = row["run"]

        bold_path = Path(row["bold_mni_path"])
        mask_path = Path(row["brain_mask_path"])

        print("=" * 70)
        print(f"Processing: {subject} {session} {task} {run}")
        print(f"BOLD: {bold_path}")
        print(f"Mask: {mask_path}")

        bold_img = nib.load(str(bold_path))
        mask_img = nib.load(str(mask_path))

        # 套用 Schaefer 100
        atlas_img = get_schaefer_atlas(mask_img, n_rois=100)
        
        ts, roi_labels = extract_roi_timeseries(bold_img, atlas_img)
        ts_z = standardize_timeseries(ts)

        base = f"{subject}_{session}_{task}_{run}"

        # 檔名更新為 schaefer100 以做區隔
        atlas_out = output_dir / f"{base}_schaefer100_atlas.nii.gz"
        ts_out = output_dir / f"{base}_roi_timeseries.csv"
        ts_z_out = output_dir / f"{base}_roi_timeseries_z.csv"
        labels_out = output_dir / f"{base}_roi_labels.csv"

        nib.save(atlas_img, str(atlas_out))

        ts_df = pd.DataFrame(ts, columns=[f"ROI_{label:03d}" for label in roi_labels])
        ts_z_df = pd.DataFrame(ts_z, columns=[f"ROI_{label:03d}" for label in roi_labels])
        labels_df = pd.DataFrame({"roi_index": range(1, len(roi_labels) + 1), "roi_label": roi_labels})

        ts_df.to_csv(ts_out, index=False)
        ts_z_df.to_csv(ts_z_out, index=False)
        labels_df.to_csv(labels_out, index=False)

        print(f"Saved atlas:           {atlas_out}")
        print(f"Saved time series:     {ts_out}")
        print(f"Saved z time series:   {ts_z_out}")
        print(f"Saved ROI labels:      {labels_out}")
        print(f"Time series shape:     {ts.shape}")

        summary_rows.append(
            {
                "subject": subject,
                "session": session,
                "task": task,
                "run": run,
                "n_timepoints": ts.shape[0],
                "n_rois": ts.shape[1],
                "atlas_path": str(atlas_out),
                "timeseries_path": str(ts_out),
                "timeseries_z_path": str(ts_z_out),
                "labels_path": str(labels_out),
            }
        )

    summary_df = pd.DataFrame(summary_rows)
    summary_out = output_dir / "roi_timeseries_summary.csv"
    summary_df.to_csv(summary_out, index=False)

    print("=" * 70)
    print("ROI time series extraction (Schaefer 100) completed")
    print(f"Summary saved to: {summary_out}")
    print(summary_df.to_string(index=False))

if __name__ == "__main__":
    main()
