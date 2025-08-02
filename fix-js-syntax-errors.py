#!/usr/bin/env python3
"""
Fix JavaScript syntax errors (stray closing braces)
"""

import os
import re

def fix_stray_braces(file_path):
    """Remove stray closing braces after observer.observe"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to find and fix the stray braces
    # Look for observer.observe followed by two closing braces
    pattern = r'(observer\.observe\(document\.body, \{ childList: true, subtree: true \}\);\s*\n\s*)\}\s*\n\s*\}'
    
    # Check if pattern exists
    if re.search(pattern, content):
        # Replace with just one closing brace (remove the extra ones)
        content = re.sub(pattern, r'\1', content)
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    
    return False

def main():
    # List of files with syntax errors
    files_to_fix = [
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
    
    print("Fixing JavaScript syntax errors...")
    print("=" * 80)
    
    fixed_count = 0
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            if fix_stray_braces(file_path):
                print(f"✅ Fixed: {file_path}")
                fixed_count += 1
            else:
                print(f"⚠️  No match found in: {file_path}")
        else:
            print(f"❌ Not found: {file_path}")
    
    print("\n" + "=" * 80)
    print(f"\nFixed {fixed_count} files.")
    
    if fixed_count > 0:
        print("\n✅ JavaScript syntax errors have been fixed!")
        print("The hamburger menu should now work on all pages.")

if __name__ == "__main__":
    main()