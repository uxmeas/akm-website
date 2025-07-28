/**
 * AKM Secure - Performance Checker
 * 
 * This script analyzes the performance of the page and provides recommendations
 * for improvement. It checks for:
 * - Unoptimized images
 * - Render-blocking resources
 * - Unused CSS/JS
 * - Large DOM size
 * - Unminified assets
 * - Missing caching headers
 * - Uncompressed assets
 */

class PerformanceChecker {
    constructor() {
        this.results = {
            issues: [],
            warnings: [],
            notices: [],
            metrics: {}
        };
        
        // Performance thresholds
        this.thresholds = {
            imageSize: 100, // KB
            domSize: 1500, // Number of nodes
            domDepth: 15, // Maximum recommended depth
            cssSize: 50, // KB
            jsSize: 200, // KB
            fontDisplay: 'swap' // Recommended font-display value
        };
    }
    
    // Main method to run all performance checks
    async runAllChecks() {
        try {
            await this.checkImages();
            this.checkRenderBlocking();
            this.checkDomSize();
            this.checkAssets();
            this.checkFonts();
            this.checkThirdParty();
            this.checkCaching();
            this.calculateMetrics();
            
            this.showResults();
        } catch (error) {
            console.error('Error running performance checks:', error);
            this.results.issues.push({
                type: 'Error',
                message: `Failed to complete performance analysis: ${error.message}`
            });
            this.showResults();
        }
    }
    
    // Check for unoptimized images
    async checkImages() {
        const images = Array.from(document.getElementsByTagName('img'));
        
        for (const img of images) {
            try {
                // Skip data URIs and SVGs
                if (img.src.startsWith('data:') || img.src.endsWith('.svg')) {
                    continue;
                }
                
                // Check for explicit dimensions
                if (!img.hasAttribute('width') || !img.hasAttribute('height')) {
                    this.results.warnings.push({
                        type: 'Missing dimensions',
                        element: img,
                        message: 'Image is missing width and/or height attributes',
                        selector: this.getSelector(img)
                    });
                }
                
                // Check for loading="lazy" on above-the-fold images
                const rect = img.getBoundingClientRect();
                const isAboveTheFold = rect.top < window.innerHeight && 
                                     rect.bottom >= 0 && 
                                     rect.right >= 0 && 
                                     rect.left < window.innerWidth;
                
                if (isAboveTheFold && img.loading === 'lazy') {
                    this.results.warnings.push({
                        type: 'Lazy loading above-the-fold',
                        element: img,
                        message: 'Avoid lazy loading images that are in the viewport on page load',
                        selector: this.getSelector(img)
                    });
                }
                
                // Check for next-gen formats (this is a simple check, not comprehensive)
                const src = img.src.toLowerCase();
                if (!(src.endsWith('.webp') || src.endsWith('.avif'))) {
                    this.results.notices.push({
                        type: 'Consider next-gen formats',
                        element: img,
                        message: 'Consider using WebP or AVIF for better compression',
                        selector: this.getSelector(img)
                    });
                }
                
            } catch (error) {
                console.warn('Error checking image:', img, error);
            }
        }
    }
    
    // Check for render-blocking resources
    checkRenderBlocking() {
        // Check for render-blocking CSS
        const stylesheets = Array.from(document.querySelectorAll('link[rel="stylesheet"]'));
        stylesheets.forEach(link => {
            if (link.media && link.media !== 'all' && link.media !== 'screen') {
                return; // Skip print stylesheets
            }
            
            if (link.disabled) {
                return; // Skip disabled stylesheets
            }
            
            // Check if the stylesheet is render-blocking
            if (!link.media || link.media === 'all' || link.media === 'screen') {
                this.results.issues.push({
                    type: 'Render-blocking CSS',
                    element: link,
                    message: 'Consider inlining critical CSS and deferring non-critical CSS',
                    selector: this.getSelector(link)
                });
            }
        });
        
        // Check for render-blocking JavaScript
        const scripts = Array.from(document.querySelectorAll('script[src]:not([defer]):not([async])'));
        scripts.forEach(script => {
            if (script.hasAttribute('type') && script.type !== 'text/javascript') {
                return; // Skip non-JavaScript scripts
            }
            
            this.results.issues.push({
                type: 'Render-blocking JS',
                element: script,
                message: 'Consider adding defer or async attribute to script',
                selector: this.getSelector(script)
            });
        });
    }
    
