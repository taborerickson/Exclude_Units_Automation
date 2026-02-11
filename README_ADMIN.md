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

Runtime folders (created automatically relative to the executable):
- `data/` — temporary uploaded reports (cleared on app exit)
- `output/` — CSV outputs (cleared on app exit)
- `logs/` — app logs (persist between runs)

**Important**: End-users only get the `.exe` and the user README. Admins keep the admin package with build artifacts and the admin README

---

## 2. Prerequisites (for admins / build machines)
- Windows build machine (matching target)
- Python 3.9+ installed
- A dedicated virtualenv for builds
- Tools:
  - `pip`, `venv`
  - `pyinstaller`
  - `git` (for the source repo)
- Python packages (recommended pinned versions in `requirements.txt`):
  - `pyside6`
  - `pandas`
  - `numpy`
  - `openpyxl`
  - `pytest`

  ---

  ## 3. Development & local testing (admin steps)
1. `git clone` the private repo to your dev machine.
2. Create a virtualenv and activate:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt

---
