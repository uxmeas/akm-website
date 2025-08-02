#!/usr/bin/env python3
"""
Quick testing script to check common issues before deployment
Run this to get a quick overview of potential problems
"""

import os
import re
from pathlib import Path

def check_html_files():
    """Check all HTML files for common issues"""
    html_files = list(Path('.').glob('*.html'))
    issues = []
    
    print(f"\n📋 Checking {len(html_files)} HTML files...\n")
    
    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        file_issues = []
        
        # Check for placeholder text
        if 'lorem ipsum' in content.lower():
            file_issues.append("Contains Lorem Ipsum placeholder text")
        
        # Check for missing meta descriptions
        if '<meta name="description"' not in content:
            file_issues.append("Missing meta description")
            
        # Check for missing favicon
        if '<link rel="icon"' not in content:
            file_issues.append("Missing favicon link")
            
        # Check for TODO comments
        if 'TODO' in content or 'FIXME' in content:
            file_issues.append("Contains TODO/FIXME comments")
            
        # Check for console.log statements
        if 'console.log' in content:
            file_issues.append("Contains console.log statements")
            
        # Check for localhost references
        if 'localhost' in content or '127.0.0.1' in content:
            file_issues.append("Contains localhost references")
            
        # Check for broken image paths
        img_pattern = r'src=["\'](.*?)["\']'
        images = re.findall(img_pattern, content)
        for img in images:
            if not img.startswith('http') and not img.startswith('data:'):
                if not os.path.exists(img):
                    file_issues.append(f"Broken image path: {img}")
        
        # Check viewport meta tag
        if '<meta name="viewport"' not in content:
            file_issues.append("Missing viewport meta tag for mobile")
            
        # Check for form input font size (mobile zoom issue)
        if '<input' in content and 'font-size' not in content:
            file_issues.append("Form inputs may cause zoom on mobile (no font-size specified)")
        
        if file_issues:
            issues.append((file.name, file_issues))
    
    return issues

def check_performance_issues():
    """Check for performance-related issues"""
    print("\n🚀 Checking performance issues...\n")
    
    issues = []
    
    # Check image sizes
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    large_images = []
    
    for ext in image_extensions:
        for img_file in Path('.').rglob(f'*{ext}'):
            size_mb = os.path.getsize(img_file) / (1024 * 1024)
            if size_mb > 0.5:  # Images larger than 500KB
                large_images.append((img_file, f"{size_mb:.2f}MB"))
    
    if large_images:
        issues.append(("Large Images Found", large_images))
    
    # Check for optimized folder
    if os.path.exists('assets/optimized'):
        optimized_count = len(list(Path('assets/optimized').glob('*')))
        print(f"✅ Found {optimized_count} optimized images")
    else:
        issues.append(("Missing optimized images folder", ["No assets/optimized directory found"]))
    
    return issues

def check_mobile_readiness():
    """Check mobile-specific issues"""
    print("\n📱 Checking mobile readiness...\n")
    
    mobile_ready = []
    
    # Check if mobile menu fix was applied
    html_files = list(Path('.').glob('*.html'))
    mobile_menu_fixed = 0
    
    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'solutions-mobile-toggle' in content and 'DOMContentLoaded' in content:
                mobile_menu_fixed += 1
    
    mobile_ready.append(f"Mobile menu properly implemented in {mobile_menu_fixed}/{len(html_files)} files")
    
    # Check responsive grid classes
    responsive_forms = 0
    for file in html_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'grid-cols-1 md:grid-cols-2' in content:
                responsive_forms += 1
    
    mobile_ready.append(f"Responsive forms found in {responsive_forms} files")
    
    return mobile_ready

def generate_report(html_issues, perf_issues, mobile_status):
    """Generate a summary report"""
    print("\n" + "="*50)
    print("📊 PRE-DEPLOYMENT QUICK CHECK REPORT")
    print("="*50 + "\n")
    
    # HTML Issues
    if html_issues:
        print("❌ HTML ISSUES FOUND:")
        for filename, issues in html_issues:
            print(f"\n  📄 {filename}:")
            for issue in issues:
                print(f"     - {issue}")
    else:
        print("✅ No HTML issues found!")
    
    # Performance Issues
    if perf_issues:
        print("\n❌ PERFORMANCE ISSUES:")
        for issue_type, details in perf_issues:
            print(f"\n  🚨 {issue_type}:")
            for detail in details:
                if isinstance(detail, tuple):
                    print(f"     - {detail[0]}: {detail[1]}")
                else:
                    print(f"     - {detail}")
    else:
        print("\n✅ No major performance issues found!")
    
    # Mobile Status
    print("\n📱 MOBILE STATUS:")
    for status in mobile_status:
        print(f"  - {status}")
    
    # Summary
    total_issues = len(html_issues) + len(perf_issues)
    print(f"\n{'='*50}")
    if total_issues == 0:
        print("✅ SITE APPEARS READY FOR DEPLOYMENT!")
        print("   Remember to still do manual testing, especially:")
        print("   - Form submissions (requires live server)")
        print("   - Cross-browser testing")
        print("   - Mobile device testing")
    else:
        print(f"⚠️  FOUND {total_issues} CATEGORIES OF ISSUES")
        print("   Please address these before deployment")
    
    print("\n📝 Next Steps:")
    print("1. Review PRE-DEPLOYMENT-CHECKLIST.md for complete list")
    print("2. Test forms on staging server")
    print("3. Run through mobile devices physically")
    print("4. Validate HTML at https://validator.w3.org/")
    print("5. Check page speed at https://pagespeed.web.dev/")

if __name__ == "__main__":
    print("🔍 Running pre-deployment quick check...")
    
    # Run checks
    html_issues = check_html_files()
    perf_issues = check_performance_issues()
    mobile_status = check_mobile_readiness()
    
    # Generate report
    generate_report(html_issues, perf_issues, mobile_status)