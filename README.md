# Django Scrubber

A tool to analyze Django projects for unused components, helping you keep your codebase clean and maintainable.

## Features

- Identifies unused URLs
- Finds unused methods
- Detects duplicate method implementations
- Identifies unused templates

## Installation

```bash
pip install django-scrubber
```

## Usage

To analyze a Django project, run:

```bash
django-scrubber /path/to/your/django/project
```

The tool will analyze your project and display a summary of findings, including:
- Unused URLs
- Unused methods
- Duplicate method implementations
- Unused templates

## Example Output

```
Django Project Analysis Summary
==============================
Unused URLs:
- /api/v1/old-endpoint/
- /admin/legacy/

Unused Methods:
- views.old_view
- utils.deprecated_function

Duplicate Methods:
Similar implementations found in:
- views.py:process_data
- utils.py:handle_data

Unused Templates:
- templates/old_design/index.html
- templates/legacy/header.html
```

## Requirements

- Python 3.8 or higher
- Django 3.0 or higher

## License

MIT License 