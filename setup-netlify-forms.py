#!/usr/bin/env python3
"""
Update all forms to work with Netlify's form handling
This adds the required netlify attribute and honeypot field
"""

import re
from pathlib import Path

def update_forms_for_netlify():
    """Update all forms to work with Netlify"""
    
    # Find all HTML files with forms
    form_files = []
    html_files = list(Path('.').glob('*.html'))
    
    for file in html_files:
        if file.name.endswith('.backup'):
            continue
            
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if '<form' in content:
            form_files.append(file)
    
    print(f"Found {len(form_files)} files with forms to update\n")
    
    for file in form_files:
        print(f"Updating {file.name}...")
        
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Update form tag for Netlify
        # Remove mailto action and add netlify attribute
        content = re.sub(
            r'<form class="contact-form" action="mailto:info@akmcyber.com" method="POST" enctype="text/plain">',
            '<form class="contact-form" name="contact" method="POST" data-netlify="true" data-netlify-honeypot="bot-field">',
            content
        )
        
        # Add honeypot field right after form opening
        if 'data-netlify="true"' in content and 'bot-field' not in content:
            # Find where to insert honeypot
            form_start = content.find('<form class="contact-form"')
            if form_start != -1:
                form_tag_end = content.find('>', form_start) + 1
                honeypot = '''
                        <input type="hidden" name="form-name" value="contact">
                        <p class="hidden">
                            <label>Don't fill this out if you're human: <input name="bot-field" /></label>
                        </p>'''
                content = content[:form_tag_end] + honeypot + content[form_tag_end:]
        
        # Update button type from button to submit
        content = re.sub(
            r'<button type="button"([^>]*>Submit)',
            r'<button type="submit"\1',
            content
        )
        
        # Add success page redirect (optional but recommended)
        # You'll need to create a thank-you.html page
        content = re.sub(
            r'data-netlify="true"',
            r'data-netlify="true" action="/thank-you"',
            content
        )
        
        # Save if changed
        if content != original_content:
            with open(file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ Updated form for Netlify")
        else:
            print(f"  ℹ️  No changes needed")
    
    print("\n✅ Form updates complete!")
    print("\nNext steps:")
    print("1. Create a thank-you.html page for form submissions")
    print("2. Deploy to Netlify")
    print("3. Forms will automatically appear in Netlify dashboard under 'Forms'")
    print("4. You can set up email notifications in Netlify Forms settings")

def create_thank_you_page():
    """Create a simple thank you page for form submissions"""
    
    thank_you_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Preconnect to external domains for faster loading -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="preconnect" href="https://unpkg.com">
    <link rel="preconnect" href="https://cdn.tailwindcss.com">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thank You - AKM SecureKey</title>
    <meta name="description" content="Thank you for contacting AKM SecureKey. We'll be in touch soon.">
    
    <!-- Favicon -->
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
    
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest/dist/umd/lucide.js"></script>
    
    <!-- Pure Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        'akm-black': '#000000',
                        'akm-white': '#ffffff',
                    },
                    fontFamily: {
                        'inter': ['Inter', 'sans-serif'],
                    }
                }
            }
        }
    </script>
</head>
<body class="font-inter bg-gray-50">
    <div class="min-h-screen flex items-center justify-center px-4">
        <div class="max-w-md w-full text-center">
            <div class="bg-white p-8 rounded-lg shadow-lg">
                <div class="mb-6">
                    <i data-lucide="check-circle" class="w-16 h-16 text-green-500 mx-auto"></i>
                </div>
                <h1 class="text-3xl font-bold text-gray-900 mb-4">Thank You!</h1>
                <p class="text-gray-600 mb-8">
                    Your message has been received. We'll get back to you within 24 hours.
                </p>
                <a href="/" class="inline-flex items-center gap-2 bg-black text-white px-6 py-3 font-semibold hover:bg-gray-800 transition-colors">
                    <i data-lucide="arrow-left" class="w-4 h-4"></i>
                    Back to Home
                </a>
            </div>
        </div>
    </div>
    
    <script>
        // Initialize Lucide icons
        lucide.createIcons();
        
        // Redirect to home after 5 seconds
        setTimeout(() => {
            window.location.href = '/';
        }, 5000);
    </script>
</body>
</html>'''
    
    with open('thank-you.html', 'w', encoding='utf-8') as f:
        f.write(thank_you_content)
    
    print("\n✅ Created thank-you.html page")

if __name__ == "__main__":
    print("🔧 Setting up forms for Netlify...\n")
    
    # Update forms
    update_forms_for_netlify()
    
    # Create thank you page
    create_thank_you_page()
    
    print("\n📋 IMPORTANT NETLIFY SETUP NOTES:")
    print("="*50)
    print("1. Forms will work automatically when deployed to Netlify")
    print("2. No server-side code needed!")
    print("3. Submissions appear in Netlify dashboard > Forms")
    print("4. Set up email notifications:")
    print("   - Go to Site settings > Forms > Form notifications")
    print("   - Add your email to receive submissions")
    print("5. Forms are protected by Netlify's spam filters")
    print("6. Free tier includes 100 form submissions/month")
    print("\n✅ Your site is now ready for Netlify deployment!")