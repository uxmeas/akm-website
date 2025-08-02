# Image Optimization Guide for AKM SecureKey Website

## Current Status

The website currently has several large PNG images that need optimization:

### Large Images (>1MB)
1. **Hero/Background Images**
   - `industries-sub-hero-background.png` - 2.1MB
   - `solutions-sub-hero-background.png` - 1.9MB
   - `future-of-ot-security.png` - 1.7MB
   - `ready-to-secure.png` - 1.6MB
   - `how-akm-securekey-works-for-you.png` - 1.6MB
   - Other hero images - 1.4MB each

2. **Industry Card Images**
   - All 10 industry card images - 1.4MB each

3. **Duplicate Files**
   - `assets/akmlogo-white.png` and `assets/logos/akmlogo-white.png` are identical

## Recommended Optimizations

### 1. Image Compression and Format Conversion

#### Install Required Tools
```bash
# macOS
brew install webp imagemagick

# Ubuntu/Debian
sudo apt-get install webp imagemagick

# Or use Python
pip install Pillow
```

#### Convert to WebP Format
WebP provides 25-35% better compression than PNG/JPEG:
```bash
# Convert PNG to WebP
cwebp -q 85 input.png -o output.webp
```

#### Create Responsive Images
Generate multiple sizes for different screen resolutions:
```bash
# Create different sizes
convert input.png -resize 1920x1080 -quality 85 output-large.jpg
convert input.png -resize 1280x720 -quality 85 output-medium.jpg
convert input.png -resize 640x360 -quality 85 output-small.jpg
```

### 2. Update HTML for Responsive Images

Replace current `<img>` tags with responsive picture elements:

```html
<!-- Before -->
<img src="assets/hero-banner.png" alt="Hero">

<!-- After -->
<picture>
  <source type="image/webp" 
          srcset="assets/optimized/hero-banner-mobile.webp 640w,
                  assets/optimized/hero-banner-small.webp 1280w,
                  assets/optimized/hero-banner-medium.webp 1920w,
                  assets/optimized/hero-banner-large.webp 2560w"
          sizes="100vw">
  <img src="assets/optimized/hero-banner-large.jpg" 
       alt="Hero"
       srcset="assets/optimized/hero-banner-mobile.jpg 640w,
               assets/optimized/hero-banner-small.jpg 1280w,
               assets/optimized/hero-banner-medium.jpg 1920w,
               assets/optimized/hero-banner-large.jpg 2560w"
       sizes="100vw">
</picture>
```

### 3. Lazy Loading
Add lazy loading for images below the fold:
```html
<img src="image.jpg" alt="Description" loading="lazy">
```

### 4. File Structure Cleanup
1. Remove `assets/logos/` directory (duplicate logo)
2. Use the logo from `assets/akmlogo-white.png`
3. Consider organizing optimized images in subdirectories

### 5. Expected Results
- Hero images: 2.1MB → ~300-500KB (WebP)
- Industry cards: 1.4MB → ~200-300KB (WebP)
- Industry photos: Already optimized (32KB-169KB)
- Total reduction: ~70-80% file size savings

## Implementation Priority
1. **High Priority**: Hero and background images (biggest impact)
2. **Medium Priority**: Industry card images
3. **Low Priority**: Already optimized industry photos

## Testing
After optimization:
1. Test all images load correctly
2. Verify responsive images work on different devices
3. Check page load speed improvements
4. Ensure fallbacks work for browsers without WebP support

## Automation Scripts
Two scripts are provided:
- `optimize-images.sh` - Bash script using ImageMagick and cwebp
- `optimize-images.py` - Python script using Pillow

Run after installing required dependencies.