#!/usr/bin/env python3
"""
Add favicon links to all HTML pages
"""

import os
import re

def add_favicon_links(file_path):
    """Add favicon links to HTML file if missing"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip if already has favicon
    if 'favicon.ico' in content or 'rel="icon"' in content:
        return False
    
    # Favicon HTML to insert
    favicon_html = '''    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    '''
    
    # Find where to insert (after <meta name="description"> or before </head>)
    # Try to insert after description meta tag
    meta_desc_pattern = re.search(r'(<meta name="description"[^>]*>)\s*\n', content)
    
    if meta_desc_pattern:
        # Insert after meta description
        insert_pos = meta_desc_pattern.end()
        new_content = content[:insert_pos] + '\n' + favicon_html + content[insert_pos:]
    else:
        # Insert before </head> as fallback
        head_close = content.find('</head>')
        if head_close != -1:
            new_content = content[:head_close] + favicon_html + '\n' + content[head_close:]
        else:
            return False
    
    # Write updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True

def main():
    # Get all HTML files
    html_files = []
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and node_modules
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
        
        for file in files:
            if file.endswith('.html') and 'wireframe' not in file and 'example' not in file:
                html_files.append(os.path.join(root, file))
    
    html_files.sort()
    
    print("Adding favicon links to all pages...")
    print("=" * 80)
    
    added_count = 0
    already_has = 0
    
    for file_path in html_files:
        if add_favicon_links(file_path):
            print(f"✅ Added favicon to: {file_path}")
            added_count += 1
        else:
            print(f"⏭️  Skipped: {file_path} (already has favicon)")
            already_has += 1
    
    print("\n" + "=" * 80)
    print(f"\nSummary:")
    print(f"- Total HTML files: {len(html_files)}")
    print(f"- Added favicon links to: {added_count} pages")
    print(f"- Already had favicon: {already_has} pages")
    
    if added_count > 0:
        print("\n✅ Favicon links successfully added to all pages!")
        print("\nFavicon files being used:")
        print("- /favicon.ico (standard favicon)")
        print("- /favicon-32x32.png (32x32 pixel version)")
        print("- /favicon-16x16.png (16x16 pixel version)")

if __name__ == "__main__":
    main()