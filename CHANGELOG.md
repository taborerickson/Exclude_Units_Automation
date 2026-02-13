# Changelog 

All notable changes to this project (after deployment) should be documented in this file. 

---

## [1.3.1] - 02-13-2026 

### Minor (Behavior) - Changed logging to persistent per-user storage & logging 
- Persisted runtime folders to per-user location when running a packaged executable:
  - `C:\Users\<username>\AppData\Local\ExcludeUnitsTool\logs`
  - `C:\Users\<username>\AppData\Local\ExcludeUnitsTool\data`
  - `C:\Users\<username>\AppData\Local\ExcludeUnitsTool\output`
- This change prevents transient temp-folder logging (PyInstaller `_MEI*` extraction) and ensures logs and output persist across runs for easier troubleshooting.
- In dev mode (running from source) the app retains the previous project-local `data/`, `output/`, and `logs/` locations.
- Startup now logs resolved runtime paths (visible in the first log entry) to make troubleshooting and support easier.

### Patch (Bugfixes & hardening) 
- Improved cleanup logic:
  - `data/` and `output/` contents are safely cleared at application exit (or startup) to avoid accumulation of files, while `logs/` are preserved.
  - Cleanup now handles nested directories and permission errors and logs any failures.
- Added a global unhandled-exception handler that:
  - Logs full tracebacks to the `logs/` directory.
  - Notifies users that an error occurred and where to find logs.
- Hardened file saving:
  - `save_uploaded_file()` ensures unique filenames (timestamp suffix) when duplicates are added/created.
  - Ensures `DATA_DIR` exists before copying.
- Minor logging improvements: startup path information is included in logs to locate files easier.

### Packaging / Release
- Rebuilt with updated packaging instructions to include README and enforce consistent behavior across different OS themes.
- Release name: `ExcludeUnitsTool_v1.3.1.exe`.

### Notes for Admins / Troubleshooting
- With this release, logs and outputs are located at `%LOCALAPPDATA%\ExcludeUnitsTool\`.
- When extracting logs, open:
  - `%LOCALAPPDATA%\ExcludeUnitsTool\logs` (Windows Run or Explorer)
- No user data is migrated between versions; persistent logs and outputs are retained across updates in the same folder (NOT deleted by upgrade).

---

## [1.2.0] - 02-12-2026

### UI Improvements 
- Enforced consistent dark theme styling across all user environments.
- Fixed text visibility issues caused by OS light/dark mode differences.
- Explicitly defined label, button, and table text colors to ensure readability.
- Standardized table header and grid styling for improved clarity.

### Enhanced Browse Button 
- Increased Browse button size for improved visibility.
- Updated font to bold for better readability.
- Improved hover and pressed state styling.

### Built-In Help / README Viewer 
- Added in-application Help dialog to display README documentation.
- Markdown is now rendered directly within the app (no browser extensions required).
- Eliminated dependency on external Markdown viewers.
- Added fallback handling if README file cannot be located.

### Packaging Improvements 
- Updated PyInstaller build configuration to bundle README with the executable.
- Cleaned release build process to ensure fresh packaging for each version.
- Improved cross-system UI consistency by enforcing explicit style rules.

---

## 1.1.0 - 02-11-2026 
Added: 
- Improved UI messaging and layout
- Better duplicate file handling 

Fixed: 
- QT Stylesheet syntax for QLabel  

--- 
