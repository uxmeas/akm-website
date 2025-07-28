# AKM Secure - Project Onboarding Guide

## Project Overview (Updated: July 27, 2025)
AKM Secure is a modern, mobile-first website for a cybersecurity company specializing in operational technology (OT) security. We're currently implementing a major refactor to better utilize Bootstrap 5's utility classes while maintaining custom design elements.

### Current Focus
- **Refactoring**: Converting custom layouts to Bootstrap 5 utility classes
- **Performance**: Optimizing CSS and JavaScript
- **Accessibility**: Ensuring WCAG 2.1 AA compliance
- **Consistency**: Standardizing section structures and spacing

### Recent Changes
- Refactored Hero and Solutions sections to use Bootstrap 5 utilities
- Added `theme.css` for custom design enhancements
- Implemented consistent section spacing and responsive behavior
- Added smooth scrolling and scroll-triggered animations

## Technology Stack

### Core Technologies
- **HTML5**: Semantic markup with accessibility in mind
- **CSS3**: Custom properties (variables) for theming, Flexbox, and Grid
- **JavaScript**: Vanilla JS for interactivity with Intersection Observer API
- **Bootstrap 5**: Used as a foundation with strategic customization
  - Primarily using utility classes for layout
  - Custom theming via CSS variables
  - Minimal custom CSS overrides

### Development Tools
- **Git**: Version control
- **VS Code**: Recommended editor with extensions (ESLint, Prettier, Live Server)
- **Node.js**: For build processes (if needed in the future)
- **Lighthouse**: For performance and accessibility audits

## Project Structure

```
akmsecure-2025-07-27/
├── assets/
│   ├── images/      # All image assets
│   ├── logos/       # Brand logos and icons
│   └── fonts/       # Custom fonts
├── css/
│   ├── theme.css         # Custom design enhancements
│   ├── accessibility.css # Accessibility enhancements
│   └── styles.css        # Legacy styles (being phased out)
├── js/
│   └── mobile-first.js   # Main JavaScript (ES6+)
├── pages/           # Additional HTML pages
├── index.html       # Homepage (currently being refactored)
└── README.md        # Project documentation
```

## Design System

### Color Palette (CSS Variables)
Colors are defined in `:root` and can be overridden for dark/light themes:

```css
:root {
  --bs-primary: #2563eb;      /* Primary brand color */
  --bs-primary-dark: #1d4ed8;  /* 10% darker */
  --bs-primary-darker: #1e40af; /* 20% darker */
  --bs-dark: #0f172a;         /* Dark background */
  --bs-light: #f8fafc;        /* Light background */
  --bs-body-color: #1e293b;   /* Default text */
  --bs-body-bg: #ffffff;      /* Default background */
}

[data-bs-theme="dark"] {
  --bs-body-color: #e2e8f0;
  --bs-body-bg: #0f172a;
  /* Additional dark theme overrides */
}
```

### Typography
- **Primary Font**: Inter (self-hosted)
- **Base Font Size**: 16px (1rem)
- **Type Scale**: Using Bootstrap's responsive typography

**Example Usage:**
```html
<h1 class="display-3 fw-bold">Large Heading</h1>
<h2 class="display-5">Medium Heading</h2>
<p class="lead">Introductory text</p>
<p>Body text</p>
<small class="text-muted">Secondary text</small>
```

### Spacing System
Using Bootstrap's spacing utilities based on `$spacer` (1rem = 16px by default):

```scss
// Bootstrap's default spacers
$spacer: 1rem;
$spacers: (
  0: 0,
  1: $spacer * .25,    // 4px
  2: $spacer * .5,     // 8px
  3: $spacer,          // 16px
  4: $spacer * 1.5,    // 24px
  5: $spacer * 3,      // 48px
  6: $spacer * 4.5,    // 72px
  7: $spacer * 6,      // 96px
  8: $spacer * 7.5     // 120px
);
```

**Usage Examples:**
- `mt-3`: margin-top: 1rem
- `py-4`: padding-top & bottom: 1.5rem
- `px-lg-5`: padding-left & right: 3rem on lg+ screens

## Development Workflow

### Current State (July 2025)
We're in the middle of a major refactor to standardize on Bootstrap 5's utility classes. The following sections have been updated:

