# Dumont

Excel file generation tool with data sheets and pivot tables.

## Installation

```bash
pip install dumont

# Or install with xlwings support
pip install dumont[xlwings]
```

## CLI Usage

### Generate Excel with sample data

```bash
dumont generate -o sales_report.xlsx
```

### Generate from CSV/Excel input

```bash
dumont generate -i data.csv -o report.xlsx
```

### Customize pivot table

```bash
dumont generate -o report.xlsx \
    --pivot-values Revenue \
    --pivot-index Category \
    --pivot-columns Region \
    --aggfunc sum
```

### Use xlwings engine (requires Excel installed)

```bash
dumont generate -o report.xlsx --engine xlwings
```

### Preview sample data

```bash
dumont sample --rows 20
```

### Preview Excel file contents

```bash
dumont preview report.xlsx --sheet Data --rows 10
```

### Get file information

```bash
dumont info report.xlsx
```

## Python API Usage

```python
from dumont import create_excel_with_pivot, generate_sample_data
import pandas as pd

# Generate with sample data
create_excel_with_pivot(
    output_path="report.xlsx",
    use_sample_data=True,
    sample_rows=200,
)

# Use your own DataFrame
df = pd.read_csv("my_data.csv")
create_excel_with_pivot(
    output_path="report.xlsx",
    df=df,
    pivot_values="Sales",
    pivot_index="Product",
    pivot_columns="Quarter",
    pivot_aggfunc="sum",
)

# Use xlwings for native Excel features
from dumont import create_excel_with_xlwings

create_excel_with_xlwings(
    output_path="report.xlsx",
    use_sample_data=True,
    visible=True,  # Show Excel during creation
)
```

## Output Structure

The generated Excel file contains:

1. **Data Sheet**: Raw data with auto-fitted columns
2. **Pivot Sheet**: Pivot table summarizing the data with margins/totals

## Requirements

- Python 3.8+
- pandas
- xlsxwriter
- click
- openpyxl
- xlwings (optional, for advanced Excel features)
