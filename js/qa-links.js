// QA Link Checker for AKM Secure Website
// This script checks all links on the page and reports any issues

class LinkChecker {
    constructor() {
        this.results = {
            total: 0,
            internal: 0,
            external: 0,
            broken: [],
            emptyHrefs: [],
            samePage: [],
            status: 'ready'
        };
        
        // Elements to ignore (e.g., buttons that use JS for navigation)
        this.ignoreSelectors = [
            '[href="#"]',
            '[href="javascript:void(0)"]',
            '[href^="tel:"]',
            '[href^="mailto:"]',
            '[href*="#"]:not([href*=".html#"])' // Ignore same-page anchors
        ];
        
        // Known external domains that should be allowed
        this.allowedDomains = [
            'linkedin.com',
            'twitter.com',
            'youtube.com',
            'github.com',
            'bootstrap.com',
            'fontawesome.com'
        ];
    }
    
    // Main method to run the link check
    async checkAllLinks() {
        this.results.status = 'checking';
        this.results.total = 0;
        this.results.internal = 0;
        this.results.external = 0;
        this.results.broken = [];
        this.results.emptyHrefs = [];
        this.results.samePage = [];
        
        try {
            // Get all links on the page
            const links = Array.from(document.querySelectorAll('a[href]'));
            this.results.total = links.length;
            
            // Filter out ignored links
            const ignoreSelectors = this.ignoreSelectors.join(',');
            const filteredLinks = links.filter(link => {
                // Skip if link matches any ignore selector
                if (link.matches(ignoreSelectors)) {
                    if (link.getAttribute('href') === '#') {
                        this.results.samePage.push({
                            element: link,
                            href: link.href,
                            text: link.textContent.trim() || '[No text]',
                            selector: this.getElementSelector(link)
                        });
                    }
                    return false;
                }
                
                // Skip if no href or empty href
                if (!link.href || link.href.trim() === '') {
                    this.results.emptyHrefs.push({
                        element: link,
                        text: link.textContent.trim() || '[No text]',
                        selector: this.getElementSelector(link)
                    });
                    return false;
                }
                
                return true;
            });
            
            // Check each remaining link
            for (const link of filteredLinks) {
                await this.checkLink(link);
            }
            
            this.results.status = 'complete';
            this.showResults();
            
        } catch (error) {
            console.error('Error checking links:', error);
            this.results.status = 'error';
            this.results.error = error.message;
        }
    }
    