    // Check for large DOM size
    checkDomSize() {
        const totalNodes = document.getElementsByTagName('*').length;
        this.results.metrics.domSize = totalNodes;
        
        if (totalNodes > this.thresholds.domSize) {
            this.results.warnings.push({
                type: 'Large DOM size',
                message: `Large DOM detected (${totalNodes} nodes). This can affect performance.`
            });
        }
        
        // Check for deep DOM trees
        const maxDepth = this.getMaxDepth(document.documentElement);
        this.results.metrics.domDepth = maxDepth;
        
        if (maxDepth > this.thresholds.domDepth) {
            this.results.warnings.push({
                type: 'Deep DOM tree',
                message: `Deep DOM tree detected (depth: ${maxDepth}). This can affect performance.`
            });
        }
    }
    
    // Check CSS and JS assets
    checkAssets() {
        // Check for unminified assets
        const resources = performance.getEntriesByType('resource');
        
        resources.forEach(resource => {
            const url = resource.name;
            const extension = url.split('.').pop().toLowerCase();
            
            // Skip data URIs and external resources
            if (url.startsWith('data:') || !url.includes(window.location.hostname)) {
                return;
            }
            
            // Check for unminified CSS/JS
            if ((extension === 'js' || extension === 'css') && 
                !url.includes('.min.') && 
                !url.includes('debug') && 
                !url.includes('qa-')) {
                this.results.warnings.push({
                    type: 'Unminified asset',
                    message: `Consider minifying: ${url}`
                });
            }
            
            // Check for large assets
            if (resource.transferSize > 0) {
                const sizeKB = Math.round(resource.transferSize / 1024);
                
                if (extension === 'css' && sizeKB > this.thresholds.cssSize) {
                    this.results.warnings.push({
                        type: 'Large CSS file',
                        message: `Large CSS file (${sizeKB}KB): ${url}`
                    });
                } else if (extension === 'js' && sizeKB > this.thresholds.jsSize) {
                    this.results.warnings.push({
                        type: 'Large JS file',
                        message: `Large JS file (${sizeKB}KB): ${url}`
                    });
                }
            }
        });
    }
    
    // Check web fonts
    checkFonts() {
        // Check for font-display: swap
        const fontFaces = Array.from(document.styleSheets)
            .flatMap(sheet => {
                try {
                    return Array.from(sheet.cssRules || []);
                } catch (e) {
                    return [];
                }
            })
            .filter(rule => rule.type === CSSRule.FONT_FACE_RULE);
        
        fontFaces.forEach(rule => {
            const style = rule.style;
            const fontDisplay = style.getPropertyValue('font-display');
            
            if (!fontDisplay) {
                this.results.warnings.push({
                    type: 'Missing font-display',
                    message: `Consider adding font-display: ${this.thresholds.fontDisplay} to @font-face rules`
                });
            } else if (fontDisplay !== this.thresholds.fontDisplay) {
                this.results.notices.push({
                    type: 'Suboptimal font-display',
                    message: `Consider using font-display: ${this.thresholds.fontDisplay} for better performance`
                });
            }
        });
    }
    
    // Check third-party resources
    checkThirdParty() {
        const resources = performance.getEntriesByType('resource');
        const thirdParty = [];
        
        resources.forEach(resource => {
            const url = new URL(resource.name);
            
            // Skip data URIs and same-origin resources
            if (url.protocol === 'data:' || url.hostname === window.location.hostname) {
                return;
            }
            
            thirdParty.push({
                url: resource.name,
                initiatorType: resource.initiatorType,
                duration: resource.duration,
                transferSize: resource.transferSize
            });
        });
        
        if (thirdParty.length > 0) {
            this.results.metrics.thirdPartyCount = thirdParty.length;
            
            this.results.notices.push({
                type: 'Third-party resources',
                message: `Found ${thirdParty.length} third-party resources. Consider self-hosting critical resources.`,
                details: thirdParty.map(r => ({
                    url: r.url,
                    type: r.initiatorType,
                    size: r.transferSize ? `${Math.round(r.transferSize / 1024)}KB` : 'N/A',
                    duration: `${Math.round(r.duration)}ms`
                }))
            });
        }
    }
    
    // Check caching headers (simplified client-side check)
    checkCaching() {
        // This is a simplified check - a real implementation would need server access
        const resources = performance.getEntriesByType('resource');
        const cacheable = ['css', 'js', 'woff', 'woff2', 'ttf', 'eot', 'png', 'jpg', 'jpeg', 'webp', 'svg', 'gif'];
        
        resources.forEach(resource => {
            const url = resource.name;
            const extension = url.split('.').pop().toLowerCase();
            
            // Skip non-cacheable resources
            if (!cacheable.includes(extension)) {
                return;
            }
            
            // Skip data URIs and external resources
            if (url.startsWith('data:') || !url.includes(window.location.hostname)) {
                return;
            }
            
            // Check for cache-busting query parameters
            if (url.includes('?') || url.includes('&')) {
                this.results.warnings.push({
                    type: 'Cache-busting parameters',
                    message: `Consider using versioned filenames instead of query parameters: ${url}`
                });
            }
        });
    }
    
