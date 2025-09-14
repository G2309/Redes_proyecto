from fastmcp import FastMCP
import json
from pathlib import Path
from utils_io import get_available_datasets
from stats_tools import (
    upload_excel_bytes,
    describe_dataset,
    compute_proportion,
    compute_or_rr,
    chi2_test,
    t_test,
    plot_dataset
)

DATA_DIR = Path("/data/uploads")
mcp = FastMCP("MCP-Estadistico")

def _list_datasets_internal():
    return get_available_datasets()

@mcp.tool()
def upload_excel(file_bytes: bytes, filename: str) -> str:
    """Upload an Excel file and return a dataset ID"""
    try:
        return upload_excel_bytes(file_bytes, filename)
    except Exception as e:
        return f"Error uploading file: {str(e)}"

@mcp.tool()
def list_datasets() -> list:
    """List all available datasets"""
    datasets = _list_datasets_internal()
    if not datasets:
        print("No metadata found, scanning for files directly...")
    return datasets

@mcp.tool()
def describe(dataset_id: str, sheet_name: str = None) -> dict:
    """Describe a dataset's structure and statistics"""
    try:
        return describe_dataset(dataset_id, sheet_name=sheet_name)
    except FileNotFoundError as e:
        available = _list_datasets_internal()
        available_ids = [d.get('id', 'unknown') for d in available]
        return {
            "error": f"Dataset not found: {str(e)}",
            "available_datasets": available_ids,
            "hint": f"Try using one of these dataset IDs: {available_ids}"
        }

@mcp.tool()
def proportion(dataset_id: str, sheet_name: str, numerator_filter: str, denominator_filter: str) -> dict:
    """Compute proportions with filters"""
    try:
        return compute_proportion(dataset_id, sheet_name, numerator_filter, denominator_filter)
    except Exception as e:
        return {"error": f"Error computing proportion: {str(e)}"}

@mcp.tool()
def odds_ratio_rr(dataset_id: str, sheet_name: str, exposure_col: str, outcome_col: str, exposure_val, outcome_val) -> dict:
    """Compute odds ratio and risk ratio"""
    try:
        return compute_or_rr(dataset_id, sheet_name, exposure_col, outcome_col, exposure_val, outcome_val)
    except Exception as e:
        return {"error": f"Error computing OR/RR: {str(e)}"}

@mcp.tool()
def chi_square(dataset_id: str, sheet_name: str, col1: str, col2: str, correction: bool = True) -> dict:
    """Perform chi-square test"""
    try:
        return chi2_test(dataset_id, sheet_name, col1, col2, correction=correction)
    except Exception as e:
        return {"error": f"Error in chi-square test: {str(e)}"}

@mcp.tool()
def ttest(dataset_id: str, sheet_name: str, group_col: str, value_col: str, group1, group2) -> dict:
    """Perform t-test between two groups"""
    try:
        return t_test(dataset_id, sheet_name, group_col, value_col, group1, group2)
    except Exception as e:
        return {"error": f"Error in t-test: {str(e)}"}

@mcp.tool()
def plot(dataset_id: str, sheet_name: str, kind: str, x: str = None, y: str = None, options: dict = None) -> dict:
    """Create plots from dataset"""
    try:
        return plot_dataset(dataset_id, sheet_name, kind=kind, x=x, y=y, options=options)
    except Exception as e:
        return {"error": f"Error creating plot: {str(e)}"}

@mcp.tool()
def debug_info() -> dict:
    """Get debugging information about the server state"""
    info = {
        "data_dir": str(DATA_DIR),
        "data_dir_exists": DATA_DIR.exists(),
        "files_in_data_dir": [],
        "metadata_files": [],
        "dataset_files": []
    }
    
    if DATA_DIR.exists():
        for item in DATA_DIR.iterdir():
            info["files_in_data_dir"].append({
                "name": item.name,
                "is_file": item.is_file(),
                "size": item.stat().st_size if item.is_file() else None
            })
            
            if item.name.endswith('.meta.json'):
                info["metadata_files"].append(item.name)
            elif item.suffix.lower() in ('.xlsx', '.xls', '.csv'):
                info["dataset_files"].append({
                    "name": item.name,
                    "stem": item.stem,
                    "suffix": item.suffix
                })
    
    return info

if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8080)
