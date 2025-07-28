/**
 * AKM Secure - Accessibility Checker
 * 
 * This script performs an accessibility audit of the page and reports any issues.
 * It checks for common accessibility problems including:
 * - Missing alt text on images
 * - Missing form labels
 * - Insufficient color contrast
 * - Missing ARIA attributes
 * - Keyboard navigation issues
 * - Semantic HTML structure
 */

class AccessibilityChecker {
    constructor() {
        this.results = {
            errors: [],
            warnings: [],
            notices: [],
            contrastIssues: [],
            keyboardIssues: [],
            ariaIssues: [],
            headingStructure: []
        };
        
        // Minimum contrast ratio for normal text (WCAG AA)
        this.minContrastRatio = 4.5;
        
        // Elements that should have alt text
        this.elementsNeedingAlt = ['img', 'area', 'input[type="image"]'];
        
        // Interactive elements that should be focusable
        this.interactiveElements = [
            'a[href]', 'button', 'input', 'select', 'textarea',
            '[tabindex]', '[contenteditable]', '[role="button"]',
            '[role="link"]', '[role="checkbox"]', '[role="radio"]',
            '[role="tab"]', '[role="menuitem"]'
        ];
        
        // ARIA roles that require specific attributes
        this.ariaRoleRequirements = {
            'button': ['aria-label', 'aria-labelledby', 'title'],
            'link': ['aria-label', 'aria-labelledby', 'title'],
            'img': ['aria-label', 'aria-labelledby', 'title'],
            'checkbox': ['aria-checked'],
            'radio': ['aria-checked'],
            'tab': ['aria-selected'],
            'tabpanel': ['aria-labelledby'],
            'combobox': ['aria-expanded', 'aria-controls'],
            'dialog': ['aria-labelledby', 'aria-label']
        };
    }
    
    // Main method to run all accessibility checks
    runAllChecks() {
        this.checkImages();
        this.checkForms();
        this.checkHeadings();
        this.checkLandmarks();
        this.checkInteractiveElements();
        this.checkAria();
        this.checkContrast();
        this.checkKeyboardNavigation();
        
        this.showResults();
    }
    
    // Check for missing alt text on images
    checkImages() {
        const images = document.querySelectorAll(this.elementsNeedingAlt.join(','));
        
        images.forEach(img => {
            const alt = img.getAttribute('alt');
            const role = img.getAttribute('role');
            const isDecorative = img.getAttribute('aria-hidden') === 'true' || 
                               img.getAttribute('role') === 'presentation' || 
                               img.getAttribute('role') === 'none';
            
            // Skip decorative images
            if (isDecorative) return;
            
            // Check for missing alt text
            if (!alt && alt !== '') {
                this.results.errors.push({
                    type: 'Missing alt attribute',
                    element: img,
                    message: `Image is missing an alt attribute: ${img.outerHTML.substring(0, 100)}`,
                    selector: this.getSelector(img)
                });
            } 
            // Check for empty alt on non-decorative images
            else if (alt === '' && !isDecorative) {
                this.results.warnings.push({
                    type: 'Empty alt on non-decorative image',
                    element: img,
                    message: 'Image has empty alt text but appears to be informative',
                    selector: this.getSelector(img)
                });
            }
            
            // Check for suspicious alt text
            if (alt && (alt.toLowerCase().includes('image of') || 
                        alt.toLowerCase().includes('picture of') ||
                        alt.toLowerCase().includes('graphic of'))) {
                this.results.notices.push({
                    type: 'Suspicious alt text',
                    element: img,
                    message: 'Alt text may be redundant (contains "image of" or similar)',
                    selector: this.getSelector(img)
                });
            }
        });
    }
    
    // Check form elements for proper labels
    checkForms() {
        const formElements = document.querySelectorAll('input, select, textarea');
        
        formElements.forEach(el => {
            const type = el.type.toLowerCase();
            const id = el.id;
            const name = el.name;
            const label = el.labels && el.labels.length > 0 ? el.labels[0] : null;
            const ariaLabel = el.getAttribute('aria-label') || el.getAttribute('aria-labelledby');
            const title = el.title;
            
            // Skip hidden inputs and buttons
            if (type === 'hidden' || type === 'submit' || type === 'button' || type === 'reset') {
                return;
            }
            
            // Check for missing labels
            if (!label && !ariaLabel && !title && !el.hasAttribute('aria-hidden')) {
                this.results.errors.push({
                    type: 'Missing form label',
                    element: el,
                    message: `Form element is missing a label: ${el.outerHTML.substring(0, 100)}`,
                    selector: this.getSelector(el)
                });
            }
            
            // Check for placeholder as label
            if (el.placeholder && !label && !ariaLabel && !title) {
                this.results.warnings.push({
                    type: 'Placeholder used as label',
                    element: el,
                    message: 'Placeholder text should not be used as a label',
                    selector: this.getSelector(el)
                });
            }
        });
    }
    
