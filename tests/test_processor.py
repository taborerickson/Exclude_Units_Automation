#tests/test_processor.py

import pandas as pd 
import numpy as np 
from pathlib import Path 
from app.core.processor import process_report 
from app.config import HEADER_ROW 
import pytest 

def make_test_excel(path: Path, rows=5, flagged_rows=2): 
    """  
    Creates a synthetic ClosedPropertyAuditReport-like Excel file. 
    - rows: total rows 
    - flagged_rows: number of rows that should be flagged by the business rule
    """
    today = pd.Timestamp.today().normalize() 
    # Creating Mgmt End Dates: first 'flagged_rows' are old dates (today - 40 days) 
        # Rest are recent (today - 10 days) 
    dates = [today - pd.Timedelta(days=40)] * flagged_rows + [today - pd.Timedelta(days=10)] * (rows - flagged_rows)
    # Building DataFrame columns expected 
    data = pd.DataFrame({
        "Property": [f"P{i}" for i in range(rows)], 
        "BU#": [f"BU{i}" for i in range(rows)], 
        "Mgmt End Date": dates, 
        "Unit Count": [10] * rows, 
        # For flagged rows, setting Excluded < Unit Count to create a difference 
        "Excluded": [5 if i < flagged_rows else 10 for i in range(rows)]
    })
    # Writing to Excel with sheet name matching config.SHEET_NAME (Report1) 
    with pd.ExcelWriter(path, engine='openpyxl') as writer: 
        data.to_excel(writer, sheet_name='Report1', index=False, startrow=HEADER_ROW)
    #data.to_excel(path, sheet_name="Report1", index=False) 

def test_process_report_flags_correct_rows(tmp_path): 
    # Creating synthetic Excel file 
    excel_path = tmp_path / "ClosedPropertyAuditReport_test.xlsx" 
    make_test_excel(excel_path, rows=6, flagged_rows=2) 
    # Output path 
    out_csv = tmp_path / "out.csv" 
    # Running processor 
    result = process_report(excel_path, out_csv) 
    # Verifying result dictionary 
    assert "flagged_rows" in result 
    assert result["flagged_rows"] == 2 
    # Output csv should exist 
    assert out_csv.exists() 
    # Reading csv and verifying flagged rows count 
    out_df = pd.read_csv(out_csv) 
    assert len(out_df) == 2 
    # The "Incomplete" should be present and equal to "X" for all rows 
    assert 'Incomplete' in out_df.columns 
    assert out_df['Incomplete'].eq('X').all() 