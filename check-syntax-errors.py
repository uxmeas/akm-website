#!/usr/bin/env python3
"""
Check for JavaScript syntax errors in HTML files
"""

import os
import re

def check_js_syntax(file_path):
    """Check for common JavaScript syntax errors"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # Check for stray closing braces after observer.observe
    pattern = r'observer\.observe\(document\.body[^;]+;\s*\n\s*}\s*\n\s*}'
    if re.search(pattern, content):
        issues.append("Stray closing brace '}' after observer.observe")
    
    # Check for incomplete script sections
    script_sections = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
    for i, script in enumerate(script_sections):
        open_braces = script.count('{')
        close_braces = script.count('}')
        if open_braces != close_braces:
            issues.append(f"Script section {i+1}: Mismatched braces ({open_braces} open, {close_braces} close)")
    
    return issues

def main():
    # Get all industry HTML files
    industry_files = [
        './industry-aerospace-defense.html',
        './industry-chemical-processing.html',
        './industry-energy-oil-gas.html',
        './industry-financial-services.html',
        './industry-government.html',
        './industry-manufacturing.html',
        './industry-mining.html',
        './industry-pharmaceuticals.html',
        './industry-transportation.html',
        './industry-utilities.html'
    ]
    
    print("Checking for JavaScript syntax errors...")
    print("=" * 80)
    
    files_with_errors = []
    
    for file_path in industry_files:
        if os.path.exists(file_path):
            issues = check_js_syntax(file_path)
            if issues:
                files_with_errors.append((file_path, issues))
                print(f"\n❌ {file_path}")
                for issue in issues:
                    print(f"   - {issue}")
        else:
            print(f"❌ {file_path} - File not found")
    
    print("\n" + "=" * 80)
    
    if files_with_errors:
        print(f"\n⚠️  Found syntax errors in {len(files_with_errors)} files!")
        return files_with_errors
    else:
        print("\n✅ No syntax errors found!")
        return []

if __name__ == "__main__":
    main()