    // Check heading hierarchy
    checkHeadings() {
        const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6, [role="heading"]'));
        const headingLevels = [];
        let previousLevel = 0;
        
        headings.forEach((heading, index) => {
            let level;
            
            // Get heading level
            if (heading.tagName.match(/^H[1-6]$/i)) {
                level = parseInt(heading.tagName.charAt(1), 10);
            } else if (heading.hasAttribute('aria-level')) {
                level = parseInt(heading.getAttribute('aria-level'), 10);
            } else {
                level = 2; // Default if role="heading" without aria-level
            }
            
            headingLevels.push({ element: heading, level });
            
            // Check for skipped heading levels
            if (index > 0 && level > previousLevel + 1) {
                this.results.warnings.push({
                    type: 'Skipped heading level',
                    element: heading,
                    message: `Heading level jumps from ${previousLevel} to ${level}`,
                    selector: this.getSelector(heading)
                });
            }
            
            previousLevel = level;
        });
        
        // Check for multiple h1 elements (not always an error, but worth noting)
        const h1Count = document.querySelectorAll('h1').length;
        if (h1Count > 1) {
            this.results.notices.push({
                type: 'Multiple h1 elements',
                message: `Found ${h1Count} h1 elements on the page`
            });
        }
        
        this.results.headingStructure = headingLevels;
    }
    
    // Check landmark regions
    checkLandmarks() {
        const landmarks = [
            'banner',
            'navigation',
            'main',
            'complementary',
            'contentinfo',
            'search',
            'form',
            'region'
        ];
        
        landmarks.forEach(landmark => {
            const elements = document.querySelectorAll(`[role="${landmark}"]`);
            
            // Check for multiple landmarks of the same type without labels
            if (elements.length > 1) {
                elements.forEach((el, index) => {
                    const label = el.getAttribute('aria-label') || el.getAttribute('aria-labelledby');
                    if (!label) {
                        this.results.warnings.push({
                            type: 'Unlabeled landmark',
                            element: el,
                            message: `Multiple ${landmark} landmarks found without unique labels`,
                            selector: this.getSelector(el)
                        });
                    }
                });
            }
        });
        
        // Check for main landmark
        const main = document.querySelector('main, [role="main"]');
        if (!main) {
            this.results.warnings.push({
                type: 'Missing main landmark',
                message: 'Page is missing a main landmark (main or role="main")'
            });
        }
    }
    
    // Check interactive elements
    checkInteractiveElements() {
        const interactiveElements = document.querySelectorAll(this.interactiveElements.join(','));
        
        interactiveElements.forEach(el => {
            // Skip elements that are hidden or have negative tabindex
            if (this.isHidden(el) || el.tabIndex < 0) {
                return;
            }
            
            // Check for focusable elements without keyboard support
            if (el.tagName === 'DIV' && el.getAttribute('role') === 'button' && 
                !el.getAttribute('tabindex')) {
                this.results.errors.push({
                    type: 'Missing tabindex',
                    element: el,
                    message: 'Custom button is missing tabindex attribute',
                    selector: this.getSelector(el)
                });
            }
            
            // Check for non-interactive elements with interactive roles
            if (el.getAttribute('role') && !this.isInteractiveElement(el)) {
                this.results.warnings.push({
                    type: 'Non-interactive element with interactive role',
                    element: el,
                    message: `Element has role="${el.getAttribute('role')}" but is not keyboard focusable`,
                    selector: this.getSelector(el)
                });
            }
        });
    }
    
