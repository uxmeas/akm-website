# SEO & Copywriter Guide for AKM SecureKey Website

## Current SEO Setup ✅

The website is **partially ready** for copywriter edits. Here's what's in place:

### ✅ Ready for Editing (Already Implemented)

1. **Title Tags** - Every page has a unique `<title>` tag
   - Location: Inside `<head>` section
   - Format: `[Page Topic] - AKM SecureKey`
   - Example: `<title>Financial Services (Data Centers with OT) - AKM SecureKey</title>`

2. **Meta Descriptions** - Every page has a unique meta description
   - Location: Inside `<head>` section  
   - Format: `<meta name="description" content="Your description here">`
   - Length: Keep between 150-160 characters

3. **H1 Headings** - Main headlines on each page
   - Location: In page content, usually in hero section
   - Best practice: Only ONE H1 per page

4. **Body Content** - All text content throughout the pages
   - Paragraphs, lists, card content, etc.

5. **Basic Technical SEO**
   - UTF-8 charset encoding ✅
   - Viewport meta tag for mobile ✅
   - Mobile-responsive design ✅

## 🔴 NOT Yet Implemented (Missing for Full SEO)

1. **Open Graph Tags** (for social media sharing)
   ```html
   <meta property="og:title" content="Page Title">
   <meta property="og:description" content="Page description">
   <meta property="og:image" content="image-url.jpg">
   <meta property="og:url" content="page-url">
   ```

2. **Twitter Card Tags**
   ```html
   <meta name="twitter:card" content="summary_large_image">
   <meta name="twitter:title" content="Page Title">
   <meta name="twitter:description" content="Page description">
   ```

3. **Canonical URLs**
4. **Structured Data** (Schema.org)
5. **XML Sitemap**
6. **Robots.txt file**
7. **Alt text for many images**

## 📝 How to Edit SEO Elements

### To Edit Title Tags:
1. Open the HTML file
2. Find `<title>` in the `<head>` section (usually around line 11)
3. Edit the text between `<title>` and `</title>`
4. Keep it under 60 characters
5. Include primary keyword

### To Edit Meta Descriptions:
1. Open the HTML file
2. Find `<meta name="description"` in the `<head>` section (usually around line 12)
3. Edit the content="" value
4. Keep between 150-160 characters
5. Include keywords naturally
6. Make it compelling for clicks

### To Edit H1 Headings:
1. Search for `<h1` in the file
2. Edit the text between `<h1>` and `</h1>`
3. Keep it concise and keyword-rich
4. Only ONE H1 per page!

### To Edit Body Content:
1. Find the relevant section in the HTML
2. Look for `<p>`, `<h2>`, `<h3>`, `<li>` tags
3. Edit the text content
4. Maintain HTML structure

## 🎯 SEO Best Practices for Copywriters

1. **Title Tag Formula:**
   - Primary Keyword | Secondary Keyword - Brand Name
   - Example: "Quantum-Resilient Cybersecurity for Manufacturing - AKM SecureKey"
   - Keep under 60 characters

2. **Meta Description Formula:**
   - Action verb + Value proposition + Keywords + Call to action
   - Example: "Protect your industrial systems with quantum-resilient security. AKM SecureKey delivers zero-trust OT cybersecurity. Learn more."

3. **Keyword Placement:**
   - Title tag (beginning)
   - Meta description
   - H1 heading
   - First paragraph
   - Subheadings (H2, H3)
   - Throughout body naturally

4. **Content Guidelines:**
   - Write for humans first, search engines second
   - Use semantic variations of keywords
   - Include long-tail keywords
   - Answer user intent

## 📋 Quick Checklist for Each Page

- [ ] Unique title tag (under 60 chars)
- [ ] Unique meta description (150-160 chars)
- [ ] One H1 tag per page
- [ ] Keywords in title, meta desc, H1
- [ ] Natural keyword usage in body
- [ ] Internal links to related pages
- [ ] Call-to-action present

## 🚀 Next Steps for Full SEO Implementation

If you need complete SEO functionality, we should add:

1. **Social Media Tags** - For better sharing previews
2. **Structured Data** - For rich snippets in search results
3. **XML Sitemap** - For search engine crawling
4. **Image SEO** - Alt text for all images
5. **URL Structure** - Ensure SEO-friendly URLs

## 📧 Need Help?

The current setup allows you to edit all primary SEO elements (titles, descriptions, content). For adding missing SEO features, additional development work would be needed.