✅ **Completed**
- Hero section
- Solutions section with feature cards
- Base typography and spacing
- Theme configuration

⏳ **In Progress**
- Features/Benefits section
- Testimonials section
- Final CTA section
- Footer

### Branching Strategy
- `main`: Production-ready code
- `staging`: Pre-production testing
- `feature/*`: New features (e.g., `feature/refactor-sections`)
- `fix/*`: Bug fixes
- `docs/*`: Documentation updates

### Commit Message Convention
```
type(scope): description

[optional body]

[optional footer]
```

**Types**: feat, fix, docs, style, refactor, test, chore

## Accessibility Standards

### Key Requirements
- WCAG 2.1 AA compliance
- Keyboard navigation
- Screen reader compatibility
- Reduced motion preferences
- High contrast mode support

### Testing
- Keyboard navigation
- Screen readers (VoiceOver, NVDA, JAWS)
- Color contrast checkers
- Lighthouse audits

## Performance Optimization

### Current Optimizations
- Lazy loading for images and iframes
- Preloading critical resources
- Minimal JavaScript with progressive enhancement
- Optimized animations with `prefers-reduced-motion`

### Areas for Improvement
- Image optimization
- JavaScript bundle size
- Critical CSS extraction
- Service worker implementation

## Getting Started

### Local Development Setup
1. Clone the repository
2. Install Live Server in VS Code (or use your preferred local server)
3. Open the project folder in VS Code
4. Start Live Server (usually `cmd+shift+P` > "Live Server: Open with Live Server")

### Development Commands
```bash
# Install dependencies (if any)
npm install

# Build assets (if configured)
npm run build

# Start development server
npm run dev
```

### Code Style
- Use Bootstrap 5 utility classes for layout and spacing
- Keep custom CSS minimal and focused on design enhancements
- Follow BEM naming for custom components
- Use semantic HTML5 elements

### Build Process
Currently using vanilla HTML/CSS/JS. Future build process may include:
- CSS preprocessing (Sass/PostCSS)
- JavaScript bundling (esbuild/Rollup)
- Asset optimization

## Common Tasks

### Adding a New Section
1. Use the following section template:

```html
<!-- Section Template -->
<section class="py-6 py-lg-8 bg-light text-dark">
  <div class="container-xxl">
    <div class="row justify-content-center text-center mb-5">
      <div class="col-lg-8">
        <span class="d-inline-block text-uppercase fw-bold text-primary mb-3">Section Eyebrow</span>
        <h2 class="display-4 fw-bold mb-3">Section Heading</h2>
        <p class="lead text-muted">Section subtitle or description</p>
      </div>
    </div>
    
    <!-- Section Content -->
    <div class="row g-4">
      <!-- Content goes here -->
    </div>
  </div>
</section>
```

### Theming
- Use `data-bs-theme="dark"` for dark sections
- Toggle between themes with JavaScript if needed
- Test contrast ratios for accessibility

### Styling Components
1. Use existing CSS variables for colors and spacing
2. Follow BEM naming convention for new components
3. Add responsive styles using mobile-first approach

### Adding JavaScript Functionality
1. Add event listeners in `mobile-first.js`
2. Use `data-*` attributes for behavior hooks
3. Ensure graceful degradation

## Troubleshooting

### Common Issues
- **Layout Shifts**: Ensure all images have explicit `width` and `height` attributes
- **Bootstrap Overrides**: Use `!important` sparingly; prefer higher specificity
- **JavaScript Errors**: Check browser console for any issues
- **Accessibility**: Use browser dev tools for accessibility audits

### Performance Tips
- Optimize images before adding to `assets/images/`
- Use `loading="lazy"` for below-the-fold images
- Minimize custom CSS in favor of Bootstrap utilities
- Consider critical CSS for above-the-fold content

### Browser Support
- Chrome (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Edge (latest 2 versions)
- Mobile Safari (iOS 13+)
- Chrome for Android

## Contact
For questions or support, contact:
- Project Lead: [Your Name]
- Email: [Your Email]
- GitHub: [Your GitHub Username]

## License
[Specify License - e.g., MIT, Proprietary]
