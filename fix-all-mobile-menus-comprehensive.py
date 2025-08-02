#!/usr/bin/env python3
"""
Comprehensive fix for mobile menu on all pages
"""

import os
import re
from pathlib import Path

def wrap_mobile_menu_in_dom_ready(file_path):
    """Wrap mobile menu code in DOMContentLoaded"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already wrapped
    if 'Mobile menu functionality - wrapped in DOMContentLoaded' in content:
        return False
    
    # Find the mobile menu script that's not wrapped
    # Look for the pattern starting with "// Mobile menu functionality"
    pattern = r'(\s*// Mobile menu functionality\s*\n\s*const mobileMenuToggle[^}]+?if \(e\.key === \'Escape\'[^}]+?\}\s*\}\);\s*})'
    
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        old_code = match.group(1)
        indent = re.match(r'(\s*)', old_code).group(1)
        
        # Create the wrapped version
        new_code = f'''{indent}// Mobile menu functionality - wrapped in DOMContentLoaded to ensure elements exist
{indent}document.addEventListener('DOMContentLoaded', function() {{
{indent}    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
{indent}    const mobileMenuOverlay = document.getElementById('mobile-menu-overlay');
{indent}    const closeMenuButton = document.getElementById('close-menu-button');
{indent}    
{indent}    // Mobile dropdown toggles
{indent}    const solutionsToggle = document.getElementById('solutions-mobile-toggle');
{indent}    const solutionsMenu = document.getElementById('solutions-mobile-menu');
{indent}    const industriesToggle = document.getElementById('industries-mobile-toggle');
{indent}    const industriesMenu = document.getElementById('industries-mobile-menu');

{indent}    // Ensure elements exist before adding listeners
{indent}    if (solutionsToggle && solutionsMenu) {{
{indent}        solutionsToggle.addEventListener('click', (e) => {{
{indent}            e.preventDefault();
{indent}            e.stopPropagation();
{indent}            solutionsMenu.classList.toggle('hidden');
{indent}            
{indent}            // Find and rotate the icon (svg after Lucide processes it)
{indent}            const icon = solutionsToggle.querySelector('svg');
{indent}            if (icon) {{
{indent}                icon.style.transform = solutionsMenu.classList.contains('hidden') ? 'rotate(0deg)' : 'rotate(45deg)';
{indent}                icon.style.transition = 'transform 0.3s ease';
{indent}            }}
{indent}        }});
{indent}    }}

{indent}    if (industriesToggle && industriesMenu) {{
{indent}        industriesToggle.addEventListener('click', (e) => {{
{indent}            e.preventDefault();
{indent}            e.stopPropagation();
{indent}            industriesMenu.classList.toggle('hidden');
{indent}            
{indent}            // Find and rotate the icon (svg after Lucide processes it)
{indent}            const icon = industriesToggle.querySelector('svg');
{indent}            if (icon) {{
{indent}                icon.style.transform = industriesMenu.classList.contains('hidden') ? 'rotate(0deg)' : 'rotate(45deg)';
{indent}                icon.style.transition = 'transform 0.3s ease';
{indent}            }}
{indent}        }});
{indent}    }}
{indent}    
{indent}    if (mobileMenuToggle && mobileMenuOverlay && closeMenuButton) {{
{indent}        mobileMenuToggle.addEventListener('click', function() {{
{indent}            mobileMenuOverlay.classList.add('active');
{indent}            document.body.style.overflow = 'hidden';
{indent}        }});
{indent}        
{indent}        function closeMobileMenu() {{
{indent}            mobileMenuOverlay.classList.remove('active');
{indent}            document.body.style.overflow = '';
{indent}        }}
{indent}        
{indent}        closeMenuButton.addEventListener('click', closeMobileMenu);
{indent}        
{indent}        mobileMenuOverlay.addEventListener('click', function(e) {{
{indent}            if (e.target === mobileMenuOverlay) {{
{indent}                closeMobileMenu();
{indent}            }}
{indent}        }});
{indent}        
{indent}        document.addEventListener('keydown', function(e) {{
{indent}            if (e.key === 'Escape' && mobileMenuOverlay.classList.contains('active')) {{
{indent}                closeMobileMenu();
{indent}            }}
{indent}        }});
{indent}    }}
{indent}}});'''
        
        # Replace the old code with the new wrapped version
        content = content.replace(old_code, new_code)
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    
    return False

def main():
    # List of files that need fixing
    files_to_fix = [
        './contact.html',
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
    
    print("Fixing mobile menu DOM ready wrapper on all pages...")
    print("=" * 80)
    
    fixed_count = 0
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            if wrap_mobile_menu_in_dom_ready(file_path):
                print(f"✅ Fixed: {file_path}")
                fixed_count += 1
            else:
                print(f"⏭️  Skipped: {file_path} (already fixed or no match found)")
        else:
            print(f"❌ Not found: {file_path}")
    
    print("\n" + "=" * 80)
    print(f"\nFixed {fixed_count} files.")
    
    if fixed_count > 0:
        print("\nAll pages should now have properly working hamburger menus!")

if __name__ == "__main__":
    main()