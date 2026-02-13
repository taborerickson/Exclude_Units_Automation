#app/config.py 

"""  
Added SHEET_NAME and HEADER_ROW constants
"""
from pathlib import Path 
from datetime import datetime 
import os 
import sys 

# Adding an app name (no versions) so upgrades use the same folder 
APP_NAME = "ExcludeUnitsTool" 

# Base directory 
PROJECT_ROOT = Path(__file__).resolve().parent.parent 

# Detecting if running as frozen exe 
IS_FROZEN = getattr(sys, "frozen", False) 
LOCAL_APPDATA = Path(os.getenv("LOCALAPPDATA", "")) if os.getenv("LOCALAPPDATA") else None 
if IS_FROZEN and LOCAL_APPDATA: 
    # Using consistent app folder (per user) for logs 
    USER_BASE = LOCAL_APPDATA / APP_NAME 
    BASE_DIR = USER_BASE 
else: 
    BASE_DIR = PROJECT_ROOT  

DATA_DIR = BASE_DIR / "data" 
OUTPUT_DIR = BASE_DIR / "output" 
LOG_DIR = BASE_DIR / "logs" 

SHEET_NAME = "Report1" 
HEADER_ROW = 5 # Row 6 in Excel (zero-based index) 

# Making sure directories exists 
for directory in (DATA_DIR, OUTPUT_DIR, LOG_DIR): 
    try: 
        directory.mkdir(parents=True, exist_ok=True) 
    except Exception: 
        # Fallback to project-local (if creation fails) 
        fallback = PROJECT_ROOT / "logs"
        fallback.mkdir(parents=True, exist_ok=True) 
        LOG_DIR = fallback 

# Adding usefule values for logging/inspections 
def info_paths(): 
    return {
        "is_frozen": IS_FROZEN, 
        "project_root": str(PROJECT_ROOT), 
        "base_dir": str(BASE_DIR), 
        "data_dir": str(DATA_DIR), 
        "output_dir": str(OUTPUT_DIR),
        "log_dir": str(LOG_DIR),  
    }

#OUTPUT_FILENAME = f"exclude_properties_{datetime.today().strftime('%Y%m%d')}.csv"