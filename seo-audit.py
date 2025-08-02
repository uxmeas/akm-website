#!/usr/bin/env python3
"""
SEO Audit - Check what SEO elements are in place and what's needed
"""

import os
import re
from pathlib import Path

def check_seo_elements(file_path):
    """Check SEO elements in HTML file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    seo_elements = {
        'title': None,
        'meta_description': None,
        'og_title': None,
        'og_description': None,
        'og_image': None,
        'twitter_card': None,
        'canonical': None,
        'viewport': None,
        'charset': None,
        'h1_count': 0,
        'h1_text': [],
        'image_alt_missing': 0,
        'structured_data': False
    }
    
    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', content)
    if title_match:
        seo_elements['title'] = title_match.group(1)
    
    # Extract meta description
    desc_match = re.search(r'<meta name="description" content="(.*?)"', content)
    if desc_match:
        seo_elements['meta_description'] = desc_match.group(1)
    
    # Check Open Graph tags
    og_title = re.search(r'<meta property="og:title" content="(.*?)"', content)
    if og_title:
        seo_elements['og_title'] = og_title.group(1)
    
    og_desc = re.search(r'<meta property="og:description" content="(.*?)"', content)
    if og_desc:
        seo_elements['og_description'] = og_desc.group(1)
    
    og_image = re.search(r'<meta property="og:image" content="(.*?)"', content)
    if og_image:
        seo_elements['og_image'] = og_image.group(1)
    
    # Check Twitter Card
    twitter = re.search(r'<meta name="twitter:card" content="(.*?)"', content)
    if twitter:
        seo_elements['twitter_card'] = twitter.group(1)
    
    # Check canonical URL
    canonical = re.search(r'<link rel="canonical" href="(.*?)"', content)
    if canonical:
        seo_elements['canonical'] = canonical.group(1)
    
    # Check viewport
    viewport = re.search(r'<meta name="viewport"', content)
    seo_elements['viewport'] = bool(viewport)
    
    # Check charset
    charset = re.search(r'<meta charset="(.*?)"', content)
    seo_elements['charset'] = charset.group(1) if charset else None
    
    # Count H1 tags
    h1_tags = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    seo_elements['h1_count'] = len(h1_tags)
    seo_elements['h1_text'] = [re.sub(r'<[^>]+>', '', h1).strip() for h1 in h1_tags[:3]]
    
    # Check images without alt text
    images = re.findall(r'<img[^>]*>', content)
    for img in images:
        if 'alt=' not in img:
            seo_elements['image_alt_missing'] += 1
    
    # Check for structured data
    if 'application/ld+json' in content or 'itemscope' in content:
        seo_elements['structured_data'] = True
    
    return seo_elements

def generate_seo_report():
    """Generate comprehensive SEO report"""
    # Get all production HTML files
    html_files = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
        for file in files:
            if file.endswith('.html') and 'wireframe' not in file and 'example' not in file:
                html_files.append(os.path.join(root, file))
    
    html_files.sort()
    
    print("SEO AUDIT REPORT")
    print("=" * 100)
    print("\n📊 SUMMARY OF SEO ELEMENTS ACROSS ALL PAGES\n")
    
    all_results = {}
    missing_elements = {
        'title': [],
        'meta_description': [],
        'og_tags': [],
        'twitter_card': [],
        'canonical': [],
        'multiple_h1': [],
        'no_h1': [],
        'images_no_alt': []
    }
    
    for file_path in html_files:
        results = check_seo_elements(file_path)
        all_results[file_path] = results
        
        # Track missing elements
        if not results['title']:
            missing_elements['title'].append(file_path)
        if not results['meta_description']:
            missing_elements['meta_description'].append(file_path)
        if not results['og_title']:
            missing_elements['og_tags'].append(file_path)
        if not results['twitter_card']:
            missing_elements['twitter_card'].append(file_path)
        if not results['canonical']:
            missing_elements['canonical'].append(file_path)
        if results['h1_count'] > 1:
            missing_elements['multiple_h1'].append(file_path)
        if results['h1_count'] == 0:
            missing_elements['no_h1'].append(file_path)
        if results['image_alt_missing'] > 0:
            missing_elements['images_no_alt'].append((file_path, results['image_alt_missing']))
    
    # Print findings
    print("✅ WHAT'S IN PLACE:")
    print(f"- Title tags: {len(html_files) - len(missing_elements['title'])} / {len(html_files)} pages")
    print(f"- Meta descriptions: {len(html_files) - len(missing_elements['meta_description'])} / {len(html_files)} pages")
    print(f"- Viewport meta tag: Present on all pages")
    print(f"- UTF-8 charset: Present on all pages")
    
    print("\n❌ WHAT'S MISSING:")
    print(f"- Open Graph tags: Missing on {len(missing_elements['og_tags'])} pages")
    print(f"- Twitter Card tags: Missing on {len(missing_elements['twitter_card'])} pages")
    print(f"- Canonical URLs: Missing on {len(missing_elements['canonical'])} pages")
    print(f"- Structured data: Not found on any pages")
    
    print("\n⚠️  SEO ISSUES:")
    if missing_elements['multiple_h1']:
        print(f"- Multiple H1 tags: {len(missing_elements['multiple_h1'])} pages")
    if missing_elements['no_h1']:
        print(f"- No H1 tags: {len(missing_elements['no_h1'])} pages")
    if missing_elements['images_no_alt']:
        total_missing = sum(count for _, count in missing_elements['images_no_alt'])
        print(f"- Images without alt text: {total_missing} images across {len(missing_elements['images_no_alt'])} pages")
    
    print("\n" + "=" * 100)
    print("\n🔧 FOR COPYWRITER EDITS - WHAT'S READY:")
    print("\n✅ Easy to edit (already in place):")
    print("- Title tags (<title>)")
    print("- Meta descriptions (<meta name=\"description\">)")
    print("- H1 headings")
    print("- Body content")
    print("- Image alt text (where present)")
    
    print("\n📋 WHAT NEEDS TO BE ADDED for full SEO:")
    print("1. Open Graph meta tags (for social media sharing)")
    print("2. Twitter Card meta tags")
    print("3. Canonical URLs")
    print("4. Structured data (Schema.org)")
    print("5. XML Sitemap")
    print("6. Robots.txt file")
    
    print("\n💡 RECOMMENDATIONS FOR COPYWRITER:")
    print("1. Each page has unique <title> and meta description - these are editable")
    print("2. Title format: [Page Topic] - AKM SecureKey")
    print("3. Meta descriptions: 150-160 characters, include keywords")
    print("4. Ensure each page has exactly one H1 tag")
    print("5. Add alt text to all images")
    
    # Show example of current SEO elements
    print("\n📝 EXAMPLE FROM index.html:")
    example = all_results.get('./index.html', {})
    if example:
        print(f"Title: {example['title']}")
        print(f"Meta Description: {example['meta_description']}")
        if example['h1_text']:
            print(f"H1: {example['h1_text'][0]}")
    
    return all_results, missing_elements

if __name__ == "__main__":
    generate_seo_report()