    // Check a single link
    async checkLink(link) {
        const url = new URL(link.href);
        const isExternal = !url.hostname.includes(window.location.hostname) && 
                         !this.allowedDomains.some(domain => url.hostname.includes(domain));
        
        const linkInfo = {
            href: link.href,
            text: link.textContent.trim() || '[No text]',
            selector: this.getElementSelector(link),
            isExternal,
            status: 'pending'
        };
        
        try {
            if (isExternal) {
                // For external links, we can't check status due to CORS
                // Just mark them as external
                this.results.external++;
                linkInfo.status = 'external';
                return;
            }
            
            // For internal links, we can check if they're valid
            const response = await fetch(link.href, { 
                method: 'HEAD',
                cache: 'no-store'
            });
            
            if (response.ok) {
                this.results.internal++;
                linkInfo.status = response.status;
            } else {
                this.results.broken.push({
                    ...linkInfo,
                    status: response.status
                });
            }
            
        } catch (error) {
            // If HEAD request fails, maybe it's a client-side route
            // Try a GET request for the homepage to verify the domain is reachable
            if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
                try {
                    const domainCheck = await fetch('/', { method: 'HEAD' });
                    if (domainCheck.ok) {
                        // If we can reach the domain, it's likely a client-side route
                        this.results.internal++;
                        linkInfo.status = 'client-side-route';
                    } else {
                        throw new Error(`Server returned ${domainCheck.status}`);
                    }
                } catch (e) {
                    this.results.broken.push({
                        ...linkInfo,
                        status: 'error',
                        error: error.message
                    });
                }
            } else {
                this.results.broken.push({
                    ...linkInfo,
                    status: 'error',
                    error: error.message
                });
            }
        }
    }
    
    // Helper to generate a CSS selector for an element
    getElementSelector(element) {
        if (!element || !element.tagName) return '';
        
        const path = [];
        let current = element;
        
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
                    if (sibling.nodeType === Node.ELEMENT_NODE && sibling.nodeName.toLowerCase() === selector) {
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
        resultsDiv.id = 'qa-link-results';
        resultsDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            max-width: 400px;
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
        title.textContent = 'Link Checker Results';
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
        summary.innerHTML = `
            <div><strong>Total Links:</strong> ${this.results.total}</div>
            <div><strong>Internal Links:</strong> ${this.results.internal}</div>
            <div><strong>External Links:</strong> ${this.results.external}</div>
            <div><strong>Broken Links:</strong> ${this.results.broken.length}</div>
            <div><strong>Empty Hrefs:</strong> ${this.results.emptyHrefs.length}</div>
            <div><strong>Same-Page Anchors:</strong> ${this.results.samePage.length}</div>
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
            
            if (typeof content === 'string') {
                tabContent.innerHTML = content;
            } else if (Array.isArray(content) && content.length > 0) {
                const list = document.createElement('ul');
                list.style.paddingLeft = '20px';
                content.forEach(item => {
                    const li = document.createElement('li');
                    li.style.marginBottom = '8px';
                    
                    if (item.selector) {
                        const code = document.createElement('code');
                        code.textContent = item.selector;
                        code.style.display = 'block';
                        code.style.marginTop = '4px';
                        code.style.fontSize = '12px';
                        code.style.color = '#666';
                        
                        const link = document.createElement('a');
                        link.href = item.href || '#';
                        link.textContent = item.text;
                        link.target = '_blank';
                        link.style.color = '#007bff';
                        link.style.textDecoration = 'none';
                        
                        li.appendChild(link);
                        li.appendChild(document.createElement('br'));
                        li.appendChild(code);
                        
                        if (item.status) {
                            const status = document.createElement('span');
                            status.textContent = `Status: ${item.status}`;
                            status.style.display = 'block';
                            status.style.fontSize = '12px';
                            status.style.color = item.status >= 400 ? '#dc3545' : '#28a745';
                            li.appendChild(status);
                        }
                    } else {
                        li.textContent = item.text || 'Unknown';
                    }
                    
                    list.appendChild(li);
                });
                tabContent.appendChild(list);
            } else {
                tabContent.textContent = 'No items to display.';
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
        const brokenTab = createTab('Broken Links', this.results.broken, true);
        const emptyTab = createTab('Empty Hrefs', this.results.emptyHrefs);
        const samePageTab = createTab('Same-Page Anchors', this.results.samePage);
        
        tabs.appendChild(brokenTab.tab);
        tabs.appendChild(emptyTab.tab);
        tabs.appendChild(samePageTab.tab);
        
        tabContents.appendChild(brokenTab.tabContent);
        tabContents.appendChild(emptyTab.tabContent);
        tabContents.appendChild(samePageTab.tabContent);
        
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
            #qa-link-results button { cursor: pointer; }
            #qa-link-results ul { margin: 0; }
            #qa-link-results li { margin-bottom: 5px; }
            #qa-link-results code { 
                background: #f5f5f5; 
                padding: 2px 4px; 
                border-radius: 3px; 
                font-family: monospace;
            }
        `;
        document.head.appendChild(style);
    }
}

// Initialize and run the link checker when the page loads
document.addEventListener('DOMContentLoaded', () => {
    // Only run in development environment or when explicitly enabled
    if (window.location.hostname === 'localhost' || window.location.search.includes('debug=links')) {
        const linkChecker = new LinkChecker();
        linkChecker.checkAllLinks();
    }
});
