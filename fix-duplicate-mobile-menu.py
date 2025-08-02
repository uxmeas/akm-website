#!/usr/bin/env python3
"""
Fix duplicate mobile menu functionality and ensure proper DOM ready wrapper
"""

import os
import re
from pathlib import Path

def fix_mobile_menu_duplicates(file_path):
    """Remove duplicate mobile menu code and ensure proper wrapping"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count occurrences of mobile menu functionality
    mobile_menu_count = content.count('// Mobile menu functionality')
    
    if mobile_menu_count <= 1:
        return False, "No duplicates found"
    
    # Find the incomplete mobile menu snippet (usually the first one)
    incomplete_pattern = r'// Mobile menu functionality\s*\n\s*const mobileMenuToggle = document\.getElementById\(\'mobile-menu-toggle\'\);\s*\n\s*const mobileMenuOverlay = document\.getElementById\(\'mobile-menu-overlay\'\);\s*\n\s*const closeMenuButton = document\.getElementById\(\'close-menu-button\'\);\s*\n\s*\n\s*\}'
    
    # Remove incomplete snippets
    content = re.sub(incomplete_pattern, '}', content)
    
    # Also remove any standalone incomplete mobile menu declarations
    standalone_pattern = r'// Mobile menu functionality\s*\n\s*const mobileMenuToggle = document\.getElementById\(\'mobile-menu-toggle\'\);\s*\n\s*const mobileMenuOverlay = document\.getElementById\(\'mobile-menu-overlay\'\);\s*\n\s*const closeMenuButton = document\.getElementById\(\'close-menu-button\'\);\s*\n\s*(?![\s]*//)'
    
    # Check if there's a complete implementation
    if 'mobileMenuToggle.addEventListener' in content:
        # Remove only the incomplete snippet
        content = re.sub(standalone_pattern, '', content)
    
    # Now ensure the remaining mobile menu is wrapped in DOMContentLoaded
    if 'Mobile menu functionality - wrapped in DOMContentLoaded' not in content:
        # Find the complete mobile menu implementation
        complete_pattern = r'(// Mobile menu functionality\s*\n\s*const mobileMenuToggle = document\.getElementById.*?document\.addEventListener\(\'keydown\'.*?\}\);\s*\}\);)'
        
        match = re.search(complete_pattern, content, re.DOTALL)
        
        if match:
            old_code = match.group(1)
            
            # Wrap it properly
            wrapped_code = '''// Mobile menu functionality - wrapped in DOMContentLoaded to ensure elements exist
        document.addEventListener('DOMContentLoaded', function() {
            const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
            const mobileMenuOverlay = document.getElementById('mobile-menu-overlay');
            const closeMenuButton = document.getElementById('close-menu-button');
            
            // Mobile dropdown toggles
            const solutionsToggle = document.getElementById('solutions-mobile-toggle');
            const solutionsMenu = document.getElementById('solutions-mobile-menu');
            const industriesToggle = document.getElementById('industries-mobile-toggle');
            const industriesMenu = document.getElementById('industries-mobile-menu');

            // Ensure elements exist before adding listeners
            if (solutionsToggle && solutionsMenu) {
                solutionsToggle.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    solutionsMenu.classList.toggle('hidden');
                    
                    // Find and rotate the icon (svg after Lucide processes it)
                    const icon = solutionsToggle.querySelector('svg');
                    if (icon) {
                        icon.style.transform = solutionsMenu.classList.contains('hidden') ? 'rotate(0deg)' : 'rotate(45deg)';
                        icon.style.transition = 'transform 0.3s ease';
                    }
                });
            }

            if (industriesToggle && industriesMenu) {
                industriesToggle.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    industriesMenu.classList.toggle('hidden');
                    
                    // Find and rotate the icon (svg after Lucide processes it)
                    const icon = industriesToggle.querySelector('svg');
                    if (icon) {
                        icon.style.transform = industriesMenu.classList.contains('hidden') ? 'rotate(0deg)' : 'rotate(45deg)';
                        icon.style.transition = 'transform 0.3s ease';
                    }
                });
            }
            
            if (mobileMenuToggle && mobileMenuOverlay && closeMenuButton) {
                mobileMenuToggle.addEventListener('click', function() {
                    mobileMenuOverlay.classList.add('active');
                    document.body.style.overflow = 'hidden';
                });
                
                function closeMobileMenu() {
                    mobileMenuOverlay.classList.remove('active');
                    document.body.style.overflow = '';
                }
                
                closeMenuButton.addEventListener('click', closeMobileMenu);
                
                mobileMenuOverlay.addEventListener('click', function(e) {
                    if (e.target === mobileMenuOverlay) {
                        closeMobileMenu();
                    }
                });
                
                document.addEventListener('keydown', function(e) {
                    if (e.key === 'Escape' && mobileMenuOverlay.classList.contains('active')) {
                        closeMobileMenu();
                    }
                });
            }
        });'''
            
            content = content.replace(old_code, wrapped_code)
    
    # Write back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True, "Fixed duplicates and wrapped in DOMContentLoaded"

def main():
    # Get all HTML files
    html_files = []
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and node_modules
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules' and d != 'assets']
        
        for file in files:
            if file.endswith('.html') and 'wireframe' not in file and 'example' not in file:
                html_files.append(os.path.join(root, file))
    
    html_files.sort()
    
    print("Fixing duplicate mobile menu code and ensuring DOM ready wrapper...")
    print("=" * 80)
    
    fixed_count = 0
    
    for file_path in html_files:
        fixed, message = fix_mobile_menu_duplicates(file_path)
        if fixed:
            print(f"✅ Fixed {file_path}: {message}")
            fixed_count += 1
    
    print("\n" + "=" * 80)
    print(f"\nFixed {fixed_count} files.")
    
    if fixed_count > 0:
        print("\nAll mobile menus should now work properly!")

if __name__ == "__main__":
    main()