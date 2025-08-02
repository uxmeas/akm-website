#!/usr/bin/env python3
"""
Fix mobile issues in AKM SecureKey website:
1. Mobile menu submenu click functionality
2. Form mobile responsiveness
3. Add skeleton loaders for images
"""

import os
import re
import glob

def fix_mobile_menu_script(content):
    """Fix the mobile menu JavaScript to ensure submenus work properly"""
    
    # Find the script section with mobile menu code
    script_pattern = r'(// Mobile dropdown toggles\s*\n)(.*?)(mobileMenuToggle\.addEventListener)'
    
    # New robust mobile menu code
    new_mobile_menu_code = '''// Mobile dropdown toggles
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
                solutionsToggle.style.transform = solutionsMenu.classList.contains('hidden') ? 'rotate(0deg)' : 'rotate(45deg)';
                
                // Re-initialize Lucide icons
                setTimeout(() => {
                    lucide.createIcons();
                }, 100);
            });
        }

        if (industriesToggle && industriesMenu) {
            industriesToggle.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                industriesMenu.classList.toggle('hidden');
                industriesToggle.style.transform = industriesMenu.classList.contains('hidden') ? 'rotate(0deg)' : 'rotate(45deg)';
                
                // Re-initialize Lucide icons
                setTimeout(() => {
                    lucide.createIcons();
                }, 100);
            });
        }
        
        '''
    
    # Replace the mobile dropdown code
    content = re.sub(
        r'// Mobile dropdown toggles.*?industriesToggle\.style\.transform[^\n]*\n\s*}\);',
        new_mobile_menu_code.strip(),
        content,
        flags=re.DOTALL
    )
    
    return content

def fix_form_responsiveness(content):
    """Fix form mobile responsiveness issues"""
    
    # Fix form container to be responsive
    content = re.sub(
        r'<form class="space-y-4 max-w-2xl mx-auto">',
        '<form class="space-y-4 w-full max-w-2xl mx-auto">',
        content
    )
    
    # Fix form grid to stack on mobile
    content = re.sub(
        r'<div class="grid grid-cols-2 gap-4">',
        '<div class="grid grid-cols-1 md:grid-cols-2 gap-4">',
        content
    )
    
    # Fix input fields to be full width on mobile
    content = re.sub(
        r'<input([^>]*?)class="([^"]*?)"',
        lambda m: f'<input{m.group(1)}class="w-full {m.group(2)}"' if 'w-full' not in m.group(2) else m.group(0),
        content
    )
    
    # Fix select to be full width
    content = re.sub(
        r'<select([^>]*?)class="([^"]*?)"',
        lambda m: f'<select{m.group(1)}class="w-full {m.group(2)}"' if 'w-full' not in m.group(2) else m.group(0),
        content
    )
    
    # Fix button to be full width on mobile
    content = re.sub(
        r'<button type="submit" class="([^"]*?)">',
        lambda m: '<button type="submit" class="w-full ' + m.group(1) + '">' if 'w-full' not in m.group(1) else m.group(0),
        content
    )
    
    return content

def add_skeleton_loaders(content):
    """Add skeleton loaders for large images"""
    
    # Add skeleton loader styles in the head
    skeleton_styles = '''
        /* Skeleton loader styles */
        .skeleton-loader {
            background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
            background-size: 200% 100%;
            animation: loading 1.5s infinite;
        }
        
        @keyframes loading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
        
        .image-container {
            position: relative;
            overflow: hidden;
        }
        
        .image-container img {
            transition: opacity 0.3s ease;
        }
        
        .image-container.loading img {
            opacity: 0;
        }
        
        .image-container .skeleton {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 1;
        }
        
        .image-container.loaded .skeleton {
            display: none;
        }
    '''
    
    # Add styles before </style>
    content = re.sub(
        r'(</style>)',
        skeleton_styles + r'\1',
        content
    )
    
    # Add image loading script
    image_loading_script = '''
        
        // Image loading with skeleton
        document.addEventListener('DOMContentLoaded', function() {
            // Add skeleton loaders to large images
            const largeImages = document.querySelectorAll('img[src*="-large"], img[src*="hero"], img[src*="background"]');
            
            largeImages.forEach(img => {
                // Skip if already processed
                if (img.closest('.image-container')) return;
                
                // Wrap image in container
                const container = document.createElement('div');
                container.className = 'image-container loading';
                container.style.width = img.style.width || '100%';
                container.style.height = img.style.height || 'auto';
                
                // Create skeleton
                const skeleton = document.createElement('div');
                skeleton.className = 'skeleton skeleton-loader';
                skeleton.style.minHeight = '200px';
                
                // Wrap the image
                img.parentNode.insertBefore(container, img);
                container.appendChild(skeleton);
                container.appendChild(img);
                
                // Handle image load
                if (img.complete) {
                    container.classList.remove('loading');
                    container.classList.add('loaded');
                } else {
                    img.addEventListener('load', function() {
                        container.classList.remove('loading');
                        container.classList.add('loaded');
                    });
                    
                    img.addEventListener('error', function() {
                        container.classList.remove('loading');
                        skeleton.style.background = '#f0f0f0';
                        skeleton.innerHTML = '<div style="display: flex; align-items: center; justify-content: center; height: 100%; color: #999;">Failed to load image</div>';
                    });
                }
            });
        });
    '''
    
    # Add script before closing body tag
    content = re.sub(
        r'(</body>)',
        f'<script>{image_loading_script}</script>\n\\1',
        content
    )
    
    return content

def process_html_file(filepath):
    """Process a single HTML file"""
    print(f"Processing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Apply fixes
    original_content = content
    content = fix_mobile_menu_script(content)
    content = fix_form_responsiveness(content)
    content = add_skeleton_loaders(content)
    
    # Only write if changes were made
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ Fixed")
    else:
        print(f"  - No changes needed")

def main():
    print("Fixing mobile issues...")
    print("")
    
    # Process all HTML files
    html_files = glob.glob("*.html")
    
    for html_file in html_files:
        if not html_file.endswith('.backup'):
            process_html_file(html_file)
    
    print("")
    print("Fixes complete!")
    print("")
    print("Fixed:")
    print("1. Mobile menu submenu click functionality")
    print("2. Form mobile responsiveness")
    print("3. Added skeleton loaders for large images")

if __name__ == "__main__":
    main()