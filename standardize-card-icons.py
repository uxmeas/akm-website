#!/usr/bin/env python3
"""
Standardize icon sizes for feature, solution, and industry cards only.
Leaves navigation, hero sections, and testimonial icons unchanged.
"""

import re
import glob
import os

def standardize_card_icons(content, filename):
    """Standardize icon sizes in feature/solution/industry cards to w-10 h-10"""
    
    changes_made = False
    
    # Pattern to find card icons that need standardization
    # This targets icons within card contexts that currently use w-8 h-8 or w-12 h-12
    
    # Feature cards pattern (usually w-8 h-8)
    # Look for cards with specific classes and icon sizes
    patterns = [
        # Feature cards with w-8 h-8 icons
        (r'(<div class="(?:fade-in-card )?bg-(?:white|black)(?: text-white)? shadow-lg p-6.*?<i data-lucide="[^"]*" class=")w-8 h-8', r'\1w-10 h-10'),
        
        # Solution cards that might have w-8 h-8
        (r'(<div class="(?:fade-in-card )?bg-white border-t-4 border-black shadow-lg p-8.*?<i data-lucide="[^"]*" class=")w-8 h-8', r'\1w-10 h-10'),
        
        # Any remaining card contexts with w-12 h-12 (but not testimonials)
        (r'(<div class="(?:fade-in-card )?(?:bg-(?:white|black)|.*?shadow-lg).*?p-6.*?<i data-lucide="(?!quote)[^"]*" class=")w-12 h-12', r'\1w-10 h-10'),
    ]
    
    for pattern, replacement in patterns:
        new_content, count = re.subn(pattern, replacement, content, flags=re.DOTALL)
        if count > 0:
            content = new_content
            changes_made = True
            print(f"  - Updated {count} icons from {pattern.split('w-')[1].split(' ')[0]} to w-10")
    
    # Special handling for the home page "How We Solve" section icons
    if 'index.html' in filename:
        # Update the solution cards in the How We Solve section
        solution_pattern = r'(<div class="p-3 bg-gray-100 rounded-lg">\s*<i data-lucide="[^"]*" class=")w-8 h-8'
        new_content, count = re.subn(solution_pattern, r'\1w-10 h-10', content, flags=re.DOTALL)
        if count > 0:
            content = new_content
            changes_made = True
            print(f"  - Updated {count} solution card icons from w-8 to w-10")
    
    return content, changes_made

def main():
    print("Standardizing card icon sizes...")
    print("Target: Features, Solutions, and Industries cards → w-10 h-10")
    print("Preserving: Navigation, Hero sections, and Testimonials\n")
    
    updated_files = []
    
    # Process all HTML files
    for filepath in glob.glob("*.html"):
        if filepath.endswith('.backup'):
            continue
            
        print(f"Checking: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Apply standardization
        new_content, was_updated = standardize_card_icons(content, filepath)
        
        if was_updated:
            # Write updated content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated_files.append(filepath)
            print(f"  ✓ Updated\n")
        else:
            print(f"  - No changes needed\n")
    
    print("\nStandardization complete!")
    print(f"Files updated: {len(updated_files)}")
    
    if updated_files:
        print("\nUpdated files:")
        for file in updated_files:
            print(f"  - {file}")
    
    print("\nAll feature, solution, and industry cards now use consistent w-10 h-10 icons.")
    print("Navigation (w-4, w-5, w-6), hero sections, and testimonials (w-16) remain unchanged.")

if __name__ == "__main__":
    main()