<center> 

# **Exclude Units Automation Script** 

*Python-based automation script designed to process a structured Excel report, identify records that meet defined criteria, and export a clean CSV for downstream action.* <br>

*__This script automates filtering, calculation, and audit steps that were previously completed manually.__* <br> 

</center> 

---

## Features 

- Automatically detects and reads the most recent Excel report 
- Validates required columns and formatting
- Flags rows requiring downstream actions based on date and unit exclusion rules 
- Exports a clean, organized CSV to the '/output' directory
- Data remains local

---
## Requirements 
*__Can be imported manually or using 'requirements.txt' file__*

- Python 3.x 
- pandas 
- numpy
- pathlib 
- datetime 
- sys
- traceback

---
Installing dependencies: 
```bash 
pip install -r requirements.txt
```
---
Running the Script: 

Place Excel report inside: <br> 
```project_directory/data/```

Run the script: <br>
```python exclude_units.py```

The results will appear in: <br>
```project_directory/output/```

