# Icon Size Standardization Guide

## Current Inconsistencies

The website currently uses different icon sizes across various card types, which creates visual inconsistency. Here's the current state and recommended standardization:

## Current Icon Sizes

| Component Type | Current Size | Location |
|----------------|--------------|----------|
| Navigation dropdowns | `w-4 h-4` | Nav menus |
| Mobile menu toggles | `w-6 h-6` | Mobile nav |
| Home page feature cards | `w-8 h-8` | Homepage sections |
| Solution pages cards | `w-10 h-10` | Solutions/features |
| Industry pages cards | `w-10 h-10` | Industry capabilities |
| Hero section icons | `w-12 h-12` | Some hero sections |
| Testimonial quotes | `w-16 h-16` | Quote decorations |

## Recommended Standardization

### 1. **Primary Card Icons** (Most Important)
Standardize all primary card icons to `w-10 h-10`:
- Feature cards
- Capability cards
- Benefit cards
- Use case cards

**Why**: This size is large enough to be clear but not overwhelming, and it's already the most commonly used size.

### 2. **Navigation Icons**
Keep current sizes:
- Dropdown arrows: `w-4 h-4`
- Mobile menu: `w-6 h-6`
- Arrow links: `w-5 h-5`

**Why**: These are appropriately sized for their context.

### 3. **Decorative Icons**
- Testimonial quotes: Keep `w-16 h-16` (they're decorative backgrounds)
- Hero overlays: Can vary based on design needs

## Implementation Script

```python
#!/usr/bin/env python3
"""Standardize icon sizes across the website"""

import re
import glob

def standardize_icons(content):
    # Card icons: Change w-8 h-8 and w-12 h-12 to w-10 h-10 in cards
    card_contexts = [
        'bg-white shadow-lg p-6',
        'bg-black text-white p-6',
        'fade-in-card',
        'bg-white border-t-4'
    ]
    
    for context in card_contexts:
        # Find card blocks and update icon sizes
        pattern = rf'({context}.*?<i data-lucide.*?class=")(w-(?:8|12) h-(?:8|12))('
        content = re.sub(pattern, r'\1w-10 h-10\3', content, flags=re.DOTALL)
    
    return content

# Process all HTML files
for file in glob.glob("*.html"):
    if not file.endswith('.backup'):
        with open(file, 'r') as f:
            content = f.read()
        
        updated = standardize_icons(content)
        
        if updated != content:
            with open(file, 'w') as f:
                f.write(updated)
            print(f"Updated: {file}")
```

## Visual Impact

### Before Standardization:
- Inconsistent visual hierarchy
- Some cards feel "heavier" than others
- Unpredictable icon sizing

### After Standardization:
- Consistent visual weight across all cards
- Better visual rhythm and balance
- Professional, polished appearance
- Easier to maintain

## Benefits

1. **Visual Consistency**: All similar components look cohesive
2. **Better Hierarchy**: Size variations only where intentionally different
3. **Easier Maintenance**: One standard size to remember
4. **Improved Aesthetics**: Balanced visual weight across the page
5. **Better User Experience**: Predictable visual patterns

## Quick Reference

```html
<!-- Standard card icon -->
<i data-lucide="icon-name" class="w-10 h-10 text-color"></i>

<!-- Navigation arrow -->
<i data-lucide="arrow-up-right" class="w-5 h-5"></i>

<!-- Mobile menu icon -->
<i data-lucide="menu" class="w-6 h-6"></i>

<!-- Decorative quote -->
<i data-lucide="quote" class="w-16 h-16 text-white/20"></i>
```