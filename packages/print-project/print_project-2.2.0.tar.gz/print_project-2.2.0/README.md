# Directory Content Analysis Tool

[![PyPI version](https://badge.fury.io/py/print-project.svg)](https://badge.fury.io/py/print-project)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)

A comprehensive Python utility for analyzing and extracting the contents of source code files across a project directory structure, outputting them into a single organized document for easier review and analysis.e

## Features

- **Recursive Directory Scanning**: Analyzes entire project structures including subdirectories
- **File Type Filtering**: Include/exclude files by extension or specific filenames
- **Smart Binary Detection**: Automatically skips binary files while allowing trusted text extensions
- **Project Structure Recovery**: Reconstructs complete project directories from analysis files
- **Directory Tree Generation**: Creates visual directory structure representation
- **Configurable Output**: Customizable output formatting with summary statistics
- **Size Limits**: Configurable maximum file size processing limits
- **Flexible Configuration**: INI-based configuration with command-line overrides

## Installation

### 🚀 Option 1: PyPI Installation (Recommended)

Install directly from PyPI - works on **any system** with Python:

```bash
pip install print-project
```

> **Latest Release**: v2.0.3 (October 2025) - [View on PyPI](https://pypi.org/project/print-project/)

**✅ After installation, use from any directory:**
```bash
print-project --help                    # Main command
analyze-project /path/to/project        # Alternative command
print-project --console -f ~/myproject  # Example usage
```

### 📦 Option 2: One-Line Installation Scripts

Install without cloning - alternative method for any system:

**Unix/Linux/macOS:**
```bash
curl -sSL https://raw.githubusercontent.com/smaxiso/print-project/master/scripts/install.sh | bash
```

**Windows (PowerShell):**
```powershell
iwr -useb https://raw.githubusercontent.com/smaxiso/print-project/master/scripts/install.ps1 | iex
```### 🔧 Option 3: Development Installation  

For development or latest features from source:

```bash
# Clone the repository
git clone https://github.com/smaxiso/print-project.git
cd print-project

# Install as Python package (creates 'print-project' and 'analyze-project' commands)
pip install -e .
```

### 🎯 Option 4: Guided Installation Script

For interactive setup with multiple installation options:

```bash
git clone https://github.com/smaxiso/print-project.git
cd print-project
python scripts/install.py
# Provides guided installation with choices for different setups
```

### 📁 Option 5: Direct Usage (No Installation)

Run directly without any installation:

```bash
git clone https://github.com/smaxiso/print-project.git
cd print-project
python print_project.py --help          # Works immediately
python print_project.py --console       # Example usage
```

### 📋 Requirements

- **Python 3.6+** (required)
- **chardet library** (automatically installed with pip methods)

### ✅ Verification

After installation, test that everything works:

```bash
# Test CLI commands (after pip install):
print-project --help
analyze-project --help

# Test basic functionality:
print-project --console --only-include-files "README.md"

# Test Python script (development):
python print_project.py --help
```

### 🔧 Cross-Platform Compatibility

This tool works identically on:
- ✅ **Windows** (tested)
- ✅ **macOS** (clone and `pip install -e .`)  
- ✅ **Linux** (clone and `pip install -e .`)

### 📂 Config File Search Locations

The tool automatically searches for `config.ini` in:
1. Current working directory
2. Script directory (for development)
3. Script directory `config/` subdirectory (organized structure)
4. `~/.print-project/config.ini` (user config)
5. `/etc/print-project/config.ini` (system config - Unix/Linux)
6. `%APPDATA%/print-project/config.ini` (system config - Windows)

## Usage

### Basic Usage

```bash
# CLI commands (after pip install or local install):
print-project                    # Analyze current directory
print-project -f /path/to/project # Analyze specific directory
print-project --console          # Show console output during processing

# Alternative command name:
analyze-project --help

# Direct Python script usage:
python print_project.py
python print_project.py -f /path/to/project
python print_project.py --console
```

### Advanced Options

```bash

The tool generates a `.txt` file containing:

1. **Directory Tree**: Visual representation of the project structure
2. **File Analysis**: Content of each processed file with:
   - File path and metadata
   - Line numbers
   - Syntax highlighting markers
3. **Summary Statistics**: 
   - Total files processed
   - Files skipped (with reasons)
   - Processing time and performance metrics

### 🔄 Project Reconstruction

Reverse engineer a project from the output text file. This automatically recreates the directory structure and files.

**Option 1: Unified Command (Recommended)**
```bash
# Reconstruct using the main tool
print-project --reconstruct output/myproject.txt

# Reconstruct to specific directory
print-project --reconstruct output/myproject.txt --output-dir ./workspace
```

**Option 2: Standalone Command**
```bash
# Reconstruct to ./project_name/ (default behavior)
reconstruct-project output/myproject.txt

# Reconstruct deep inside another directory
reconstruct-project output/myproject.txt --output-dir ./workspace

# Reconstruct flat (no project folder)
reconstruct-project output/myproject.txt --output-dir ./workspace --no-project-dir
```

**Option 3: Direct Script Usage**
```bash
python reconstruct_project.py output/myproject.txt
```

## Project Structure

```
print-project/
├── print_project.py           # Main application
├── reconstruct_project.py     # Reconstruction tool
├── config/
│   └── config.ini            # Default configuration
├── scripts/
│   ├── install.sh            # Unix/Linux installer
│   ├── install.ps1           # Windows installer
│   ├── install.py            # Interactive installer
│   └── release.sh            # Release automation
├── docs/
│   ├── CHANGELOG.md          # Version history
│   ├── CONTRIBUTING.md       # Development guidelines
│   ├── INSTALL.md            # Installation guide
│   └── PYPI_PUBLISHING.md    # Publishing guide
├── archive/                  # Previous versions
└── README.md                 # This file
```

## Use Cases

- **Code Reviews**: Generate comprehensive project snapshots
- **Documentation**: Create detailed project overviews
- **Analysis**: Understand project structure and content
- **Migration**: Prepare project content for analysis or transfer
- **AI/LLM Input**: Generate context-rich project representations

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](https://github.com/smaxiso/print-project/blob/master/docs/CONTRIBUTING.md) for detailed guidelines on:

- Setting up the development environment
- Code style and testing requirements
- Submitting bug reports and feature requests
- Pull request process and release guidelines

For version history and recent changes, see [CHANGELOG.md](https://github.com/smaxiso/print-project/blob/master/docs/CHANGELOG.md).

## License

This project is open source. See the repository for license details.