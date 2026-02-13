# Changelog 

All notable changes to this project (after deployment) should be documented in this file. 

---

## [1.2.0] - 02-12-2026

### UI Improvements 
- Enforced consistent dark theme styling across all user environments.
- Fixed text visibility issues caused by OS light/dark mode differences.
- Explicitly defined label, button, and table text colors to ensure readability.
- Standardized table header and grid styling for improved clarity.

### Enhanced Browse Button 
- Increased Browse button size for improved visibility.
- Updated font to bold for better prominence.
- Improved hover and pressed state styling for clearer user feedback.

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

