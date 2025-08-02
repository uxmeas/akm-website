#!/usr/bin/env python3
"""
Check hamburger menu functionality on all pages
"""

import os
import re
from pathlib import Path

def check_hamburger_menu(file_path):
    """Check if hamburger menu functionality is properly implemented"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # Check for hamburger menu button
    if 'id="mobile-menu-toggle"' not in content:
        issues.append("Missing mobile menu toggle button with id='mobile-menu-toggle'")
    
    # Check for mobile menu overlay
    if 'id="mobile-menu-overlay"' not in content:
        issues.append("Missing mobile menu overlay with id='mobile-menu-overlay'")
    
    # Check for close button
    if 'id="close-menu-button"' not in content:
        issues.append("Missing close menu button with id='close-menu-button'")
    
    # Check for event listener on mobile-menu-toggle
    mobile_toggle_listener = re.search(
        r"mobileMenuToggle\.addEventListener\s*\(\s*['\"]click['\"].*?mobileMenuOverlay\.classList\.add\s*\(\s*['\"]active['\"]",
        content,
        re.DOTALL
    )
    if not mobile_toggle_listener:
        issues.append("Missing or incorrect event listener for mobile menu toggle")
    
    # Check for closeMobileMenu function
    if "function closeMobileMenu()" not in content:
        issues.append("Missing closeMobileMenu function")
    
    # Check for event listener on close button
    close_button_listener = re.search(
        r"closeMenuButton\.addEventListener\s*\(\s*['\"]click['\"].*?closeMobileMenu",
        content,
        re.DOTALL
    )
    if not close_button_listener:
        issues.append("Missing event listener for close menu button")
    
    # Check for mobile-menu-overlay CSS styles
    if ".mobile-menu-overlay" not in content or "transform: translateX(-100%)" not in content:
        issues.append("Missing or incorrect mobile menu overlay CSS styles")
    
    # Check for active state CSS
    if ".mobile-menu-overlay.active" not in content or "transform: translateX(0)" not in content:
        issues.append("Missing or incorrect active state CSS for mobile menu")
    
    return issues

def main():
    # Get all HTML files
    html_files = []
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and node_modules
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
        
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    html_files.sort()
    
    print(f"Checking hamburger menu functionality in {len(html_files)} HTML files...")
    print("=" * 80)
    
    all_good = True
    files_with_issues = 0
    
    for file_path in html_files:
        issues = check_hamburger_menu(file_path)
        
        if issues:
            all_good = False
            files_with_issues += 1
            print(f"\n❌ {file_path}")
            for issue in issues:
                print(f"   - {issue}")
        else:
            print(f"✅ {file_path} - Hamburger menu properly implemented")
    
    print("\n" + "=" * 80)
    print(f"\nSummary:")
    print(f"- Total files checked: {len(html_files)}")
    print(f"- Files with proper hamburger menu: {len(html_files) - files_with_issues}")
    print(f"- Files with issues: {files_with_issues}")
    
    if all_good:
        print("\n✅ All pages have properly functioning hamburger menu!")
    else:
        print("\n❌ Some pages have issues with hamburger menu functionality.")
        print("\nTo fix these issues:")
        print("1. Ensure all pages have the mobile menu toggle button with id='mobile-menu-toggle'")
        print("2. Ensure all pages have the mobile menu overlay with id='mobile-menu-overlay'")
        print("3. Ensure all pages have proper event listeners for opening/closing the menu")
        print("4. Ensure all pages have the correct CSS styles for menu animation")

if __name__ == "__main__":
    main()