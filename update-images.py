#!/usr/bin/env python3
"""
Script to update HTML files to use optimized images with responsive srcset
"""

import os
import re
import glob

def update_background_images(content):
    """Update CSS background images to use optimized versions"""
    
    # Map of original images to optimized versions
    replacements = [
        ('industries-sub-hero-background.png', 'optimized/industries-sub-hero-background-large.jpg'),
        ('solutions-sub-hero-background.png', 'optimized/solutions-sub-hero-background-large.jpg'),
        ('sub-hero-about.png', 'optimized/sub-hero-about-large.jpg'),
        ('hero-banner.png', 'optimized/hero-banner-large.jpg'),
        ('hero-subpages.png', 'optimized/hero-subpages-large.jpg'),
    ]
    
    for old, new in replacements:
        content = content.replace(f"url('assets/{old}')", f"url('assets/{new}')")
        content = content.replace(f'url("assets/{old}")', f'url("assets/{new}")')
    
    return content

def update_img_tags(content):
    """Update img tags to use picture elements with srcset"""
    
    # Industry card images
    industry_cards = [
        'industries-energy', 'industries-financial', 'industries-government',
        'industries-manufacturing', 'industries-mining', 'industries-pharmaceuticals',
        'industries-transportation', 'industries-utilities', 'industries-aerospace',
        'industries-chemical'
    ]
    
    for card in industry_cards:
        # Find img tags with this source
        pattern = f'<img src="assets/industries/{card}.png"([^>]*)>'
        replacement = f'''<picture>
                    <img src="assets/optimized/{card}-large.jpg"
                         srcset="assets/optimized/{card}-mobile.jpg 640w,
                                 assets/optimized/{card}-small.jpg 1280w,
                                 assets/optimized/{card}-medium.jpg 1920w,
                                 assets/optimized/{card}-large.jpg 2560w"
                         sizes="(max-width: 768px) 100vw, (max-width: 1024px) 50vw, 33vw"
                         loading="lazy"\\1>
                </picture>'''
        content = re.sub(pattern, replacement, content)
    
    # Industry photo images
    industry_photos = [
        'industries-energy-photo', 'industries-financial-photo', 'industries-government-photo',
        'industries-manufacturing-photo', 'industries-mining-photo', 'industries-pharmaceuticals-photo',
        'industries-transportation-photo', 'industries-utilities-photo', 'industries-aerospace-photo',
        'industries-chemical-photo'
    ]
    
    for photo in industry_photos:
        pattern = f'<img src="assets/industries/{photo}.png"([^>]*)>'
        replacement = f'<img src="assets/optimized/{photo}.jpg" loading="lazy"\\1>'
        content = re.sub(pattern, replacement, content)
    
    # Other images
    other_images = {
        'future-of-ot-security.png': 'future-of-ot-security',
        'ready-to-secure.png': 'ready-to-secure',
        'how-we-solve.png': 'how-we-solve',
        'how-akm-securekey-works-for-you.png': 'how-akm-securekey-works-for-you',
        'how-akm-securekey-works-for-you-2.png': 'how-akm-securekey-works-for-you-2',
        'built-for-the-future.png': 'built-for-the-future',
    }
    
    for old_name, base_name in other_images.items():
        pattern = f'<img src="assets/{old_name}"([^>]*)>'
        replacement = f'''<picture>
                    <img src="assets/optimized/{base_name}-large.jpg"
                         srcset="assets/optimized/{base_name}-mobile.jpg 640w,
                                 assets/optimized/{base_name}-small.jpg 1280w,
                                 assets/optimized/{base_name}-medium.jpg 1920w,
                                 assets/optimized/{base_name}-large.jpg 2560w"
                         sizes="100vw"
                         loading="lazy"\\1>
                </picture>'''
        content = re.sub(pattern, replacement, content)
    
    return content

def process_html_file(filepath):
    """Process a single HTML file"""
    print(f"Processing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Backup original
    backup_path = filepath + '.backup'
    if not os.path.exists(backup_path):
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    # Update content
    content = update_background_images(content)
    content = update_img_tags(content)
    
    # Write updated content
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ Updated")

def main():
    print("Updating HTML files to use optimized images...")
    print("")
    
    # Process all HTML files
    html_files = glob.glob("*.html")
    
    for html_file in html_files:
        if not html_file.endswith('.backup'):
            process_html_file(html_file)
    
    print("")
    print("Update complete!")
    print("")
    print("Next steps:")
    print("1. Review the updated HTML files")
    print("2. Test all images load correctly")
    print("3. Check responsive behavior on different devices")
    print("4. Deploy the optimized site")
    print("")
    print("Backups created with .backup extension")

if __name__ == "__main__":
    main()