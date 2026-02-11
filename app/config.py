#app/config.py 

"""  
Added SHEET_NAME and HEADER_ROW constants
"""
from pathlib import Path 
from datetime import datetime 

# base directory (contained inside executable) 
BASE_DIR = Path(__file__).resolve().parent.parent 

DATA_DIR = BASE_DIR / "data" 
OUTPUT_DIR = BASE_DIR / "output" 
LOG_DIR = BASE_DIR / "logs" 

SHEET_NAME = "Report1" 
HEADER_ROW = 5 # Row 6 in Excel (zero-based index) 

for directory in (DATA_DIR, OUTPUT_DIR, LOG_DIR): 
    directory.mkdir(parents=True, exist_ok=True) 

#OUTPUT_FILENAME = f"exclude_properties_{datetime.today().strftime('%Y%m%d')}.csv"