#!/usr/bin/env python3
"""
Optimize new industries background images
Creates responsive versions and updates HTML files
"""

import os
import shutil
from pathlib import Path
from PIL import Image

def create_responsive_versions(image_path, output_dir):
    """Create multiple sizes of an image for responsive design"""
    
    # Open the image
    with Image.open(image_path) as img:
        # Convert RGBA to RGB if needed (for JPEG)
        if img.mode in ('RGBA', 'LA'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = rgb_img
        
        # Define sizes
        sizes = {
            'small': (640, None),      # Mobile
            'medium': (1024, None),    # Tablet  
            'large': (1920, None),     # Desktop
            'xlarge': (2560, None)     # Large screens
        }
        
        base_name = image_path.stem
        
        for size_name, (width, _) in sizes.items():
            # Calculate height to maintain aspect ratio
            aspect_ratio = img.height / img.width
            height = int(width * aspect_ratio)
            
            # Resize image
            resized = img.resize((width, height), Image.Resampling.LANCZOS)
            
            # Save with optimization
            output_path = output_dir / f"{base_name}-{size_name}.jpg"
            resized.save(output_path, 'JPEG', quality=85, optimize=True)
            print(f"  Created: {output_path.name} ({width}x{height})")

def optimize_industries_images():
    """Main function to optimize all industries images"""
    
    # Define paths
    industries_dir = Path('assets/industries')
    optimized_dir = Path('assets/optimized')
    
    # Create optimized directory if it doesn't exist
    optimized_dir.mkdir(exist_ok=True)
    
    print("🖼️  Optimizing industries images...\n")
    
    # Process each image
    for img_file in industries_dir.glob('*.png'):
        print(f"\nProcessing: {img_file.name}")
        
        # Create responsive versions
        create_responsive_versions(img_file, optimized_dir)
        
        # Get file sizes for comparison
        original_size = img_file.stat().st_size / (1024 * 1024)
        optimized_size = sum(
            (optimized_dir / f"{img_file.stem}-{size}.jpg").stat().st_size 
            for size in ['small', 'medium', 'large', 'xlarge']
            if (optimized_dir / f"{img_file.stem}-{size}.jpg").exists()
        ) / (1024 * 1024)
        
        print(f"  Original: {original_size:.2f}MB")
        print(f"  Optimized (all sizes): {optimized_size:.2f}MB")
        print(f"  Reduction: {((original_size - optimized_size) / original_size * 100):.1f}%")

def update_industry_pages():
    """Update industry HTML pages to use new images"""
    
    print("\n\n📝 Updating HTML files...\n")
    
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
    
    for html_file, img_base in industry_mapping.items():
        if not os.path.exists(html_file):
            print(f"  ⚠️  {html_file} not found")
            continue
            
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if this page uses hero-background-industry-aerospace.jpg pattern
        old_pattern = r'background-image:\s*url\([\'"]([^\'"\)]+)[\'"\]\)'
        
        # Replace with new optimized image
        new_bg = f"background-image: url('assets/optimized/{img_base}-large.jpg');"
        
        # Find and replace background image
        import re
        if 'background-image:' in content and 'hero-background-industry' in content:
            # Replace the background image
            content = re.sub(
                r'background-image:\s*url\([\'"][^\'"\)]+hero-background-industry-[^\'"\)]+[\'"\]\);',
                new_bg,
                content
            )
            
            # Also add srcset for responsive loading in a picture element if needed
            # For now, just update the background image
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ Updated {html_file}")
        else:
            print(f"  ℹ️  {html_file} - no industry background found")

def main():
    """Main execution"""
    # First optimize images
    optimize_industries_images()
    
    # Then update HTML files
    update_industry_pages()
    
    print("\n\n✅ Industries images optimization complete!")
    print("\nNext steps:")
    print("1. Review the updated pages locally")
    print("2. Commit and push to GitHub")
    print("3. Netlify will auto-deploy the changes")

if __name__ == "__main__":
    main()