    // Calculate performance metrics
    calculateMetrics() {
        // Use the Navigation Timing API
        const timing = performance.timing;
        
        if (timing) {
            this.results.metrics.pageLoadTime = timing.loadEventEnd - timing.navigationStart;
            this.results.metrics.domContentLoaded = timing.domContentLoadedEventEnd - timing.navigationStart;
            this.results.metrics.firstPaint = performance.getEntriesByName('first-paint')[0]?.startTime || 0;
            this.results.metrics.firstContentfulPaint = performance.getEntriesByName('first-contentful-paint')[0]?.startTime || 0;
            
            // Check for Largest Contentful Paint (LCP)
            const lcp = performance.getEntriesByType('largest-contentful-paint');
            if (lcp.length > 0) {
                this.results.metrics.lcp = lcp[lcp.length - 1].renderTime || lcp[lcp.length - 1].loadTime;
            }
            
            // Check for Cumulative Layout Shift (CLS)
            const cls = performance.getEntriesByType('layout-shift');
            if (cls.length > 0) {
                this.results.metrics.cls = cls.reduce((sum, entry) => {
                    return sum + entry.value;
                }, 0);
            }
        }
        
        // Check for unused CSS/JS (simplified check)
        const styles = Array.from(document.styleSheets);
        let totalCssSize = 0;
        
        styles.forEach(sheet => {
            try {
                const rules = sheet.cssRules || [];
                totalCssSize += rules.length;
            } catch (e) {
                // Cross-origin stylesheet
            }
        });
        
        this.results.metrics.cssRules = totalCssSize;
        
        if (totalCssSize > 500) {
            this.results.warnings.push({
                type: 'Large CSS codebase',
                message: `Large CSS codebase (${totalCssSize} rules). Consider code splitting or purging unused CSS.`
            });
        }
    }
    
