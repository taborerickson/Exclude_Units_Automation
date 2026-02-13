# Exclude Units — Admin & Deployment Guide

**Purpose:** This guide documents building, packaging, deploying, troubleshooting, and supporting the Exclude Units desktop application.

---

## Contents
- Overview
- Prerequisites
- Development & local testing
- Packaging (PyInstaller)
- Deployment models
- Admin support procedures
- Troubleshooting & logs
- Versioning and updates
- Security & governance

---

## 1. Overview
Exclude Units is a single-user desktop tool that:
- Accepts an exported Excel `ClosedPropertyAuditReport` (sheet `Report1`).
- Flags properties that are closed 30+ days and have units not fully excluded.
- Shows results inside a table and writes CSV output and logs.

### Runtime Folder Behavior (v1.3.0+)

In packaged (.exe) mode: 

Subfolders:

- `data/` — temporary uploaded reports (cleared on app exit)
- `output/` — generated CSV output (cleared on app exit)
- `logs/` — application logs (persist between runs)

In development mode (`python app/main.py`), these folders are created in the project root.

**Important**: End-users only receive the `.exe` and the user README. 
Admins keep the admin package with build artifacts and the admin README guide. 

---

## 2. Prerequisites (for admins / build machines)
- Windows build machine (matching target)
- Python 3.9+ installed
- A dedicated virtualenv for builds
- Tools:
  - `pip` 
  - `venv`
  - `pyinstaller`
  - `git` (for the source repo)

### Required Python Packages 
(recommended pinned versions in `requirements.txt`):
  - `pyside6`
  - `pandas`
  - `numpy`
  - `openpyxl`
  - `pytest`
  - `markdown` 

---

## Troubleshooting & Log File Access 
**Overview**
As of version 1.3.1 

### Log Location (Packaged .exe Mode) 
Logs are written to: 
```
LOCALAPPDATA%\ExcludeUnitsTool\logs
```
Expanded path example: 
```
C:\Users\JohnDoe\AppData\Local\ExcludeUnitsTool\logs
```

### How to Locate Logs: 
Using Run Dialog: 
1. Press **Windows** + **R**
2. Type: ```%LOCALAPPDATA%```
3. Press **Enter**
4. Open: `ExcludeUnitsTool`
5. Open: `logs`

### Crash Diagnostics Checklist
1. Confirm Version 
  - Verify the `.exe` name matches expected version (e.g., `v1.3.1`) 
  - Confirm `__version__` inside source 
2. Collect Log File 
  - Retrieve most recent `.txt` log file 
  - Confirm timestamps match crash time 
3. Check for: 
  - `ModuleNotFoundError`
  - `FileNotFoundError`
  - `PermissionError`
  - `Traceback` entries
  - Unhandled exceptions 
4. Confirm Input File
  - Was the correct Excel sheet (`Report1`) used? 
  - Is header row correct?
  - Is file corrupted?
5. Reproduce in Development Mode
  - Use same input file
  - Enable debug logging
6. Rebuild if Packaging Issue is Suspected
  - Common packaging failures: 
    - Missing hidden imports 
    - Missing `markdown`
    - Version mismatch 
    - Incomplete rebuild (old `build/` or `dist/` not cleared)

### Enabling Debug-Level Logging 
By default, logging level is typically `INFO`. 

Modify logger setup: 
```
import os
log_level = os.getenv("EXCLUDE_UNITS_LOG_LEVEL", "INFO") 
logging.basicConfig(level=log_level) 
```
Then launch via cmd: 
```
set EXCLUDE_UNITS_LOG_LEVEL=DEBUG
ExcludeUnitsTool_v1.3.1.exe
```
*(Enables debug logging without code modifications)*

### Versioning & Updates 

Versioning follows: 
```
MAJOR.MINOR.PATCH
```
Example: `1.3.1`
- MAJOR: Breaking changes
- MINOR: New features (e.g., LOCALAPPDATA logging) 
- PATCH: Bug fixes only 

**Release Checklist:**
- Update `__version__`
- Update `CHANGELOG.md`
- Delete old `build/` and `dist/` 
- Rebuild executable 
- Test logging location 
- Verify cleanup behavior 
- Confirm no missing modules 

---

## 4. Development & local testing (admin steps)

### Clone the Repository 

(cmd)
```
git clone <private_repo_url>
cd exclude-units 
```

### Create & Activate Virtual Environment 
```
python -m venv venv 
venv\Scripts\activate
pip install -r requirements.txt
```

### Run the Application in Development Mode 
```
python -m app.main
```
or 
```
python app/main.py
```
Expected Behavior: 
- `data/`, `output/`, and `logs/` folders are created in the project root
- Logs are written to: 
```
<project_root>/logs/
```
Verify Logging:
- Launch the app
- Load a test report 
- Close the application 
- Navigate to `logs/`
- Confirm a `.txt` log file exists and contains recent timestamps 

Verify Cleanup Behavior: 
- After closing the app: 
  - `data/` should be empty
  - `output/` should be empty
  - `logs/` should still contain log files 

### Packaging (PyInstaller) 
Create a separate virtual environment for the build 
```
python -m venv build_venv
build_venv\Scripts\activate
pip install -r requirements.txt
```
Confirm pathlib backport is not installed 
```
python -m pip uninstall pathlib
```
Install PyInstaller
```
pip install pyinstaller
```
Build command to package the application: 
```
pyinstaller --noconfirm --onefile --windowed --add-data "README.md;." --name ExcludeUnitsTool_v1.3.1 app/main.py
```
**(Replace `--name ExcludeUnitsTool_v1.3.1` with the version name (if updated))**

After building: 
```
dist/
└── ExcludeUnitsTool_v1.3.1.exe
```
Test the .exe before deployment. 


---

