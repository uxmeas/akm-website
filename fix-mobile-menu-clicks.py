#!/usr/bin/env python3
"""
Fix mobile menu submenu click functionality by ensuring event listeners
are attached after Lucide icons are created
"""

import re
import glob

def fix_mobile_menu_script(content):
    """Fix the mobile menu JavaScript to ensure submenus work properly"""
    
    # Find and replace the mobile menu script section
    # We need to move the mobile submenu event listeners inside the Lucide initialization callback
    
    old_pattern = r'''// Initialize Lucide icons with delay
        setTimeout\(\(\) => \{
            lucide\.createIcons\(\);
        \}, 100\);'''
    
    new_code = '''// Initialize Lucide icons with delay
        setTimeout(() => {
            lucide.createIcons();
            
            // Mobile dropdown toggles - moved here to ensure icons exist
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
                    
                    // Rotate the icon
                    const icon = solutionsToggle.querySelector('svg') || solutionsToggle;
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
                    
                    // Rotate the icon
                    const icon = industriesToggle.querySelector('svg') || industriesToggle;
                    if (icon) {
                        icon.style.transform = industriesMenu.classList.contains('hidden') ? 'rotate(0deg)' : 'rotate(45deg)';
                        icon.style.transition = 'transform 0.3s ease';
                    }
                });
            }
        }, 100);'''
    
    # Replace the old initialization code
    content = content.replace(old_pattern, new_code)
    
    # Remove the duplicate mobile toggle code that was added before
    # Pattern to find and remove the old mobile dropdown toggles section
    duplicate_pattern = r'''// Mobile dropdown toggles\s*\n\s*const solutionsToggle = document\.getElementById\('solutions-mobile-toggle'\);[\s\S]*?}\s*\n\s*}\s*\n'''
    
    content = re.sub(duplicate_pattern, '', content)
    
    return content

def process_html_file(filepath):
    """Process a single HTML file"""
    print(f"Processing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply fixes
    original_content = content
    content = fix_mobile_menu_script(content)
    
    # Only write if changes were made
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Fixed")
    else:
        print(f"  - No changes needed")

def main():
    print("Fixing mobile menu submenu click functionality...")
    print("")
    
    # Process all HTML files
    html_files = glob.glob("*.html")
    
    for html_file in html_files:
        if not html_file.endswith('.backup'):
            process_html_file(html_file)
    
    print("")
    print("Fix complete!")
    print("")
    print("The mobile menu submenus should now work properly:")
    print("- Event listeners are attached after icons are created")
    print("- Click events properly toggle the submenus")
    print("- Icons rotate when clicked")

if __name__ == "__main__":
    main()