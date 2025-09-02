# server/utils_io.py
from pathlib import Path
import pandas as pd
import base64
import io
import json

DATA_DIR = Path("/data/uploads")

def save_dataset_from_bytes(dataset_id: str, file_bytes: bytes, filename: str, base_dir=DATA_DIR):
    base_dir.mkdir(parents=True, exist_ok=True)
    dest = base_dir / f"{dataset_id}_{filename}"
    with open(dest, "wb") as f:
        f.write(file_bytes)
    return dest

def read_sheet(dataset_id, sheet_name=None):
    files = list(DATA_DIR.glob(f"{dataset_id}_*"))
    if not files:
        raise FileNotFoundError("dataset not found")
    path = files[0]
    df = pd.read_excel(path, sheet_name=sheet_name)
    if isinstance(df, dict):
        if sheet_name is None:
            first = list(df.keys())[0]
            return df[first]
        else:
            return df[sheet_name]
    return df

