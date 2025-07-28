# AKM Secure Website Rebuild

Welcome to the AKM Secure rebuild project.

This site is being redesigned using **Bootstrap 5** for a modern, monochromatic, defense-tech-inspired look. You will find 1:1 content extracted from the original site stored in `.txt` files under the `/content` folder. Do **not generate or modify any content**. Use the exact copy provided.

## 🚀 Quick Start

1. **Development Server**
   ```bash
   # Start a local server (Python 3)
   python3 -m http.server 8000
   ```
   Then open `http://localhost:8000` in your browser.

2. **QA Tools** (available in development mode):
   - **Accessibility Checker**: `?debug=a11y`
   - **Performance Checker**: `?debug=perf`
   - **Link Checker**: Automatically runs in development

---

## 📁 Folder Structure

/content
├── home.txt
├── about.txt
├── contact.txt
├── solutions/
│   ├── resilient-key-protection.txt
│   ├── seamless-integration.txt
│   ├── streamlined-compliance.txt
├── industries/
│   ├── mining.txt
│   ├── financial-services.txt
│   ├── government.txt
│   ├── chemical-processing.txt
│   ├── pharmaceuticals.txt
│   ├── aerospace-defense.txt
│   ├── transportation.txt
│   ├── utilities.txt
│   ├── manufacturing.txt
│   ├── energy.txt

Each `.txt` file contains clean, structured text content for its respective page or subpage.

---

## 🔐 Important Rules

- **No content creation or rewriting**. All copy is client-supplied and final.
- Only use content from the `/content` folder.
- Preserve all headings, lists, CTAs, quotes, and labels.
- Do not alter the copy or try to "improve" it.
- This is a UX/UI rebuild only — design system and layout changes are allowed.

---

## 🎨 Design Guidelines

- Monochromatic palette inspired by **Palantir** and **Anduril**.
- Use **Bootstrap 5** (CDN or local).
- Focus on clean typography, dark backgrounds, minimalistic UI.
- Mobile-first responsive layout using Bootstrap's grid system.
- Use `.container` for fixed-width containers or `.container-fluid` for full-width.
- Use Bootstrap's spacing utilities for consistent padding/margins.
- Follow Bootstrap's component patterns where possible.

---

## 🧠 Development Guidelines

### File Structure
```
/
├── index.html              # Homepage
├── pages/                  # Other pages
│   ├── about.html
│   ├── solutions/
│   └── industries/
├── css/
│   ├── theme.css          # Custom styles
│   └── debug.css          # Debug styles (dev only)
├── js/
│   ├── main.js            # Main JavaScript
│   ├── mobile-first.js     # Mobile navigation
│   └── qa-*.js            # QA tools (dev only)
└── content/               # Source content (1:1 from client)
```

### Coding Standards
- Use semantic HTML5 elements
- Follow Bootstrap 5's utility-first approach
- Keep custom CSS minimal (prefer Bootstrap utilities)
- Use Bootstrap's JavaScript components when possible
- Ensure all interactive elements are keyboard accessible
- Add appropriate ARIA attributes for complex components

### QA Process
1. **Accessibility**
   - Run with `?debug=a11y`
   - Fix all errors before committing
   - Address warnings and notices when possible

2. **Performance**
   - Run with `?debug=perf`
   - Check for render-blocking resources
   - Optimize images and assets
   - Review performance metrics

3. **Links**
   - Automatic check in development
   - Fix all broken links
   - Ensure external links open in new tabs

---

## ✅ Development Tasks

### High Priority
1. Implement responsive layouts for all pages using `/content/**/*.txt`
2. Ensure all interactive elements are keyboard accessible
3. Optimize images and assets for web
4. Fix any issues reported by the QA tools

### Components to Build/Update
- [ ] Main navigation (mobile-friendly)
- [ ] Footer with site links
- [ ] Solution cards
- [ ] Testimonial carousel
- [ ] Contact forms
- [ ] Industry-specific page templates

### QA Checklist
- [ ] All pages pass accessibility checks
- [ ] No console errors
- [ ] Responsive on all screen sizes
- [ ] All links work correctly
- [ ] Images are optimized
- [ ] Performance metrics meet targets

---

## 🛠 Development Workflow

1. **Setup**
   ```bash
   git clone [repository-url]
   cd akmsecure
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make changes**
   - Follow the coding standards
   - Keep commits atomic
   - Write clear commit messages

4. **Test your changes**
   - Check accessibility with `?debug=a11y`
   - Verify performance with `?debug=perf`
   - Test on multiple devices

5. **Create a pull request**
   - Reference any related issues
   - Include screenshots if applicable
   - Request review from a team member

## 🧩 Future Steps

- [ ] Implement a design system
- [ ] Add CMS integration (e.g., Sanity, Strapi)
- [ ] Set up automated testing
- [ ] Implement CI/CD pipeline

## 📝 Notes for Developers

- Always refer to `/content/**` for source content
- Keep custom CSS minimal (use Bootstrap utilities first)
- Document any complex components or patterns
- Follow semantic HTML5 structure
- Ensure all interactive elements are keyboard accessible

## 📩 Questions?

For any questions, please refer to:
1. The content in `/content/**`
2. The QA tools (`?debug=a11y` and `?debug=perf`)
3. Bootstrap 5 documentation
4. Your team lead if you're still unsure
