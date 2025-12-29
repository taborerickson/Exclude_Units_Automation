"""  
Exclude Units Automation Script (Public Version) 
------------------------------------------------
This script reads the most recent Excel report (stored locally), identifies
records requiring action based on date and unit-exclusion logic, and exports 
a clean, organized CSV output. All data referenced by the script remains local
and is not included in the repository. 

Excluded from the repo: 
- No proprietary data 
- No internal system names 
- No confidential business logic specifics 
"""

import pandas as pd 
import numpy as np 
from pathlib import Path 
from datetime import datetime, timedelta 
import sys 
import traceback  

# ------------------------------------------------------------------
# Setting Configurations 
# ------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent 
DATA_DIR = PROJECT_ROOT / "data" 
OUTPUT_DIR = PROJECT_ROOT / "output" 

SHEET_NAME = "Report1" 
HEADER_ROW = 5 # Row 6 in excel 

OUTPUT_FILENAME = f"exclude_properties_{datetime.today().strftime('%Y%m%d')}.csv"

# ------------------------------------------------------------------
# Adding helper functions 
# ------------------------------------------------------------------
# Finding the latest report (in case there are more than one ClosedPropertyAuditReport files present) 
def find_latest_report(data_dir: Path) -> Path: 
    """  
    Function to find the most recent ClosedPropertyAuditReport Excel file based on modified time/dates 
    """
    files = list(data_dir.glob("ClosedPropertyAuditReport*.xlsx")) 
    if not files: 
        raise FileNotFoundError("No ClosedPropertiesAuditReport Excel files found") 
    return max(files, key=lambda f: f.stat().st_mtime) 

# Error logging 
def log_error(message: str): 
    """   
    Adds a simple console error logging 
        Can be expanded to file logging later (if needed) 
    """
    print(f"[ERROR] {message}", file=sys.stderr) 

# ------------------------------------------------------------------
# Main process logic 
# ------------------------------------------------------------------
def main(): 
    try: 
        OUTPUT_DIR.mkdir(exist_ok=True) 
        # Finding the latest report 
        report_path = find_latest_report(DATA_DIR) 
        print(f"Using report: {report_path.name}") 
        # Loading the excel file (starting at the header row) 
        df = pd.read_excel(
            report_path, 
            sheet_name=SHEET_NAME, 
            header=HEADER_ROW 
        )
        # Selecting required columns (for output) 
        required_cols = [
            'Property', 
            'BU#', 
            'Mgmt End Date', 
            'Unit Count', 
            'Excluded' 
        ]
        # Check for missing columns 
        missing_cols = [c for c in required_cols if c not in df.columns] 
        if missing_cols: 
            raise ValueError(f"Missing required columns: {missing_cols}") 
        # Selecting only required columns 
        df = df[required_cols].copy() 

        # Preprocessing the report data 
        # Converting Mgmt End Date to datetime 
        df['Mgmt End Date'] = pd.to_datetime(df['Mgmt End Date'], errors='coerce') 
        # Converting Unit Count / Excluded to numeric 
        df['Unit Count'] = pd.to_numeric(df['Unit Count'], errors='coerce') 
        df['Excluded'] = pd.to_numeric(df['Excluded'], errors='coerce') 
        # Dropping rows with missing data in the calculation fields 
        df = df.dropna(subset=['Mgmt End Date', 'Unit Count', 'Excluded']) 

        # Main filtering logic 
        """  
        Filtering for properties that: 
            1.) Have been closed 30+ days 
            2.) Have units that are not excluded  
        """
        thirty_days_ago = datetime.today().date() - timedelta(days=30) 
        df['Incomplete'] = np.where(
            (df['Mgmt End Date'].dt.date <= thirty_days_ago) & 
            (df['Unit Count'] != df['Excluded']), 
            "X", 
            ""
        )
        # Filtering to select only incomplete properties 
        exclude_df = df[df['Incomplete'] == "X"].copy() 

        # Output 
        """  
        Output .csv file containing the properties needing to exclude units 
        """
        output_path = OUTPUT_DIR / OUTPUT_FILENAME 
        exclude_df.to_csv(output_path, index=False) 
        print(f"Output written to: {output_path}") 
        print(f"Total properties flagged: {len(exclude_df)}") 

    except Exception as e: 
        log_error("Script failed.") 
        log_error(str(e)) 
        traceback.print_exc()


if __name__ == "__main__": 
    main() 
