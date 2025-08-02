#!/usr/bin/env python3
"""
Check and fix hamburger menu on ALL pages
"""

import os
import re
from pathlib import Path

def check_mobile_menu_elements(content):
    """Check if all required mobile menu elements exist"""
    issues = []
    
    # Check for hamburger button
    if 'id="mobile-menu-toggle"' not in content:
        issues.append("Missing mobile menu toggle button")
    
    # Check for mobile menu overlay
    if 'id="mobile-menu-overlay"' not in content:
        issues.append("Missing mobile menu overlay")
    
    # Check for close button
    if 'id="close-menu-button"' not in content:
        issues.append("Missing close menu button")
    
    # Check for mobile menu CSS
    if '.mobile-menu-overlay' not in content:
        issues.append("Missing mobile menu CSS")
    
    # Check for JavaScript functionality
    if 'mobileMenuToggle.addEventListener' not in content and 'mobile-menu-toggle' in content:
        issues.append("Missing mobile menu JavaScript")
    
    return issues

def has_proper_dom_ready_wrapper(content):
    """Check if mobile menu script is wrapped in DOMContentLoaded"""
    return 'Mobile menu functionality - wrapped in DOMContentLoaded' in content

def fix_mobile_menu(file_path):
    """Fix mobile menu issues in the file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fixes_made = []
    
    # Skip non-production files
    if 'wireframe' in file_path.lower() or 'example' in file_path.lower():
        return False, []
    
    # Check for issues
    issues = check_mobile_menu_elements(content)
    
    if not issues:
        # Check if needs DOM ready wrapper
        if not has_proper_dom_ready_wrapper(content) and 'mobileMenuToggle.addEventListener' in content:
            # Need to wrap in DOMContentLoaded
            pattern = r'// Mobile menu functionality\s*\n\s*const mobileMenuToggle = document\.getElementById.*?document\.addEventListener\([\'"]keydown[\'"].*?\}\);\s*\}\);'
            match = re.search(pattern, content, re.DOTALL)
            
            if match:
                old_code = match.group(0)
                # Extract just the inner code
                inner_code = old_code.replace('// Mobile menu functionality', '').strip()
                
                new_code = '''// Mobile menu functionality - wrapped in DOMContentLoaded to ensure elements exist
        document.addEventListener('DOMContentLoaded', function() {
            ''' + inner_code + '''
        });'''
                
                content = content.replace(old_code, new_code)
                fixes_made.append("Wrapped mobile menu in DOMContentLoaded")
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
    
    return len(fixes_made) > 0, fixes_made

def main():
    # Get ALL HTML files
    html_files = []
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and node_modules
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules' and d != 'assets']
        
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    html_files.sort()
    
    print(f"Checking hamburger menu functionality in {len(html_files)} HTML files...")
    print("=" * 80)
    
    # First, check for issues
    files_with_issues = []
    files_ok = []
    
    for file_path in html_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = check_mobile_menu_elements(content)
        
        if issues:
            files_with_issues.append((file_path, issues))
        else:
            # Check if wrapped properly
            if not has_proper_dom_ready_wrapper(content) and 'mobileMenuToggle' in content:
                files_with_issues.append((file_path, ["Mobile menu not wrapped in DOMContentLoaded"]))
            else:
                files_ok.append(file_path)
    
    # Report issues
    print("\n❌ Files with issues:")
    for file_path, issues in files_with_issues:
        print(f"\n{file_path}:")
        for issue in issues:
            print(f"  - {issue}")
    
    print(f"\n✅ Files OK: {len(files_ok)}")
    for file_path in files_ok:
        print(f"  {file_path}")
    
    # Now fix issues
    print("\n" + "=" * 80)
    print("\nAttempting to fix issues...")
    
    fixed_count = 0
    for file_path, issues in files_with_issues:
        fixed, fixes = fix_mobile_menu(file_path)
        if fixed:
            print(f"✅ Fixed {file_path}: {', '.join(fixes)}")
            fixed_count += 1
    
    print("\n" + "=" * 80)
    print(f"\nSummary:")
    print(f"- Total HTML files: {len(html_files)}")
    print(f"- Files already OK: {len(files_ok)}")
    print(f"- Files with issues: {len(files_with_issues)}")
    print(f"- Files fixed: {fixed_count}")
    
    # Re-check after fixes
    if fixed_count > 0:
        print("\nRe-checking after fixes...")
        still_have_issues = []
        
        for file_path, _ in files_with_issues:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            issues = check_mobile_menu_elements(content)
            if issues:
                still_have_issues.append((file_path, issues))
        
        if still_have_issues:
            print(f"\n❌ {len(still_have_issues)} files still have issues:")
            for file_path, issues in still_have_issues:
                print(f"\n{file_path}:")
                for issue in issues:
                    print(f"  - {issue}")
        else:
            print("\n✅ All issues have been resolved!")

if __name__ == "__main__":
    main()