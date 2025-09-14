from pathlib import Path
import pandas as pd
import json
from typing import Optional, Tuple

DATA_DIR = Path("/data/uploads")
DATA_DIR.mkdir(parents=True, exist_ok=True)


def save_dataset_from_bytes(dataset_id: str, file_bytes: bytes, filename: str, base_dir: Optional[Path] = None) -> Path:
    base = (base_dir or DATA_DIR)
    base.mkdir(parents=True, exist_ok=True)

    dest = base / f"{dataset_id}_{filename}"
    with open(dest, "wb") as f:
        f.write(file_bytes)

    meta = {"id": dataset_id, "filename": filename, "path": str(dest)}
    with open(base / f"{dataset_id}.meta.json", "w", encoding="utf-8") as mf:
        json.dump(meta, mf, ensure_ascii=False, indent=2)

    return dest


def _find_dataset_file(dataset_id: str, base_dir: Optional[Path] = None) -> Path:
    base = (base_dir or DATA_DIR)

    meta_path = base / f"{dataset_id}.meta.json"
    if meta_path.exists():
        try:
            data = json.loads(meta_path.read_text(encoding="utf-8"))
            p = Path(data.get("path", ""))
            if p.exists():
                return p
        except Exception:
            pass

    exact = base / dataset_id
    if exact.exists():
        return exact

    by_prefix = list(base.glob(f"{dataset_id}_*"))
    if by_prefix:
        return by_prefix[0]

    for p in base.iterdir():
        if p.is_file() and p.stem == dataset_id:
            return p

    for ext in (".xlsx", ".xls", ".csv"):
        cand = base / f"{dataset_id}{ext}"
        if cand.exists():
            return cand

    raise FileNotFoundError(f"Dataset '{dataset_id}' not found in {base}")


def _read_excel_with_engine(path: Path, sheet_name: Optional[str] = None) -> pd.DataFrame:
    ext = path.suffix.lower()
    engine = None
    if ext in (".xlsx", ".xlsm", ".xltx", ".xltm"):
        engine = "openpyxl"
    elif ext == ".xls":
        engine = "xlrd" 
    try:
        if ext == ".csv":
            return pd.read_csv(path)
        return pd.read_excel(path, sheet_name=sheet_name, engine=engine)
    except ValueError as e:
        raise ValueError(f"Error leyendo Excel '{path}': {e}. Asegúrate de que el archivo no esté corrupto "
                         "y que tengas instalado 'openpyxl' (para .xlsx) o 'xlrd' (para .xls).") from e
    except Exception as e:
        raise RuntimeError(f"Error leyendo archivo '{path}': {e}") from e


def read_sheet(dataset_id: str, sheet_name: Optional[str] = None, base_dir: Optional[Path] = None) -> pd.DataFrame:
    path = _find_dataset_file(dataset_id, base_dir=base_dir)
    df_or_dict = _read_excel_with_engine(path, sheet_name=sheet_name)

    if isinstance(df_or_dict, dict):
        # pd.read_excel puede devolver dict cuando sheet_name=None -> dict[hoja] = df
        if sheet_name is None:
            first_sheet = next(iter(df_or_dict))
            return df_or_dict[first_sheet]
        else:
            if sheet_name in df_or_dict:
                return df_or_dict[sheet_name]
            else:
                raise ValueError(f"Sheet '{sheet_name}' no encontrada en '{path}'. Hojas disponibles: {list(df_or_dict.keys())}")
    return df_or_dict

def get_available_datasets(base_dir: Optional[Path] = None) -> list[dict]:
    base = (base_dir or DATA_DIR)
    datasets = []
    for meta_path in base.glob("*.meta.json"):
        try:
            data = json.loads(meta_path.read_text(encoding="utf-8"))
            datasets.append(data)
        except Exception:
            pass
    return datasets


