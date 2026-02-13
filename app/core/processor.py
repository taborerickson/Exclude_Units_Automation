#app/core/processor.py 

"""  
Implements the exclude-units logic 
Expects an Excel input file path and output CSV path 
Returns: short user-friendly string summary and CSV to output_path 
"""

import pandas as pd 
import numpy as np 
from pathlib import Path 
from app.config import DATA_DIR, OUTPUT_DIR, SHEET_NAME, HEADER_ROW
from app.services.logger import setup_logger 
from datetime import datetime, timedelta 

logger = setup_logger() 

# Main exclude units logic 
def process_report(input_file: Path, output_path: Path = None): 
    """  
    Core logic: Existing logic from previous version

    Args: 
        input_file (Path or str): path to Excel report to process 
        output_path (Path or str): path for CSV output. If None, timestamped filename is used 
    
    Returns: 
        dict: {
            "output_path": Path or None, 
            "rows_flagged": int, 
            "message": str, 
            "preview": str (small text preview for UI)
        }

    Raises: 
        Various exceptions on read/validation errors which should be caught by caller
    """ 
    input_path = Path(input_file) 
    if not input_path.exists(): 
        raise FileNotFoundError(f"Input file not found: {input_path}") 
    
    # If no output path provided, creating timestamped CSV 
    if output_path is None: 
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") 
        output_path = OUTPUT_DIR / f"exclude_properties_{timestamp}.csv" 
    else: 
        output_path = Path(output_path) 

    logger.info(f"Processing report: {input_path.name}") 

    # Reading excel sheet 
    data = pd.read_excel(
        input_path, 
        sheet_name=SHEET_NAME, 
        header=HEADER_ROW, 
        engine='openpyxl'
    )
    logger.debug(f"Excel loaded. Shape: {data.shape}") 
    
    # Selecting required columns (for output) 
    required_cols = [
        'Property',
        'BU#', 
        'Mgmt End Date', 
        'Unit Count', 
        'Excluded'
    ]
    # Check for missing columns 
    missing_cols = [c for c in required_cols if c not in data.columns] 
    if missing_cols: 
        raise ValueError(f"Missing required columns: {missing_cols}") 
    
    # Keeping only required cols 
    data = data[required_cols].copy() 

    # Enforcing data types
    data['Mgmt End Date'] = pd.to_datetime(data['Mgmt End Date'], errors='coerce') 
    data['Unit Count'] = pd.to_numeric(data['Unit Count'], errors='coerce') 
    data['Excluded'] = pd.to_numeric(data['Excluded'], errors='coerce') 

    # Logging rows with invalid fields and dropping 
    before_drop = len(data) 
    data = data.dropna(subset=['Mgmt End Date','Unit Count','Excluded']) 
    dropped = before_drop - len(data) 
    if dropped: 
        logger.info(f"Dropped {dropped} rows due to invalid fields (Mgmt End Date/Unit Count/Excluded)") 
    
    # Filtering logic 
    # Closed 30+ days and has units that are not excluded 
    thirty_days_ago = pd.Timestamp.today().normalize() - timedelta(days=30) 
    data['Incomplete'] = np.where(
        (data['Mgmt End Date'] <= thirty_days_ago) & 
        (data['Unit Count'] != data['Excluded']), 
        "X", 
        ""
    )
    # Filtering to select only incomplete properties 
    exclude_df = data[data['Incomplete'] == "X"].copy() 
    flagged_count = len(exclude_df) 

    # If nothing found, writing empty CSV with headers 
    if flagged_count == 0: 
        data.head(0).to_csv(output_path, index=False) 
        msg = "No properties met unit exclusion criteria."
        logger.info(msg + f" Wrote empty CSV to: {output_path.name}") 
        preview = "No rows flagged." 
        return {
            "output_path": output_path, 
            "flagged_rows": 0, 
            "message": msg, 
            "preview": preview
        }
    # Writing results to CSV 
    exclude_df.to_csv(output_path, index=False) 
    msg = f"Processing complete. {flagged_count} properties flagged." 
    preview = exclude_df.head(20).to_string(index=False) # short preview for UI
    logger.info(msg + f" Wrote CSV: {output_path.name}") 
    return {
        "output_path": output_path, 
        "flagged_rows": flagged_count, 
        "message": msg, 
        "preview": preview
    }
