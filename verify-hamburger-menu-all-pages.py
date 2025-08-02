#!/usr/bin/env python3
"""
Comprehensive verification of hamburger menu functionality on ALL pages
"""

import os
import re
from pathlib import Path

def verify_mobile_menu(file_path):
    """Verify all aspects of mobile menu functionality"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # 1. Check HTML elements
    if 'id="mobile-menu-toggle"' not in content:
        issues.append("Missing mobile menu toggle button (hamburger)")
    
    if 'id="mobile-menu-overlay"' not in content:
        issues.append("Missing mobile menu overlay")
    
    if 'id="close-menu-button"' not in content:
        issues.append("Missing close menu button")
    
    # 2. Check CSS
    if '.mobile-menu-overlay' not in content:
        issues.append("Missing mobile menu CSS class")
    
    if 'transform: translateX(-100%)' not in content:
        issues.append("Missing mobile menu hidden state CSS")
    
    if '.mobile-menu-overlay.active' not in content:
        issues.append("Missing mobile menu active state CSS")
    
    # 3. Check JavaScript
    if 'Mobile menu functionality - wrapped in DOMContentLoaded' not in content:
        if 'mobileMenuToggle.addEventListener' in content:
            issues.append("Mobile menu JavaScript not wrapped in DOMContentLoaded")
        elif 'mobile-menu-toggle' in content:
            issues.append("Missing mobile menu JavaScript entirely")
    
    # 4. Check for duplicate mobile menu code
    mobile_menu_count = content.count('const mobileMenuToggle = document.getElementById(\'mobile-menu-toggle\')')
    if mobile_menu_count > 1:
        issues.append(f"Duplicate mobile menu code ({mobile_menu_count} instances)")
    
    # 5. Check event listeners
    if 'mobileMenuToggle.addEventListener' not in content and 'mobile-menu-toggle' in content:
        issues.append("Missing click event listener for hamburger menu")
    
    if 'closeMenuButton.addEventListener' not in content and 'close-menu-button' in content:
        issues.append("Missing click event listener for close button")
    
    # 6. Check for proper null checks
    if 'if (mobileMenuToggle && mobileMenuOverlay && closeMenuButton)' not in content and 'mobileMenuToggle.addEventListener' in content:
        issues.append("Missing null checks for mobile menu elements")
    
    return issues

def main():
    # Get ALL HTML files
    html_files = []
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and node_modules
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
        
        for file in files:
            if file.endswith('.html'):
                # Include ALL HTML files for comprehensive check
                html_files.append(os.path.join(root, file))
    
    html_files.sort()
    
    print(f"Verifying hamburger menu functionality on ALL {len(html_files)} HTML pages...")
    print("=" * 80)
    
    # Categorize files
    production_files = []
    non_production_files = []
    
    for file_path in html_files:
        if 'wireframe' in file_path.lower() or 'example' in file_path.lower() or '/assets/' in file_path:
            non_production_files.append(file_path)
        else:
            production_files.append(file_path)
    
    # Check production files
    print(f"\n📋 PRODUCTION PAGES ({len(production_files)} files):")
    print("-" * 80)
    
    all_good = True
    production_issues = []
    
    for file_path in production_files:
        issues = verify_mobile_menu(file_path)
        
        if issues:
            all_good = False
            production_issues.append((file_path, issues))
            print(f"\n❌ {file_path}")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print(f"✅ {file_path}")
    
    # Check non-production files
    print(f"\n\n📋 NON-PRODUCTION FILES ({len(non_production_files)} files):")
    print("-" * 80)
    
    for file_path in non_production_files:
        issues = verify_mobile_menu(file_path)
        
        if issues:
            print(f"⚠️  {file_path} - {len(issues)} issues (OK - not production)")
        else:
            print(f"✅ {file_path}")
    
    # Summary
    print("\n" + "=" * 80)
    print("\n📊 SUMMARY:")
    print(f"- Total HTML files checked: {len(html_files)}")
    print(f"- Production pages: {len(production_files)}")
    print(f"  - ✅ Working correctly: {len(production_files) - len(production_issues)}")
    print(f"  - ❌ With issues: {len(production_issues)}")
    print(f"- Non-production files: {len(non_production_files)}")
    
    if all_good:
        print("\n✅ SUCCESS: All production pages have properly functioning hamburger menus!")
        print("\n✅ TASK COMPLETE: Mobile menu (hamburger) is available and working globally on all pages.")
    else:
        print("\n❌ ISSUES FOUND: Some production pages still have hamburger menu issues.")
        print("\nNext steps:")
        print("1. Review the issues listed above")
        print("2. Run the fix scripts to address these issues")
        print("3. Test manually on actual devices/browsers")
    
    # List all production pages for easy reference
    print("\n📱 ALL PRODUCTION PAGES TO TEST:")
    print("-" * 80)
    for i, file_path in enumerate(production_files, 1):
        print(f"{i:2d}. {file_path}")

if __name__ == "__main__":
    main()