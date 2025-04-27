# mypackage/mypackage.py
def greet(name):
    return f"Hello, {name}!"

import os
import ast
import sys
from collections import defaultdict
from pathlib import Path
import django
from django.conf import settings
from django.urls import get_resolver
from django.template.loader import get_template
from django.apps import apps
import click

class DjangoScrubber:
    def __init__(self, project_path):
        self.project_path = Path(project_path).resolve()
        self.unused_urls = []
        self.unused_methods = []
        self.duplicate_methods = []
        self.unused_templates = []
        self._configure_django()
        
    def _configure_django(self):
        """Configure Django settings for the project"""
        # Add project directory to Python path
        sys.path.insert(0, str(self.project_path))
        
        # Find the settings module
        project_name = None
        for item in self.project_path.iterdir():
            if item.is_dir() and not item.name.startswith('_'):
                if (item / 'settings.py').exists() and (item / 'urls.py').exists():
                    project_name = item.name
                    break
        
        if not project_name:
            raise click.ClickException("Could not find Django project settings")
            
        # Configure Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{project_name}.settings')
        django.setup()
        
    def analyze_project(self):
        """Main analysis function that runs all checks"""
        self._find_unused_urls()
        self._find_unused_methods()
        self._find_duplicate_methods()
        self._find_unused_templates()
        
    def _find_unused_urls(self):
        """Find URLs that are defined but never used"""
        resolver = get_resolver()
        all_urls = set()
        used_urls = set()
        
        def collect_urls(resolver, prefix=''):
            """Recursively collect URLs from the resolver"""
            for pattern in resolver.url_patterns:
                if hasattr(pattern, 'url_patterns'):
                    # This is an include() pattern
                    new_prefix = prefix
                    if pattern.pattern:
                        new_prefix = prefix + str(pattern.pattern)
                    collect_urls(pattern, new_prefix)
                else:
                    # This is a URL pattern
                    full_path = prefix + str(pattern.pattern)
                    # Skip admin URLs and authentication URLs
                    if not full_path.startswith(('admin/', 'auth/', 'login/', 'logout/')):
                        all_urls.add(full_path)
        
        collect_urls(resolver)
        
        # TODO: Implement URL usage tracking
        # This would require analyzing view imports and usage
        
        self.unused_urls = sorted(list(all_urls - used_urls))
    
    def _find_unused_methods(self):
        """Find methods that are defined but never used"""
        for app_config in apps.get_app_configs():
            app_path = app_config.path
            for root, _, files in os.walk(app_path):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                try:
                                    tree = ast.parse(f.read())
                                    for node in ast.walk(tree):
                                        if isinstance(node, ast.FunctionDef):
                                            # TODO: Implement method usage tracking
                                            # This would require analyzing imports and calls
                                            pass
                                except SyntaxError:
                                    continue
                        except UnicodeDecodeError:
                            # Skip files that can't be read with UTF-8
                            continue
    
    def _find_duplicate_methods(self):
        """Find methods with identical implementations"""
        method_hashes = defaultdict(list)
        
        for app_config in apps.get_app_configs():
            app_path = app_config.path
            for root, _, files in os.walk(app_path):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                try:
                                    tree = ast.parse(f.read())
                                    for node in ast.walk(tree):
                                        if isinstance(node, ast.FunctionDef):
                                            # TODO: Implement method comparison
                                            # This would require hashing method implementations
                                            pass
                                except SyntaxError:
                                    continue
                        except UnicodeDecodeError:
                            # Skip files that can't be read with UTF-8
                            continue
    
    def _find_unused_templates(self):
        """Find template files that are never used"""
        template_dirs = settings.TEMPLATES[0]['DIRS']
        all_templates = set()
        used_templates = set()
        
        # Get all template files
        for template_dir in template_dirs:
            for root, _, files in os.walk(template_dir):
                for file in files:
                    if file.endswith(('.html', '.txt')):
                        template_path = os.path.relpath(
                            os.path.join(root, file),
                            template_dir
                        )
                        all_templates.add(template_path)
        
        # TODO: Implement template usage tracking
        # This would require analyzing template inheritance and includes
        
        self.unused_templates = list(all_templates - used_templates)
    
    def get_summary(self):
        """Return a formatted summary of findings"""
        summary = []
        summary.append("Django Project Analysis Summary")
        summary.append("=" * 30)
        
        if self.unused_urls:
            summary.append("\nPotentially Unused URLs:")
            for url in self.unused_urls:
                summary.append(f"- /{url}")
        
        if self.unused_methods:
            summary.append("\nUnused Methods:")
            for method in self.unused_methods:
                summary.append(f"- {method}")
        
        if self.duplicate_methods:
            summary.append("\nDuplicate Methods:")
            for method_group in self.duplicate_methods:
                summary.append("Similar implementations found in:")
                for method in method_group:
                    summary.append(f"- {method}")
        
        if self.unused_templates:
            summary.append("\nUnused Templates:")
            for template in self.unused_templates:
                summary.append(f"- {template}")
                
        if not any([self.unused_urls, self.unused_methods, self.duplicate_methods, self.unused_templates]):
            summary.append("\nNo issues found! Your Django project looks clean.")
        else:
            summary.append("\nNote: This is a static analysis and may have false positives.")
            summary.append("Please verify these results before making any changes.")
        
        return "\n".join(summary)

@click.command()
@click.argument('project_path', type=click.Path(exists=True))
def main(project_path):
    """Analyze a Django project for unused components."""
    try:
        scrubber = DjangoScrubber(project_path)
        scrubber.analyze_project()
        print(scrubber.get_summary())
    except Exception as e:
        raise click.ClickException(str(e))

if __name__ == '__main__':
    main()