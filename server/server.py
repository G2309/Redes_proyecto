from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp import run_server  
from stats_tools import (
    upload_excel_bytes,
    describe_dataset,
    compute_proportion,
    compute_or_rr,
    chi2_test,
    t_test,
    plot_dataset
)

mcp = FastMCP("MCP-Estadistico")

@mcp.tool()
def upload_excel(file_bytes: bytes, filename: str) -> str:
    return upload_excel_bytes(file_bytes, filename)

@mcp.tool()
def list_datasets() -> list:
    return mcp.state.get("datasets", [])

@mcp.tool()
def describe(dataset_id: str, sheet_name: str = None) -> dict:
    return describe_dataset(dataset_id, sheet_name=sheet_name)

@mcp.tool()
def proportion(dataset_id: str, sheet_name: str, numerator_filter: str, denominator_filter: str) -> dict:
    return compute_proportion(dataset_id, sheet_name, numerator_filter, denominator_filter)

@mcp.tool()
def odds_ratio_rr(dataset_id: str, sheet_name: str, exposure_col: str, outcome_col: str, exposure_val, outcome_val) -> dict:
    return compute_or_rr(dataset_id, sheet_name, exposure_col, outcome_col, exposure_val, outcome_val)

@mcp.tool()
def chi_square(dataset_id: str, sheet_name: str, col1: str, col2: str, correction: bool = True) -> dict:
    return chi2_test(dataset_id, sheet_name, col1, col2, correction=correction)

@mcp.tool()
def ttest(dataset_id: str, sheet_name: str, group_col: str, value_col: str, group1, group2) -> dict:
    return t_test(dataset_id, sheet_name, group_col, value_col, group1, group2)

@mcp.tool()
def plot(dataset_id: str, sheet_name: str, kind: str, x: str = None, y: str = None, options: dict = None) -> dict:
    return plot_dataset(dataset_id, sheet_name, kind=kind, x=x, y=y, options=options)


run_server(mcp, transport="streamable_http", host="0.0.0.0", port=8080)

