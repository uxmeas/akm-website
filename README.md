# AKM Secure Website Rebuild (Cursor Project Instructions)

Welcome to the AKM Secure rebuild project.

This site is being redesigned using **Tailwind CSS** for a modern, monochromatic, defense-tech-inspired look. You will find 1:1 content extracted from the original site stored in `.txt` files under the `/content` folder. Do **not generate or modify any content**. Use the exact copy provided.

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
- Use **Tailwind CSS** (CDN or CLI).
- Focus on clean typography, dark backgrounds, minimalistic UI.
- Mobile-first responsive layout.
- Use `w-7xl` (1280px max width) for main content containers.
- Center content with consistent padding/margins.

---

## 🧠 AI Instructions (for Cursor)

When editing or building files:

- Read the content in `/content/**` as source of truth.
- If building a layout or template, refer to filename context (e.g. `mining.txt` → `pages/industries/mining.html`).
- When generating HTML, use semantic tags (`<section>`, `<article>`, `<nav>`, etc.)
- Use consistent component naming if using partials or templates.

---

## ✅ Example Tasks You Can Help With

1. Generate a new responsive homepage layout using `/content/home.txt`.
2. Build mobile-first industry pages based on files in `/content/industries/`.
3. Extract navigation and footer links from any `.txt` to a `navbar.html` and `footer.html` partial.
4. Create Tailwind-based CTA components using the “Get Started with AKM SecureKey” sections.
5. Help validate semantic HTML structure, accessibility, and responsiveness.

---

## 🧩 Future Steps

- A design system will be introduced later.
- CMS integration (like Sanity or Strapi) may come post-launch.
- Right now: focus on layout, component structure, and accurate rendering of content.

---

## 📩 Questions?

Ping the team lead via comments or task description. Use Git for version control, and always refer back to `/content/**` before suggesting changes.
