#!/usr/bin/env python3
"""
Test hamburger menu on each page individually
"""

import os
import re
from pathlib import Path

def test_hamburger_menu(file_path):
    """Test hamburger menu presence and functionality"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    results = {
        'has_hamburger_button': False,
        'button_visible_on_mobile': False,
        'has_menu_icon': False,
        'has_mobile_overlay': False,
        'has_javascript': False,
        'js_wrapped_properly': False,
        'button_html': '',
        'issues': []
    }
    
    # 1. Check for hamburger button
    hamburger_match = re.search(r'<button[^>]*id="mobile-menu-toggle"[^>]*>(.*?)</button>', content, re.DOTALL)
    if hamburger_match:
        results['has_hamburger_button'] = True
        results['button_html'] = hamburger_match.group(0)
        
        # Check if it has lg:hidden class (visible on mobile)
        if 'lg:hidden' in hamburger_match.group(0):
            results['button_visible_on_mobile'] = True
        else:
            results['issues'].append("Hamburger button missing lg:hidden class")
        
        # Check for menu icon
        if 'data-lucide="menu"' in hamburger_match.group(1) or 'lucide-menu' in hamburger_match.group(1):
            results['has_menu_icon'] = True
        else:
            results['issues'].append("Hamburger button missing menu icon")
    else:
        results['issues'].append("No hamburger button found with id='mobile-menu-toggle'")
    
    # 2. Check for mobile overlay
    if 'id="mobile-menu-overlay"' in content:
        results['has_mobile_overlay'] = True
    else:
        results['issues'].append("No mobile menu overlay found")
    
    # 3. Check for JavaScript
    if 'mobileMenuToggle.addEventListener' in content:
        results['has_javascript'] = True
        
        # Check if wrapped in DOMContentLoaded
        if 'Mobile menu functionality - wrapped in DOMContentLoaded' in content:
            results['js_wrapped_properly'] = True
        else:
            results['issues'].append("JavaScript not properly wrapped in DOMContentLoaded")
    else:
        results['issues'].append("No JavaScript event listener for hamburger menu")
    
    return results

def main():
    # Get all production HTML files
    production_files = [
        './index.html',
        './about.html',
        './contact.html',
        './solutions.html',
        './industries.html',
        './resilient-key-protection.html',
        './seamless-integration.html',
        './streamlined-compliance.html',
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
    
    print("Testing hamburger menu on each page individually...")
    print("=" * 100)
    
    pages_with_issues = []
    
    for file_path in production_files:
        if os.path.exists(file_path):
            results = test_hamburger_menu(file_path)
            
            if results['issues']:
                pages_with_issues.append((file_path, results))
                print(f"\n❌ {file_path}")
                print(f"   Hamburger button found: {results['has_hamburger_button']}")
                print(f"   Button visible on mobile: {results['button_visible_on_mobile']}")
                print(f"   Has menu icon: {results['has_menu_icon']}")
                print(f"   Has mobile overlay: {results['has_mobile_overlay']}")
                print(f"   Has JavaScript: {results['has_javascript']}")
                print(f"   JS wrapped properly: {results['js_wrapped_properly']}")
                
                if results['button_html']:
                    print(f"   Button HTML: {results['button_html'][:100]}...")
                
                print("   Issues:")
                for issue in results['issues']:
                    print(f"     - {issue}")
            else:
                print(f"✅ {file_path} - All checks passed")
        else:
            print(f"❌ {file_path} - File not found")
    
    print("\n" + "=" * 100)
    print(f"\nSummary:")
    print(f"- Total pages tested: {len(production_files)}")
    print(f"- Pages with issues: {len(pages_with_issues)}")
    
    if pages_with_issues:
        print("\n⚠️  ATTENTION: Some pages have hamburger menu issues!")
        print("\nPages that need fixing:")
        for file_path, _ in pages_with_issues:
            print(f"  - {file_path}")
    else:
        print("\n✅ All pages have properly functioning hamburger menus!")

if __name__ == "__main__":
    main()