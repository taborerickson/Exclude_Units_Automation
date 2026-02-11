# Exclude Units Task -- Quick User Guide

Automated Exclude Units Report Tool 
This desktop application helps you identify properties that have units that need to be excluded in Yardi by checking the management end dates and unit exclusions. 

## Quick Summary (What this tool does) 
- You drag-and-drop an exported Excel report (or click **Browse** to browse your computer directory). 
- The tool checks each property and flags those that: 
    - Have a management end date **30 or more days** earlier than today's date **and**
    - Have units that are **not excluded** (Unit Count ≠ Excluded).
- The tool populates the results inside the window (table preview) and saves a CSV file internally. 

## How to run (step-by-step) 
1. Find the `ExcludeUnitsTool.exe` icon (double-click to open the app). 
    - May have different naming depending on release version (`ExcludeUnitsTool_v1.1.0.exe`)
2. The window will open. You will see instructions at the top: 
    - Drag & drop the exported report file into the window **or** 
    - Click **Browse** to select the file from your computer. 
3. Drop or select the file (the tool accepts Excel files: `.xlsx`, `.xlsm`, or `.xls`). 
    - When exporting the file, it should already be exported as an Excel file
4. The tool will run; a small progress window will display while it works. 
5. When processing is finished: 
    - You will see a large success message. 
    - A table preview will show the flagged properties (up to 20). 
    - You can drage another file or click **Browse** to run another report. 
6. When you close the app, any temporary files used by the applciation (the report you dropped and the generated CSV) are deleted automatically. Log files remain for support. 

## What file should I use? 
- Use the exported report from Yardi. 
    - Should contain a sheet named **`Report1`** (this is the standard export format).
- Accepted formats: `.xlsx`, `.xlsm`, `.xls`.
- Do **not** upload sensitive or personal files beyond the intended report.

## Troubleshooting tips (end-user)
- If the app shows a friendly message like “An error occurred,” please:
  - Note the time you ran it and the filename used.
- If nothing happens when you drop a file:
  - Ensure the file is an Excel file (.xlsx) and not open in another application.
  - Try using the **Browse** button instead.



