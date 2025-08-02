#!/usr/bin/env python3
"""
Update industry pages to use new optimized background images
"""

import os
import re

def update_industry_backgrounds():
    """Update all industry pages with new optimized backgrounds"""
    
    # Mapping of industry pages to new image names
    industry_mapping = {
        'industry-aerospace-defense.html': 'industries-aerospace',
        'industry-chemical-processing.html': 'industries-chemical',
        'industry-energy-oil-gas.html': 'industries-energy',
        'industry-financial-services.html': 'industries-financial',
        'industry-government.html': 'industries-government',
        'industry-manufacturing.html': 'industries-manufacturing',
        'industry-mining.html': 'industries-mining',
        'industry-pharmaceuticals.html': 'industries-pharmaceuticals',
        'industry-transportation.html': 'industries-transportation',
        'industry-utilities.html': 'industries-utilities'
    }
    
    print("📝 Updating industry page backgrounds...\n")
    
    for html_file, img_base in industry_mapping.items():
        if not os.path.exists(html_file):
            print(f"  ⚠️  {html_file} not found")
            continue
            
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace background image in the section tag
        # Pattern: background-image: url('assets/industries/industries-*.png')
        old_pattern = r"background-image:\s*url\('assets/industries/industries-[^']+\.png'\)"
        new_bg = f"background-image: url('assets/optimized/{img_base}-large.jpg')"
        
        # Perform replacement
        updated_content = re.sub(old_pattern, new_bg, content)
        
        # Check if replacement was made
        if updated_content != content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print(f"  ✅ Updated {html_file}")
        else:
            print(f"  ℹ️  {html_file} - no matching pattern found")
            # Debug: show what we're looking for
            if 'background-image:' in content:
                matches = re.findall(r"background-image:[^;]+", content)
                print(f"     Found: {matches[0] if matches else 'none'}")

def main():
    """Main execution"""
    update_industry_backgrounds()
    
    print("\n✅ Background update complete!")
    print("\nThe industry pages now use optimized images from assets/optimized/")
    print("Each page loads the -large.jpg version (1920px wide)")

if __name__ == "__main__":
    main()