    // Helper to get the maximum depth of the DOM tree
    getMaxDepth(node, depth = 0) {
        if (!node.children || node.children.length === 0) {
            return depth;
        }
        
        let maxDepth = depth;
        for (let i = 0; i < node.children.length; i++) {
            maxDepth = Math.max(maxDepth, this.getMaxDepth(node.children[i], depth + 1));
        }
        
        return maxDepth;
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
        resultsDiv.id = 'perf-results';
        resultsDiv.style.cssText = `
            position: fixed;
            top: 20px;
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
        title.textContent = 'Performance Checker';
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
        
        const issueCount = this.results.issues.length;
        const warningCount = this.results.warnings.length;
        const noticeCount = this.results.notices.length;
        
        summary.innerHTML = `
            <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 10px;">
                <span style="background: ${issueCount > 0 ? '#dc3545' : '#28a745'}; color: white; padding: 2px 8px; border-radius: 12px;">
                    Critical: ${issueCount}
                </span>
                <span style="background: ${warningCount > 0 ? '#ffc107' : '#28a745'}; color: ${warningCount > 0 ? '#212529' : 'white'}; padding: 2px 8px; border-radius: 12px;">
                    Warnings: ${warningCount}
                </span>
                <span style="background: #6c757d; color: white; padding: 2px 8px; border-radius: 12px;">
                    Notices: ${noticeCount}
                </span>
            </div>
            <div style="font-size: 12px; color: #6c757d; margin-top: 10px;">
                Click on an issue to highlight the element on the page
            </div>
        `;
        
        // Create metrics section
        const metrics = document.createElement('div');
        metrics.style.marginBottom = '15px';
        metrics.style.padding = '10px';
        metrics.style.background = '#f8f9fa';
        metrics.style.borderRadius = '4px';
        
        metrics.innerHTML = '<h4 style="margin-top: 0; margin-bottom: 10px;">Performance Metrics</h4>';
        
        const metricsList = document.createElement('ul');
        metricsList.style.margin = '0';
        metricsList.style.paddingLeft = '20px';
        
        if (this.results.metrics.pageLoadTime) {
            metricsList.innerHTML += `<li>Page Load: ${this.results.metrics.pageLoadTime}ms</li>`;
        }
        if (this.results.metrics.domContentLoaded) {
            metricsList.innerHTML += `<li>DOM Content Loaded: ${this.results.metrics.domContentLoaded}ms</li>`;
        }
        if (this.results.metrics.firstContentfulPaint) {
            metricsList.innerHTML += `<li>First Contentful Paint: ${Math.round(this.results.metrics.firstContentfulPaint)}ms</li>`;
        }
        if (this.results.metrics.lcp) {
            metricsList.innerHTML += `<li>Largest Contentful Paint: ${Math.round(this.results.metrics.lcp)}ms</li>`;
        }
        if (this.results.metrics.cls) {
            metricsList.innerHTML += `<li>Cumulative Layout Shift: ${this.results.metrics.cls.toFixed(4)}</li>`;
        }
        if (this.results.metrics.domSize) {
            metricsList.innerHTML += `<li>DOM Size: ${this.results.metrics.domSize} nodes</li>`;
        }
        if (this.results.metrics.domDepth) {
            metricsList.innerHTML += `<li>DOM Depth: ${this.results.metrics.domDepth} levels</li>`;
        }
        if (this.results.metrics.cssRules) {
            metricsList.innerHTML += `<li>CSS Rules: ${this.results.metrics.cssRules}</li>`;
        }
        
        metrics.appendChild(metricsList);
        
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
                        const code = document.createElement('div');
                        code.textContent = item.message;
                        code.style.cursor = 'pointer';
                        code.style.padding = '4px';
                        code.style.borderRadius = '3px';
                        
                        code.onmouseover = () => {
                            const target = document.querySelector(item.selector);
                            if (target) {
                                target.style.outline = '2px solid #ff0';
                            }
                        };
                        
                        code.onmouseout = () => {
                            const target = document.querySelector(item.selector);
                            if (target) {
                                target.style.outline = '';
                            }
                        };
                        
                        code.onclick = () => {
                            const target = document.querySelector(item.selector);
                            if (target) {
                                target.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                target.style.outline = '2px solid #f00';
                                setTimeout(() => {
                                    target.style.outline = '';
                                }, 2000);
                            }
                        };
                        
                        li.appendChild(code);
                        
                        if (item.details) {
                            const details = document.createElement('div');
                            details.style.fontSize = '12px';
                            details.style.color = '#6c757d';
                            details.style.marginTop = '4px';
                            details.style.padding = '4px';
                            details.style.background = '#f8f9fa';
                            details.style.borderRadius = '3px';
                            
                            if (Array.isArray(item.details)) {
                                details.innerHTML = item.details.map(d => 
                                    `<div>${JSON.stringify(d, null, 2)}</div>`
                                ).join('');
                            } else {
                                details.textContent = JSON.stringify(item.details, null, 2);
                            }
                            
                            li.appendChild(details);
                        }
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
        const criticalTab = createTab('Critical', this.results.issues, true);
        const warningsTab = createTab('Warnings', this.results.warnings);
        const noticesTab = createTab('Notices', this.results.notices);
        
        // Only add tabs if they have content
        if (this.results.issues.length > 0) tabs.appendChild(criticalTab.tab);
        if (this.results.warnings.length > 0) tabs.appendChild(warningsTab.tab);
        if (this.results.notices.length > 0) tabs.appendChild(noticesTab.tab);
        
        // Add tab contents
        if (this.results.issues.length > 0) tabContents.appendChild(criticalTab.tabContent);
        if (this.results.warnings.length > 0) tabContents.appendChild(warningsTab.tabContent);
        if (this.results.notices.length > 0) tabContents.appendChild(noticesTab.tabContent);
        
        // Assemble the results
        resultsDiv.appendChild(header);
        resultsDiv.appendChild(summary);
        resultsDiv.appendChild(metrics);
        resultsDiv.appendChild(tabs);
        resultsDiv.appendChild(tabContents);
        
        // Add to page
        document.body.appendChild(resultsDiv);
        
        // Add some basic styling
        const style = document.createElement('style');
        style.textContent = `
            #perf-results button { cursor: pointer; }
            #perf-results ul { margin: 0; }
            #perf-results li { margin-bottom: 5px; }
            #perf-results code { 
                background: #f5f5f5; 
                padding: 2px 4px; 
                border-radius: 3px; 
                font-family: monospace;
            }
            #perf-results div[style*="cursor: pointer"]:hover {
                background: #e9ecef;
                text-decoration: underline;
            }
        `;
        document.head.appendChild(style);
    }
}

// Initialize and run the performance checker when the page loads
document.addEventListener('DOMContentLoaded', () => {
    // Only run in development environment or when explicitly enabled
    if (window.location.hostname === 'localhost' || window.location.search.includes('debug=perf')) {
        const perfChecker = new PerformanceChecker();
        perfChecker.runAllChecks();
    }
});