    // Check ARIA attributes
    checkAria() {
        // Check for required ARIA attributes based on role
        Object.entries(this.ariaRoleRequirements).forEach(([role, requiredAttrs]) => {
            const elements = document.querySelectorAll(`[role="${role}"]`);
            
            elements.forEach(el => {
                requiredAttrs.forEach(attr => {
                    if (!el.hasAttribute(attr)) {
                        this.results.errors.push({
                            type: 'Missing required ARIA attribute',
                            element: el,
                            message: `Element with role="${role}" is missing required attribute: ${attr}`,
                            selector: this.getSelector(el)
                        });
                    }
                });
                
                // Check for invalid ARIA values
                if (role === 'checkbox' || role === 'radio') {
                    const checked = el.getAttribute('aria-checked');
                    if (checked && !['true', 'false', 'mixed', 'undefined'].includes(checked)) {
                        this.results.errors.push({
                            type: 'Invalid ARIA attribute value',
                            element: el,
                            message: `Invalid aria-checked value: ${checked}`,
                            selector: this.getSelector(el)
                        });
                    }
                }
            });
        });
        
        // Check for invalid ARIA attributes
        const elementsWithAria = document.querySelectorAll('[aria-]');
        const validAriaAttrs = [
            'aria-activedescendant', 'aria-atomic', 'aria-autocomplete', 'aria-busy',
            'aria-checked', 'aria-colcount', 'aria-colindex', 'aria-colspan', 'aria-controls',
            'aria-current', 'aria-describedby', 'aria-details', 'aria-disabled', 'aria-dropeffect',
            'aria-errormessage', 'aria-expanded', 'aria-flowto', 'aria-grabbed', 'aria-haspopup',
            'aria-hidden', 'aria-invalid', 'aria-keyshortcuts', 'aria-label', 'aria-labelledby',
            'aria-level', 'aria-live', 'aria-modal', 'aria-multiline', 'aria-multiselectable',
            'aria-orientation', 'aria-owns', 'aria-placeholder', 'aria-posinset', 'aria-pressed',
            'aria-readonly', 'aria-relevant', 'aria-required', 'aria-roledescription',
            'aria-rowcount', 'aria-rowindex', 'aria-rowspan', 'aria-selected', 'aria-setsize',
            'aria-sort', 'aria-valuemax', 'aria-valuemin', 'aria-valuenow', 'aria-valuetext'
        ];
        
        elementsWithAria.forEach(el => {
            Array.from(el.attributes).forEach(attr => {
                if (attr.name.startsWith('aria-') && !validAriaAttrs.includes(attr.name)) {
                    this.results.warnings.push({
                        type: 'Invalid ARIA attribute',
                        element: el,
                        message: `Invalid ARIA attribute: ${attr.name}`,
                        selector: this.getSelector(el)
                    });
                }
            });
        });
        
        // Check for ARIA attributes on elements that don't support them
        const nonInteractiveElements = document.querySelectorAll('div, span, p, h1, h2, h3, h4, h5, h6');
        const interactiveRoles = ['button', 'link', 'checkbox', 'radio', 'tab', 'menuitem'];
        
        nonInteractiveElements.forEach(el => {
            const role = el.getAttribute('role');
            if (role && interactiveRoles.includes(role) && !this.isInteractiveElement(el)) {
                this.results.warnings.push({
                    type: 'Non-interactive element with interactive role',
                    element: el,
                    message: `Element has role="${role}" but is not keyboard focusable`,
                    selector: this.getSelector(el)
                });
            }
        });
    }
    
    // Check color contrast
    checkContrast() {
        // This is a simplified version - a real implementation would need to
        // calculate the contrast ratio between foreground and background colors
        // For now, we'll just check for low contrast text based on color and background-color
        const elements = document.querySelectorAll('p, span, div, h1, h2, h3, h4, h5, h6, a, li, td, th, label, input, textarea, select, button');
        
        elements.forEach(el => {
            // Skip hidden elements and elements with no text content
            if (this.isHidden(el) || !el.textContent.trim()) {
                return;
            }
            
            // Skip elements with background images (hard to calculate contrast)
            const style = window.getComputedStyle(el);
            if (style.backgroundImage !== 'none') {
                return;
            }
            
            // This is a placeholder - in a real implementation, you would:
            // 1. Get the computed background color (handling transparency)
            // 2. Get the computed text color
            // 3. Calculate the contrast ratio
            // 4. Compare against WCAG guidelines
            
            // For now, we'll just check for obviously low contrast combinations
            const textColor = style.color;
            const bgColor = style.backgroundColor;
            
            // Simple check for light text on light background or dark on dark
            if ((this.isLightColor(textColor) && this.isLightColor(bgColor)) ||
                (!this.isLightColor(textColor) && !this.isLightColor(bgColor))) {
                this.results.contrastIssues.push({
                    type: 'Low contrast text',
                    element: el,
                    message: 'Text may have insufficient color contrast',
                    selector: this.getSelector(el),
                    textColor,
                    bgColor
                });
            }
        });
    }
    
