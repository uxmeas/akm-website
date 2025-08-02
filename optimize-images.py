#!/usr/bin/env python3
"""
Image optimization script for AKM SecureKey website
This script will compress PNG images and create responsive versions
"""

import os
import sys
from PIL import Image
import shutil

def optimize_image(input_path, output_dir):
    """Optimize a single image file"""
    filename = os.path.basename(input_path)
    name, ext = os.path.splitext(filename)
    
    print(f"Processing: {filename}")
    
    try:
        # Open the image
        img = Image.open(input_path)
        
        # Convert RGBA to RGB if needed (for JPEG)
        if img.mode in ('RGBA', 'LA'):
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = rgb_img
        
        # Save optimized versions
        # Original size - high quality JPEG
        img.save(os.path.join(output_dir, f"{name}-large.jpg"), 'JPEG', quality=85, optimize=True)
        
        # 75% size
        medium = img.resize((int(img.width * 0.75), int(img.height * 0.75)), Image.Resampling.LANCZOS)
        medium.save(os.path.join(output_dir, f"{name}-medium.jpg"), 'JPEG', quality=85, optimize=True)
        
        # 50% size
        small = img.resize((int(img.width * 0.5), int(img.height * 0.5)), Image.Resampling.LANCZOS)
        small.save(os.path.join(output_dir, f"{name}-small.jpg"), 'JPEG', quality=85, optimize=True)
        
        # 25% size for mobile
        mobile = img.resize((int(img.width * 0.25), int(img.height * 0.25)), Image.Resampling.LANCZOS)
        mobile.save(os.path.join(output_dir, f"{name}-mobile.jpg"), 'JPEG', quality=85, optimize=True)
        
        # Also save an optimized PNG
        img.save(os.path.join(output_dir, f"{name}-optimized.png"), 'PNG', optimize=True)
        
        print(f"  ✓ Created responsive versions")
        
        # Show size reduction
        original_size = os.path.getsize(input_path)
        optimized_size = os.path.getsize(os.path.join(output_dir, f"{name}-large.jpg"))
        reduction = (1 - optimized_size / original_size) * 100
        print(f"  ✓ Size reduction: {reduction:.1f}%")
        
    except Exception as e:
        print(f"  ✗ Error processing {filename}: {str(e)}")

def main():
    print("Starting image optimization...")
    
    # Check if PIL is available
    try:
        from PIL import Image
    except ImportError:
        print("Error: Pillow is not installed.")
        print("Please install it with: pip install Pillow")
        sys.exit(1)
    
    # Create output directory
    output_dir = "assets/optimized"
    os.makedirs(output_dir, exist_ok=True)
    
    # Process hero and background images
    print("\n=== Processing hero and background images ===")
    hero_patterns = [
        "assets/*hero*.png",
        "assets/*background*.png",
        "assets/future-of-ot-security.png",
        "assets/ready-to-secure.png",
        "assets/how-*.png",
        "assets/built-for-the-future.png"
    ]
    
    import glob
    for pattern in hero_patterns:
        for img_path in glob.glob(pattern):
            if os.path.isfile(img_path):
                optimize_image(img_path, output_dir)
    
    # Process industry card images
    print("\n=== Processing industry card images ===")
    for img_path in glob.glob("assets/industries/industries-*.png"):
        if os.path.isfile(img_path) and "-photo.png" not in img_path:
            optimize_image(img_path, output_dir)
    
    # Process industry photos
    print("\n=== Processing industry photos ===")
    for img_path in glob.glob("assets/industries/*-photo.png"):
        if os.path.isfile(img_path):
            # For smaller images, just create optimized version
            filename = os.path.basename(img_path)
            name, ext = os.path.splitext(filename)
            
            print(f"Processing: {filename}")
            img = Image.open(img_path)
            
            # Convert to RGB if needed
            if img.mode in ('RGBA', 'LA'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = rgb_img
            
            img.save(os.path.join(output_dir, f"{name}.jpg"), 'JPEG', quality=90, optimize=True)
    
    # Remove duplicate logo
    print("\n=== Removing duplicate files ===")
    if os.path.exists("assets/logos/akmlogo-white.png"):
        print("Removing duplicate logo from assets/logos/")
        os.remove("assets/logos/akmlogo-white.png")
        try:
            os.rmdir("assets/logos")
        except:
            pass
    
    print("\nOptimization complete!")
    print(f"Optimized files are in {output_dir}/")
    print("\nNext steps:")
    print("1. Review the optimized images for quality")
    print("2. Update HTML files to use optimized images")
    print("3. Implement responsive images with srcset")

if __name__ == "__main__":
    main()