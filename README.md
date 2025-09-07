# MCP Epidemiology Server

This repository contains a local MCP server for performing basic epidemiological and statistical operations.  

The server exposes tools for:

- Uploading Excel datasets
    
- Describing datasets (shape, missing values, dtypes, summary stats)
    
- Computing epidemiological measures (proportion, odds ratio, risk ratio)
    
- Statistical tests (Chi-square, t-test)
    
- Generating plots (histogram, scatter, …)
    

---

## Requirements

- Python **3.12**
    
- pip dependencies (see `requirements.txt`)
    
- (Optional) Docker
    

---

## Installation

Clone the repository:

```bash
git clone https://github.com/G2309/Redes_proyecto.git
cd Redes_proyecto
```

Install dependencies (if server runs natively):

```bash
pip install -r requirements.txt
```

---

## Running the server

### Option 1: Run natively with Python

```bash
python server/server.py
```

The server will start at [http://localhost:8080](http://localhost:8080).

### Option 2: Run with Docker

```bash
docker buildx build -t mcp-epidemiology .
docker run -it --rm -p 8080:8080 mcp-epidemiology
```

---

## MCP Server Specification

- **Server name:** `Epidemiologia`
    
- **Protocol:** JSON-RPC over HTTP (via FastMCP)
    
- **Port:** `8080`
    

### Available Tools

#### 1. `upload_excel(file_bytes: bytes, filename: str) -> str`

Upload an Excel dataset.  
Returns a dataset ID.

#### 2. `list_datasets() -> list`

List available datasets.

#### 3. `describe(dataset_id: str, sheet_name: str = None) -> dict`

Return dataset summary (shape, missing values, dtypes, stats).

#### 4. `proportion(dataset_id: str, sheet_name: str, numerator_filter: str, denominator_filter: str) -> dict`

Compute proportions based on query filters.

#### 5. `odds_ratio_rr(dataset_id, sheet_name, exposure_col, outcome_col, exposure_val, outcome_val) -> dict`

Compute Odds Ratio (OR) and Risk Ratio (RR).

#### 6. `chi_square(dataset_id, sheet_name, col1, col2, correction: bool = True) -> dict`

Perform a Chi-square test of independence.

#### 7. `ttest(dataset_id, sheet_name, group_col, value_col, group1, group2) -> dict`

Perform an independent two-sample t-test.

#### 8. `plot(dataset_id, sheet_name, kind: str, x: str = None, y: str = None, options: dict = None) -> dict`

Generate a plot (histogram or scatter).

---

## Example Usage

Example request (JSON-RPC):

```json
{
  "jsonrpc": "2.0",
  "method": "describe",
  "params": {
    "dataset_id": "123e4567-e89b-12d3-a456-426614174000"
  },
  "id": 1
}
```

Example response:

```json
{
  "jsonrpc": "2.0",
  "result": {
    "basic": {...},
    "missing": {"age": 2, "sex": 0},
    "shape": [100, 5],
    "dtypes": {"age": "int64", "sex": "object"}
  },
  "id": 1
}
```

---

## Project Structure

```
.
├── Dockerfile
├── requirements.txt
├── server
│   ├── server.py        # MCP server definition
│   ├── stats_tools.py   # Statistical/epidemiological functions
│   └── utils_io.py      # Dataset IO helpers
└── tests
    └── test_tools.py    # Basic tests (future feature :eyes:)
```

---

##  Notes

- Uploaded datasets are stored in `/data/uploads` (or mounted volume when using Docker).
    
- This repository is for the **first delivery** of the MCP project (local server).
    