    // Check keyboard navigation
    checkKeyboardNavigation() {
        // Check for focusable elements with no visible focus style
        const focusableElements = document.querySelectorAll('a[href], button, input, select, textarea, [tabindex]');
        
        focusableElements.forEach(el => {
            // Skip elements that are hidden or have negative tabindex
            if (this.isHidden(el) || (el.tabIndex && el.tabIndex < 0)) {
                return;
            }
            
            // Check for focus styles
            const style = window.getComputedStyle(el);
            const hasFocusStyle = style.outlineStyle !== 'none' || 
                               style.outlineWidth !== '0px' ||
                               style.boxShadow !== 'none';
            
            if (!hasFocusStyle) {
                this.results.keyboardIssues.push({
                    type: 'Missing focus style',
                    element: el,
                    message: 'Focusable element has no visible focus style',
                    selector: this.getSelector(el)
                });
            }
            
            // Check for keyboard traps
            if (el.tabIndex > 0) {
                this.results.warnings.push({
                    type: 'Potential keyboard trap',
                    element: el,
                    message: 'Positive tabindex can cause keyboard navigation issues',
                    selector: this.getSelector(el)
                });
            }
        });
        
        // Check for skip links
        const skipLinks = document.querySelectorAll('a[href^="#"], a[href^="/#"]');
        let hasSkipLink = false;
        
        skipLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href === '#main' || href === '#content' || href === '/#main' || href === '/#content') {
                hasSkipLink = true;
            }
        });
        
        if (!hasSkipLink) {
            this.results.notices.push({
                type: 'Missing skip link',
                message: 'Consider adding a skip link to allow keyboard users to skip to main content'
            });
        }
    }
    
    // Helper to check if an element is hidden
    isHidden(el) {
        if (!el) return true;
        
        const style = window.getComputedStyle(el);
        return style.display === 'none' || 
               style.visibility === 'hidden' || 
               style.opacity === '0' ||
               el.offsetParent === null;
    }
    
    // Helper to check if an element is interactive
    isInteractiveElement(el) {
        if (!el) return false;
        
        const tagName = el.tagName.toLowerCase();
        const role = el.getAttribute('role');
        const interactiveRoles = ['button', 'link', 'checkbox', 'radio', 'tab', 'menuitem'];
        
        return (
            tagName === 'a' ||
            tagName === 'button' ||
            tagName === 'input' ||
            tagName === 'select' ||
            tagName === 'textarea' ||
            (tagName === 'div' && role && interactiveRoles.includes(role)) ||
            el.tabIndex >= 0
        );
    }
    
    // Helper to determine if a color is light
    isLightColor(color) {
        // This is a simplified version - in a real implementation, you would
        // parse the color string and calculate luminance
        if (!color) return false;
        
        // Check for common light colors
        const lightColors = [
            'white', '#fff', '#ffffff', '#f8f9fa', '#f1f1f1',
            'lightgray', 'lightgrey', '#e9ecef', '#dee2e6',
            '#f8f9fa', '#e9ecef', '#dee2e6', '#ced4da'
        ];
        
        return lightColors.includes(color.toLowerCase());
    }
    
    // Helper to get a CSS selector for an element
    getSelector(el) {
        if (!el) return '';
        
        const path = [];
        let current = el;
        
        while (current && current.nodeType === Node.ELEMENT_NODE) {
            let selector = current.nodeName.toLowerCase();
            
            if (current.id) {
                selector += `#${current.id}`;
                path.unshift(selector);
                break;
            } else {
                let sibling = current;
                let siblingCount = 0;
                let siblingIndex = 0;
                
                while (sibling) {
                    if (sibling.nodeType === Node.ELEMENT_NODE && 
                        sibling.nodeName.toLowerCase() === selector) {
                        if (sibling === current) {
                            siblingIndex = siblingCount;
                        }
                        siblingCount++;
                    }
                    sibling = sibling.previousElementSibling;
                }
                
                if (siblingCount > 1) {
                    selector += `:nth-of-type(${siblingIndex + 1})`;
                }
                
                path.unshift(selector);
                current = current.parentNode;
            }
        }
        
        return path.join(' > ');
    }
    
    // Display the results in a user-friendly way
    showResults() {
        const resultsDiv = document.createElement('div');
        resultsDiv.id = 'a11y-results';
        resultsDiv.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 400px;
            max-height: 80vh;
            overflow-y: auto;
            background: white;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 9999;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            font-size: 14px;
            color: #333;
        `;
        
        // Create header
        const header = document.createElement('div');
        header.style.cssText = 'display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;';
        
        const title = document.createElement('h3');
        title.textContent = 'Accessibility Checker';
        title.style.margin = '0 0 10px 0';
        
        const closeBtn = document.createElement('button');
        closeBtn.textContent = '×';
        closeBtn.style.cssText = 'background: none; border: none; font-size: 20px; cursor: pointer;';
        closeBtn.onclick = () => resultsDiv.remove();
        
        header.appendChild(title);
        header.appendChild(closeBtn);
        
        // Create summary
        const summary = document.createElement('div');
        summary.style.marginBottom = '15px';
        
        const errorCount = this.results.errors.length;
        const warningCount = this.results.warnings.length;
        const noticeCount = this.results.notices.length;
        const contrastCount = this.results.contrastIssues.length;
        const keyboardCount = this.results.keyboardIssues.length;
        const ariaCount = this.results.ariaIssues.length;
        
        summary.innerHTML = `
            <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 10px;">
                <span style="background: ${errorCount > 0 ? '#dc3545' : '#28a745'}; color: white; padding: 2px 8px; border-radius: 12px;">
                    Errors: ${errorCount}
                </span>
                <span style="background: ${warningCount > 0 ? '#ffc107' : '#28a745'}; color: ${warningCount > 0 ? '#212529' : 'white'}; padding: 2px 8px; border-radius: 12px;">
                    Warnings: ${warningCount}
                </span>
                <span style="background: #6c757d; color: white; padding: 2px 8px; border-radius: 12px;">
                    Notices: ${noticeCount}
                </span>
                <span style="background: ${contrastCount > 0 ? '#ffc107' : '#28a745'}; color: ${contrastCount > 0 ? '#212529' : 'white'}; padding: 2px 8px; border-radius: 12px;">
                    Contrast: ${contrastCount}
                </span>
                <span style="background: ${keyboardCount > 0 ? '#ffc107' : '#28a745'}; color: ${keyboardCount > 0 ? '#212529' : 'white'}; padding: 2px 8px; border-radius: 12px;">
                    Keyboard: ${keyboardCount}
                </span>
                <span style="background: ${ariaCount > 0 ? '#ffc107' : '#28a745'}; color: ${ariaCount > 0 ? '#212529' : 'white'}; padding: 2px 8px; border-radius: 12px;">
                    ARIA: ${ariaCount}
                </span>
            </div>
            <div style="font-size: 12px; color: #6c757d; margin-top: 10px;">
                Click on an issue to highlight the element on the page
            </div>
        `;
        
        // Create tabs
        const tabs = document.createElement('div');
        tabs.style.cssText = 'display: flex; border-bottom: 1px solid #ddd; margin-bottom: 10px;';
        
        const tabContents = document.createElement('div');
        tabContents.style.minHeight = '200px';
        
        const createTab = (name, content, isActive = false) => {
            const tab = document.createElement('button');
            tab.textContent = name;
            tab.style.cssText = `
                padding: 8px 16px;
                border: none;
                background: none;
                cursor: pointer;
                border-bottom: 2px solid ${isActive ? '#007bff' : 'transparent'};
                margin-right: 5px;
            `;
            
            const tabContent = document.createElement('div');
            tabContent.style.display = isActive ? 'block' : 'none';
            
            if (Array.isArray(content) && content.length > 0) {
                const list = document.createElement('ul');
                list.style.paddingLeft = '20px';
                content.forEach(item => {
                    const li = document.createElement('li');
                    li.style.marginBottom = '8px';
                    
                    if (item.selector) {
                        const code = document.createElement('code');
                        code.textContent = item.message;
                        code.style.display = 'block';
                        code.style.marginTop = '4px';
                        code.style.fontSize = '12px';
                        code.style.color = '#666';
                        code.style.cursor = 'pointer';
                        
                        code.onclick = () => {
                            // Scroll to the element
                            const target = document.querySelector(item.selector);
                            if (target) {
                                target.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                
                                // Highlight the element
                                const prevOutline = target.style.outline;
                                target.style.outline = '2px solid #ff0';
                                
                                // Remove highlight after 2 seconds
                                setTimeout(() => {
                                    target.style.outline = prevOutline;
                                }, 2000);
                            }
                        };
                        
                        li.appendChild(code);
                    } else {
                        li.textContent = item.message || 'No details available';
                    }
                    
                    list.appendChild(li);
                });
                tabContent.appendChild(list);
            } else if (typeof content === 'string') {
                tabContent.innerHTML = content;
            } else {
                tabContent.textContent = 'No issues found.';
            }
            
            tab.onclick = () => {
                // Hide all tab contents
                tabContents.querySelectorAll('div').forEach(div => {
                    div.style.display = 'none';
                });
                // Show this tab's content
                tabContent.style.display = 'block';
                // Update active tab
                tabs.querySelectorAll('button').forEach(btn => {
                    btn.style.borderBottomColor = 'transparent';
                });
                tab.style.borderBottomColor = '#007bff';
            };
            
            return { tab, tabContent };
        };
        
        // Create tabs for each section
        const errorsTab = createTab('Errors', this.results.errors, true);
        const warningsTab = createTab('Warnings', this.results.warnings);
        const noticesTab = createTab('Notices', this.results.notices);
        const contrastTab = createTab('Contrast', this.results.contrastIssues);
        const keyboardTab = createTab('Keyboard', this.results.keyboardIssues);
        const ariaTab = createTab('ARIA', this.results.ariaIssues);
        
        // Only add tabs if they have content
        if (this.results.errors.length > 0) tabs.appendChild(errorsTab.tab);
        if (this.results.warnings.length > 0) tabs.appendChild(warningsTab.tab);
        if (this.results.notices.length > 0) tabs.appendChild(noticesTab.tab);
        if (this.results.contrastIssues.length > 0) tabs.appendChild(contrastTab.tab);
        if (this.results.keyboardIssues.length > 0) tabs.appendChild(keyboardTab.tab);
        if (this.results.ariaIssues.length > 0) tabs.appendChild(ariaTab.tab);
        
        // Add tab contents
        if (this.results.errors.length > 0) tabContents.appendChild(errorsTab.tabContent);
        if (this.results.warnings.length > 0) tabContents.appendChild(warningsTab.tabContent);
        if (this.results.notices.length > 0) tabContents.appendChild(noticesTab.tabContent);
        if (this.results.contrastIssues.length > 0) tabContents.appendChild(contrastTab.tabContent);
        if (this.results.keyboardIssues.length > 0) tabContents.appendChild(keyboardTab.tabContent);
        if (this.results.ariaIssues.length > 0) tabContents.appendChild(ariaTab.tabContent);
        
        // Add a tab for heading structure
        if (this.results.headingStructure.length > 0) {
            const headingStructure = this.results.headingStructure.map(item => ({
                message: `${'#'.repeat(item.level)} ${item.element.textContent.trim() || '[Empty heading]'}`,
                selector: this.getSelector(item.element)
            }));
            
            const headingTab = createTab('Headings', headingStructure);
            tabs.appendChild(headingTab.tab);
            tabContents.appendChild(headingTab.tabContent);
        }
        
        // Assemble the results
        resultsDiv.appendChild(header);
        resultsDiv.appendChild(summary);
        resultsDiv.appendChild(tabs);
        resultsDiv.appendChild(tabContents);
        
        // Add to page
        document.body.appendChild(resultsDiv);
        
        // Add some basic styling
        const style = document.createElement('style');
        style.textContent = `
            #a11y-results button { cursor: pointer; }
            #a11y-results ul { margin: 0; }
            #a11y-results li { margin-bottom: 5px; }
            #a11y-results code { 
                background: #f5f5f5; 
                padding: 2px 4px; 
                border-radius: 3px; 
                font-family: monospace;
            }
            #a11y-results code:hover {
                background: #e9ecef;
                text-decoration: underline;
            }
        `;
        document.head.appendChild(style);
    }
}

// Initialize and run the accessibility checker when the page loads
document.addEventListener('DOMContentLoaded', () => {
    // Only run in development environment or when explicitly enabled
    if (window.location.hostname === 'localhost' || window.location.search.includes('debug=a11y')) {
        const a11yChecker = new AccessibilityChecker();
        a11yChecker.runAllChecks();
    }
});
