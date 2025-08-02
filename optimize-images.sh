#!/bin/bash

# Image optimization script for AKM SecureKey website
# This script will:
# 1. Convert large PNG images to WebP format
# 2. Create multiple sizes for responsive images
# 3. Remove duplicate files

echo "Starting image optimization..."

# Check if required tools are installed
check_tool() {
    if ! command -v $1 &> /dev/null; then
        echo "Error: $1 is not installed. Please install it first."
        echo "On macOS: brew install webp imagemagick"
        echo "On Ubuntu/Debian: sudo apt-get install webp imagemagick"
        exit 1
    fi
}

# Check for required tools
check_tool cwebp
check_tool convert
check_tool identify

# Create optimized directory
mkdir -p assets/optimized

# Function to convert and optimize images
optimize_image() {
    local input_file="$1"
    local output_dir="assets/optimized"
    local filename=$(basename "$input_file" .png)
    
    echo "Processing: $input_file"
    
    # Get original dimensions
    local dimensions=$(identify -format "%wx%h" "$input_file")
    echo "  Original dimensions: $dimensions"
    
    # Convert to WebP with high quality
    cwebp -q 85 "$input_file" -o "$output_dir/${filename}.webp"
    
    # Create responsive versions
    # Large (100%)
    convert "$input_file" -quality 85 "$output_dir/${filename}-large.jpg"
    
    # Medium (75%)
    convert "$input_file" -resize 75% -quality 85 "$output_dir/${filename}-medium.jpg"
    
    # Small (50%)
    convert "$input_file" -resize 50% -quality 85 "$output_dir/${filename}-small.jpg"
    
    # Mobile (25%)
    convert "$input_file" -resize 25% -quality 85 "$output_dir/${filename}-mobile.jpg"
    
    echo "  Created WebP and responsive versions"
}

# Process hero and background images
echo ""
echo "=== Processing hero and background images ==="
for img in assets/*hero*.png assets/*background*.png assets/future-of-ot-security.png assets/ready-to-secure.png assets/how-*.png assets/built-for-the-future.png; do
    if [ -f "$img" ]; then
        optimize_image "$img"
    fi
done

# Process industry images (card images)
echo ""
echo "=== Processing industry card images ==="
for img in assets/industries/industries-*.png; do
    if [ -f "$img" ] && [[ ! "$img" == *"-photo.png" ]]; then
        optimize_image "$img"
    fi
done

# Process industry photos (already smaller)
echo ""
echo "=== Processing industry photos ==="
for img in assets/industries/*-photo.png; do
    if [ -f "$img" ]; then
        echo "Processing: $img"
        # Just convert to WebP for these smaller images
        cwebp -q 90 "$img" -o "assets/optimized/$(basename "$img" .png).webp"
    fi
done

# Remove duplicate logo
echo ""
echo "=== Removing duplicate files ==="
if [ -f "assets/logos/akmlogo-white.png" ]; then
    echo "Removing duplicate logo from assets/logos/"
    rm "assets/logos/akmlogo-white.png"
    rmdir "assets/logos" 2>/dev/null
fi

# Show size comparison
echo ""
echo "=== Size comparison ==="
original_size=$(du -sh assets | cut -f1)
optimized_size=$(du -sh assets/optimized | cut -f1)
echo "Original assets size: $original_size"
echo "Optimized assets size: $optimized_size"

echo ""
echo "Optimization complete! Optimized files are in assets/optimized/"
echo ""
echo "Next steps:"
echo "1. Review the optimized images for quality"
echo "2. Update HTML files to use WebP with fallbacks"
echo "3. Implement responsive images with srcset"
echo "4. Move optimized files to replace originals (after backup)"