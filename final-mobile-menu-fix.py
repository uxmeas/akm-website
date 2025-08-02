#!/usr/bin/env python3
"""
Final comprehensive fix for mobile menu on all pages
"""

import os
import re
from pathlib import Path

def fix_mobile_menu_final(file_path):
    """Apply final comprehensive fix to mobile menu"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip non-production files
    if 'wireframe' in file_path.lower() or 'example' in file_path.lower():
        return False, "Skipped non-production file"
    
    # Check if already properly wrapped
    if 'Mobile menu functionality - wrapped in DOMContentLoaded' in content:
        return False, "Already properly wrapped"
    
    # Find the mobile menu code
    # Look for the pattern that starts with "// Mobile menu functionality"
    pattern = r'([\s]*// Mobile menu functionality[\s\S]*?)(\n\s*</script>)'
    
    match = re.search(pattern, content)
    
    if match:
        mobile_menu_code = match.group(1)
        closing_script = match.group(2)
        
        # Extract the indentation
        indent_match = re.match(r'(\s*)', mobile_menu_code)
        base_indent = indent_match.group(1) if indent_match else '        '
        
        # Create the properly wrapped version
        wrapped_code = f'''{base_indent}// Mobile menu functionality - wrapped in DOMContentLoaded to ensure elements exist
{base_indent}document.addEventListener('DOMContentLoaded', function() {{
{base_indent}    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
{base_indent}    const mobileMenuOverlay = document.getElementById('mobile-menu-overlay');
{base_indent}    const closeMenuButton = document.getElementById('close-menu-button');
{base_indent}    
{base_indent}    // Mobile dropdown toggles
{base_indent}    const solutionsToggle = document.getElementById('solutions-mobile-toggle');
{base_indent}    const solutionsMenu = document.getElementById('solutions-mobile-menu');
{base_indent}    const industriesToggle = document.getElementById('industries-mobile-toggle');
{base_indent}    const industriesMenu = document.getElementById('industries-mobile-menu');

{base_indent}    // Ensure elements exist before adding listeners
{base_indent}    if (solutionsToggle && solutionsMenu) {{
{base_indent}        solutionsToggle.addEventListener('click', (e) => {{
{base_indent}            e.preventDefault();
{base_indent}            e.stopPropagation();
{base_indent}            solutionsMenu.classList.toggle('hidden');
{base_indent}            
{base_indent}            // Find and rotate the icon (svg after Lucide processes it)
{base_indent}            const icon = solutionsToggle.querySelector('svg');
{base_indent}            if (icon) {{
{base_indent}                icon.style.transform = solutionsMenu.classList.contains('hidden') ? 'rotate(0deg)' : 'rotate(45deg)';
{base_indent}                icon.style.transition = 'transform 0.3s ease';
{base_indent}            }}
{base_indent}        }});
{base_indent}    }}

{base_indent}    if (industriesToggle && industriesMenu) {{
{base_indent}        industriesToggle.addEventListener('click', (e) => {{
{base_indent}            e.preventDefault();
{base_indent}            e.stopPropagation();
{base_indent}            industriesMenu.classList.toggle('hidden');
{base_indent}            
{base_indent}            // Find and rotate the icon (svg after Lucide processes it)
{base_indent}            const icon = industriesToggle.querySelector('svg');
{base_indent}            if (icon) {{
{base_indent}                icon.style.transform = industriesMenu.classList.contains('hidden') ? 'rotate(0deg)' : 'rotate(45deg)';
{base_indent}                icon.style.transition = 'transform 0.3s ease';
{base_indent}            }}
{base_indent}        }});
{base_indent}    }}
{base_indent}    
{base_indent}    if (mobileMenuToggle && mobileMenuOverlay && closeMenuButton) {{
{base_indent}        mobileMenuToggle.addEventListener('click', function() {{
{base_indent}            mobileMenuOverlay.classList.add('active');
{base_indent}            document.body.style.overflow = 'hidden';
{base_indent}        }});
{base_indent}        
{base_indent}        function closeMobileMenu() {{
{base_indent}            mobileMenuOverlay.classList.remove('active');
{base_indent}            document.body.style.overflow = '';
{base_indent}        }}
{base_indent}        
{base_indent}        closeMenuButton.addEventListener('click', closeMobileMenu);
{base_indent}        
{base_indent}        mobileMenuOverlay.addEventListener('click', function(e) {{
{base_indent}            if (e.target === mobileMenuOverlay) {{
{base_indent}                closeMobileMenu();
{base_indent}            }}
{base_indent}        }});
{base_indent}        
{base_indent}        document.addEventListener('keydown', function(e) {{
{base_indent}            if (e.key === 'Escape' && mobileMenuOverlay.classList.contains('active')) {{
{base_indent}                closeMobileMenu();
{base_indent}            }}
{base_indent}        }});
{base_indent}    }}
{base_indent}}});'''
        
        # Replace the entire mobile menu section
        new_content = content.replace(mobile_menu_code, wrapped_code)
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True, "Fixed and wrapped mobile menu"
    
    return False, "Could not find mobile menu code to fix"

def main():
    # List of files that need fixing based on verification
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
    
    print("Applying final mobile menu fix to all pages...")
    print("=" * 80)
    
    fixed_count = 0
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            fixed, message = fix_mobile_menu_final(file_path)
            if fixed:
                print(f"✅ Fixed: {file_path} - {message}")
                fixed_count += 1
            else:
                print(f"⏭️  Skipped: {file_path} - {message}")
        else:
            print(f"❌ Not found: {file_path}")
    
    print("\n" + "=" * 80)
    print(f"\nFixed {fixed_count} files.")
    
    if fixed_count > 0:
        print("\n✅ Mobile menu fixes applied. Running verification...")

if __name__ == "__main__":
    main()