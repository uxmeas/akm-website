#!/usr/bin/env python3
"""
Final fix for mobile menu submenu click functionality
Ensures the click targets the right element after Lucide icon conversion
"""

import re
import glob

def fix_mobile_menu_clicks(content):
    """Fix mobile menu to handle clicks on the parent div instead of the icon"""
    
    # First, update the HTML structure to make the entire div clickable
    # Pattern to find the mobile menu toggle divs
    solutions_pattern = r'(<div class="text-white text-xl font-medium py-2 flex items-center justify-between">\s*<span>Solutions</span>\s*<i data-lucide="plus" class="w-6 h-6" id="solutions-mobile-toggle"></i>\s*</div>)'
    
    solutions_replacement = '''<div class="text-white text-xl font-medium py-2 flex items-center justify-between cursor-pointer" id="solutions-mobile-toggle">
                        <span>Solutions</span>
                        <i data-lucide="plus" class="w-6 h-6"></i>
                    </div>'''
    
    content = re.sub(solutions_pattern, solutions_replacement, content, flags=re.DOTALL)
    
    # Same for industries
    industries_pattern = r'(<div class="text-white text-xl font-medium py-2 flex items-center justify-between">\s*<span>Industries</span>\s*<i data-lucide="plus" class="w-6 h-6" id="industries-mobile-toggle"></i>\s*</div>)'
    
    industries_replacement = '''<div class="text-white text-xl font-medium py-2 flex items-center justify-between cursor-pointer" id="industries-mobile-toggle">
                        <span>Industries</span>
                        <i data-lucide="plus" class="w-6 h-6"></i>
                    </div>'''
    
    content = re.sub(industries_pattern, industries_replacement, content, flags=re.DOTALL)
    
    # Now fix the JavaScript to properly handle the clicks
    # Find the mobile dropdown toggles section
    js_pattern = r'''// Ensure elements exist before adding listeners
        if \(solutionsToggle && solutionsMenu\) \{
            solutionsToggle\.addEventListener\('click', \(e\) => \{
                e\.preventDefault\(\);
                e\.stopPropagation\(\);
                solutionsMenu\.classList\.toggle\('hidden'\);
                solutionsToggle\.style\.transform = solutionsMenu\.classList\.contains\('hidden'\) \? 'rotate\(0deg\)' : 'rotate\(45deg\)';
                
                // Re-initialize Lucide icons
                setTimeout\(\(\) => \{
                    lucide\.createIcons\(\);
                \}, 100\);
            \}\);
        \}

        if \(industriesToggle && industriesMenu\) \{
            industriesToggle\.addEventListener\('click', \(e\) => \{
                e\.preventDefault\(\);
                e\.stopPropagation\(\);
                industriesMenu\.classList\.toggle\('hidden'\);
                industriesToggle\.style\.transform = industriesMenu\.classList\.contains\('hidden'\) \? 'rotate\(0deg\)' : 'rotate\(45deg\)';
                
                // Re-initialize Lucide icons
                setTimeout\(\(\) => \{
                    lucide\.createIcons\(\);
                \}, 100\);
            \}\);
        \}'''
    
    js_replacement = '''// Ensure elements exist before adding listeners
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
        }'''
    
    content = re.sub(js_pattern, js_replacement, content, flags=re.DOTALL)
    
    return content

def process_html_file(filepath):
    """Process a single HTML file"""
    print(f"Processing: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply fixes
        original_content = content
        content = fix_mobile_menu_clicks(content)
        
        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ Fixed")
        else:
            print(f"  - No changes needed")
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")

def main():
    print("Applying final fix for mobile menu submenu clicks...")
    print("")
    
    # Process all HTML files
    html_files = glob.glob("*.html")
    
    for html_file in html_files:
        if not html_file.endswith('.backup'):
            process_html_file(html_file)
    
    print("")
    print("Final fix complete!")
    print("")
    print("Changes made:")
    print("1. Moved ID to parent div (entire row is clickable)")
    print("2. Added cursor-pointer class for better UX")
    print("3. JavaScript now finds and rotates the SVG icon")
    print("4. Removed dependency on icon element having the ID")

if __name__ == "__main__":
    main()