# Django Project Scrubber

A powerful tool to analyze Django projects for unused components, helping you keep your codebase clean and maintainable.

## Features

- Identifies potentially unused URLs
- Finds unused methods (coming soon)
- Detects duplicate method implementations (coming soon)
- Identifies unused templates (coming soon)

## Installation

```bash
pip install django-project-scrubber
```

## Usage

To analyze a Django project, run:

```bash
django_scrubber /path/to/your/django/project
```

The tool will analyze your project and display a summary of findings, including:
- Potentially unused URLs (excluding admin and auth URLs)
- Unused methods (coming in future versions)
- Duplicate method implementations (coming in future versions)
- Unused templates (coming in future versions)

## Example Output

```
Django Project Analysis Summary
==============================

Potentially Unused URLs:
- /api/v1/old-endpoint/
- /legacy/dashboard/
- /unused-feature/

Note: This is a static analysis and may have false positives.
Please verify these results before making any changes.
```

## How It Works

The Django Project Scrubber analyzes your Django project by:
1. Scanning all URL patterns in your project
2. Filtering out common false positives (admin, auth, etc.)
3. Providing a clear summary of potentially unused components

## Requirements

- Python 3.8 or higher
- Django 3.0 or higher

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

## Author

Your Name - [GitHub](https://github.com/yourusername)

## Project Status

This is the initial release (v0.1.0) with URL analysis functionality. More features are planned for future releases. 