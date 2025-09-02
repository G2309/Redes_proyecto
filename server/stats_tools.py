# server/stats_tools.py
import os, uuid, json
import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from utils_io import save_dataset_from_bytes, get_dataset_path, read_sheet

DATA_DIR = Path("/data/uploads")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def upload_excel_bytes(file_bytes: bytes, filename: str) -> str:
    dataset_id = str(uuid.uuid4())
    path = save_dataset_from_bytes(dataset_id, file_bytes, filename, base_dir=DATA_DIR)
    meta = {"id": dataset_id, "filename": filename, "path": str(path)}
    with open(DATA_DIR / f"{dataset_id}.meta.json", "w") as f:
        json.dump(meta, f)
    return dataset_id

def describe_dataset(dataset_id: str, sheet_name: str = None) -> dict:
    df = read_sheet(dataset_id, sheet_name)
    desc = df.describe(include='all').to_dict()
    missing = df.isnull().sum().to_dict()
    return {"basic": desc, "missing": missing, "shape": df.shape, "dtypes": df.dtypes.astype(str).to_dict()}

def compute_proportion(dataset_id, sheet_name, numerator_filter, denominator_filter):
    df = read_sheet(dataset_id, sheet_name)
    num = df.query(numerator_filter).shape[0]
    den = df.query(denominator_filter).shape[0]
    return {"numerator": num, "denominator": den, "proportion": None if den==0 else num/den}

def compute_or_rr(dataset_id, sheet_name, exposure_col, outcome_col, exposure_val, outcome_val):
    df = read_sheet(dataset_id, sheet_name)
    a = ((df[exposure_col]==exposure_val) & (df[outcome_col]==outcome_val)).sum()
    b = ((df[exposure_col]==exposure_val) & (df[outcome_col]!=outcome_val)).sum()
    c = ((df[exposure_col]!=exposure_val) & (df[outcome_col]==outcome_val)).sum()
    d = ((df[exposure_col]!=exposure_val) & (df[outcome_col]!=outcome_val)).sum()
    # odds ratio
    or_est = (a*d) / (b*c) if b*c>0 else None
    # risk ratio
    risk_exposed = a / (a+b) if (a+b)>0 else None
    risk_unexposed = c / (c+d) if (c+d)>0 else None
    rr = None if (risk_exposed is None or risk_unexposed is None or risk_unexposed==0) else risk_exposed / risk_unexposed
    return {"a": a, "b": b, "c": c, "d": d, "odds_ratio": or_est, "risk_ratio": rr}

def chi2_test(dataset_id, sheet_name, col1, col2, correction=True):
    df = read_sheet(dataset_id, sheet_name)
    table = pd.crosstab(df[col1], df[col2])
    stat, p, dof, expected = stats.chi2_contingency(table, correction=correction)
    return {"chi2": float(stat), "pvalue": float(p), "dof": int(dof), "expected": expected.tolist(), "table": table.to_dict()}

def t_test(dataset_id, sheet_name, group_col, value_col, group1, group2):
    df = read_sheet(dataset_id, sheet_name)
    g1 = df[df[group_col]==group1][value_col].dropna()
    g2 = df[df[group_col]==group2][value_col].dropna()
    t_stat, p = stats.ttest_ind(g1, g2, equal_var=False)
    return {"t_stat": float(t_stat), "pvalue": float(p), "mean1": g1.mean(), "mean2": g2.mean()}

def plot_dataset(dataset_id, sheet_name, kind="hist", x=None, y=None, options=None):
    df = read_sheet(dataset_id, sheet_name)
    fig = plt.figure()
    if kind=="hist":
        df[x].dropna().hist()
    elif kind=="scatter":
        df.plot.scatter(x=x, y=y)
    out_path = DATA_DIR / f"{dataset_id}_{uuid.uuid4().hex}.png"
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)
    return {"plot_path": str(out_path)}

