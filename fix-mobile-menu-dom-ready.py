#!/usr/bin/env python3
"""
Fix mobile menu functionality by ensuring DOM is ready
"""

import os
import re
from pathlib import Path

def fix_mobile_menu_dom_ready(file_path):
    """Wrap mobile menu functionality in DOMContentLoaded"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip wireframe and example files
    if 'wireframe' in file_path or 'example' in file_path:
        return False
    
    # Check if already wrapped in DOMContentLoaded
    if 'Mobile menu functionality - wrapped in DOMContentLoaded' in content:
        return False
    
    # Pattern to find the mobile menu functionality script
    pattern = r'(// Mobile menu functionality\s*\n\s*const mobileMenuToggle = document\.getElementById.*?document\.addEventListener\([\'"]keydown[\'"].*?\}\);\s*\}\);)'
    
    match = re.search(pattern, content, re.DOTALL)
    
    if match:
        old_code = match.group(1)
        
        # Extract the inner code (without the comment)
        inner_pattern = r'// Mobile menu functionality\s*\n(.*)'
        inner_match = re.search(inner_pattern, old_code, re.DOTALL)
        
        if inner_match:
            inner_code = inner_match.group(1)
            
            # Wrap in DOMContentLoaded and add null checks
            new_code = f'''// Mobile menu functionality - wrapped in DOMContentLoaded to ensure elements exist
        document.addEventListener('DOMContentLoaded', function() {{
            const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
            const mobileMenuOverlay = document.getElementById('mobile-menu-overlay');
            const closeMenuButton = document.getElementById('close-menu-button');
            
            // Mobile dropdown toggles
            const solutionsToggle = document.getElementById('solutions-mobile-toggle');
            const solutionsMenu = document.getElementById('solutions-mobile-menu');
            const industriesToggle = document.getElementById('industries-mobile-toggle');
            const industriesMenu = document.getElementById('industries-mobile-menu');

            // Ensure elements exist before adding listeners
            if (solutionsToggle && solutionsMenu) {{
                solutionsToggle.addEventListener('click', (e) => {{
                    e.preventDefault();
                    e.stopPropagation();
                    solutionsMenu.classList.toggle('hidden');
                    
                    // Find and rotate the icon (svg after Lucide processes it)
                    const icon = solutionsToggle.querySelector('svg');
                    if (icon) {{
                        icon.style.transform = solutionsMenu.classList.contains('hidden') ? 'rotate(0deg)' : 'rotate(45deg)';
                        icon.style.transition = 'transform 0.3s ease';
                    }}
                }});
            }}

            if (industriesToggle && industriesMenu) {{
                industriesToggle.addEventListener('click', (e) => {{
                    e.preventDefault();
                    e.stopPropagation();
                    industriesMenu.classList.toggle('hidden');
                    
                    // Find and rotate the icon (svg after Lucide processes it)
                    const icon = industriesToggle.querySelector('svg');
                    if (icon) {{
                        icon.style.transform = industriesMenu.classList.contains('hidden') ? 'rotate(0deg)' : 'rotate(45deg)';
                        icon.style.transition = 'transform 0.3s ease';
                    }}
                }});
            }}
            
            if (mobileMenuToggle && mobileMenuOverlay && closeMenuButton) {{
                mobileMenuToggle.addEventListener('click', function() {{
                    mobileMenuOverlay.classList.add('active');
                    document.body.style.overflow = 'hidden';
                }});
                
                function closeMobileMenu() {{
                    mobileMenuOverlay.classList.remove('active');
                    document.body.style.overflow = '';
                }}
                
                closeMenuButton.addEventListener('click', closeMobileMenu);
                
                mobileMenuOverlay.addEventListener('click', function(e) {{
                    if (e.target === mobileMenuOverlay) {{
                        closeMobileMenu();
                    }}
                }});
                
                document.addEventListener('keydown', function(e) {{
                    if (e.key === 'Escape' && mobileMenuOverlay.classList.contains('active')) {{
                        closeMobileMenu();
                    }}
                }});
            }}
        }});'''
            
            # Replace the old code with the new wrapped version
            content = content.replace(old_code, new_code)
            
            # Write the updated content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
    
    return False

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
    
    print("Fixing mobile menu DOM ready issues...")
    print("=" * 80)
    
    fixed_count = 0
    
    for file_path in html_files:
        if fix_mobile_menu_dom_ready(file_path):
            print(f"✅ Fixed: {file_path}")
            fixed_count += 1
    
    print("\n" + "=" * 80)
    print(f"\nFixed {fixed_count} files.")
    
    if fixed_count > 0:
        print("\nAll mobile menus should now work properly!")
    else:
        print("\nNo files needed fixing - all mobile menus are already properly wrapped.")

if __name__ == "__main__":
    main()