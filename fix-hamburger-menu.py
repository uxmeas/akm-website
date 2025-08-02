#!/usr/bin/env python3
"""
Fix hamburger menu functionality on pages that are missing it
"""

import os
import re
from pathlib import Path

def fix_hamburger_menu(file_path):
    """Fix hamburger menu functionality in HTML file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip wireframe and example files
    if 'wireframe' in file_path or 'example' in file_path:
        return False
    
    # Check if already has proper mobile menu functionality
    has_toggle = 'mobileMenuToggle.addEventListener' in content and 'function closeMobileMenu()' in content
    
    if has_toggle:
        return False
    
    # Find where to insert the mobile menu script
    # Look for the closing script tag before </body>
    script_pattern = re.search(r'(</script>\s*)(</body>)', content, re.DOTALL)
    
    if not script_pattern:
        print(f"  ⚠️  Could not find proper script location in {file_path}")
        return False
    
    # Insert the mobile menu functionality
    mobile_menu_script = '''
        // Mobile menu functionality
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
        });'''
    
    # Insert the script before the last closing script tag
    insert_position = script_pattern.start(1)
    new_content = content[:insert_position] + mobile_menu_script + '\n    ' + content[insert_position:]
    
    # Write the updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    # List of files that need fixing based on the check
    files_to_fix = [
        './about.html',
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
    
    print("Fixing hamburger menu functionality...")
    print("=" * 80)
    
    fixed_count = 0
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            if fix_hamburger_menu(file_path):
                print(f"✅ Fixed: {file_path}")
                fixed_count += 1
            else:
                print(f"⏭️  Skipped: {file_path} (already has functionality)")
        else:
            print(f"❌ Not found: {file_path}")
    
    print("\n" + "=" * 80)
    print(f"\nFixed {fixed_count} files.")
    print("\nAll pages should now have working hamburger menu functionality!")

if __name__ == "__main__":
    main()