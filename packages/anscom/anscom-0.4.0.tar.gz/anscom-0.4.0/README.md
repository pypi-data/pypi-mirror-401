# Anscom

**Anscom** is a high-performance, native C extension for Python that recursively scans directories and categorizes files with blazingly fast speed.

## Features
- **Native C Speed:** Written in pure C (C89 compliant).
- **Visual Tree:** Prints a diagrammatic folder tree in the terminal.
- **Detailed Analysis:** Breakdowns by category and specific file extensions.
- **Cross-Platform:** Works on Windows, Linux, and macOS.

## Installation
```bash
pip install anscom



Usage
code
Python
import anscom

# Scan the current directory
anscom.scan(".")

# Scan a specific path
anscom.scan("C:/Users/Documents")
code
Code
---

### Step 2: Create a `MANIFEST.in`
When you package C modules, Python needs to know exactly which source files to include. Create a file named `MANIFEST.in`:

```text
include *.c
include *.h
include LICENSE
include README.md
