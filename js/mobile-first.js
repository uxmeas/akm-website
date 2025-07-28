/**
 * Mobile-First JavaScript for AKM SecureKey
 * Handles mobile navigation, smooth scrolling, animations, and accessibility
 */

document.addEventListener('DOMContentLoaded', function() {
    // Add ARIA live region for dynamic content
    const liveRegion = document.createElement('div');
    liveRegion.setAttribute('aria-live', 'polite');
    liveRegion.setAttribute('aria-atomic', 'true');
    liveRegion.classList.add('sr-only');
    document.body.appendChild(liveRegion);
    
    // Announce page load for screen readers
    const pageTitle = document.title || 'AKM Secure Website';
    liveRegion.textContent = `Loaded: ${pageTitle}`;
    // Mobile navigation toggle
    const navToggle = document.querySelector('.navbar-toggler');
    const navMenu = document.querySelector('.navbar-collapse');
    const mainContent = document.querySelector('main');
    
    // Trap focus in mobile menu when open
    const trapFocus = (element) => {
        const focusableEls = element.querySelectorAll('a[href]:not([disabled]), button:not([disabled]), textarea:not([disabled]), input[type="text"]:not([disabled]), input[type="radio"]:not([disabled]), input[type="checkbox"]:not([disabled]), select:not([disabled])');
        const firstFocusableEl = focusableEls[0];
        const lastFocusableEl = focusableEls[focusableEls.length - 1];
        
        element.addEventListener('keydown', function(e) {
            const isTabPressed = (e.key === 'Tab' || e.keyCode === 9);
            
            if (!isTabPressed) return;
            
            if (e.shiftKey) {
                if (document.activeElement === firstFocusableEl) {
                    lastFocusableEl.focus();
                    e.preventDefault();
                }
            } else {
                if (document.activeElement === lastFocusableEl) {
                    firstFocusableEl.focus();
                    e.preventDefault();
                }
            }
        });
    };
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            const isExpanded = this.getAttribute('aria-expanded') === 'true';
            const newState = !isExpanded;
            
            this.setAttribute('aria-expanded', newState);
            navMenu.classList.toggle('show');
            
            // Toggle body scroll and inert state when mobile menu is open
            document.body.style.overflow = newState ? 'hidden' : '';
            
            if (mainContent) {
                mainContent.inert = newState;
            }
            
            // Announce menu state to screen readers
            const liveRegion = document.querySelector('[aria-live]');
            if (liveRegion) {
                liveRegion.textContent = `Main menu ${newState ? 'opened' : 'closed'}`;
            }
            
            // Focus management
            if (newState) {
                // Focus on first item in menu when opened
                const firstNavItem = navMenu.querySelector('a');
                if (firstNavItem) {
                    firstNavItem.focus();
                }
                // Set up focus trap
                trapFocus(navMenu);
            } else {
                // Return focus to menu toggle when closed
                this.focus();
            }
        });
    }
    
    // Close mobile menu when clicking on a nav link
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            if (navMenu.classList.contains('show')) {
                navMenu.classList.remove('show');
                navToggle.setAttribute('aria-expanded', 'false');
                document.body.style.overflow = '';
            }
        });
    });
    
    // Initialize Intersection Observer for section animations
    const initIntersectionObserver = () => {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -20% 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // Add animation class to section
                    entry.target.classList.add('animate-in');
                    
                    // Animate in child elements with staggered delays
                    const content = entry.target.querySelector('.section-content');
                    if (content) {
                        const children = content.children;
                        Array.from(children).forEach((child, index) => {
                            child.style.transitionDelay = `${index * 0.1}s`;
                        });
                    }
                    
                    // Update active navigation
                    updateActiveNav(entry.target.id);
                }
            });
        }, observerOptions);

        // Observe all sections with IDs
        document.querySelectorAll('section[id]').forEach(section => {
            observer.observe(section);
        });
    };

    // Update active navigation based on scroll position
    const updateActiveNav = (sectionId) => {
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.toggle('active', 
                link.getAttribute('href') === `#${sectionId}` ||
                (sectionId === 'hero' && link.getAttribute('href') === '#home')
            );
        });
    };

    // Smooth scrolling for anchor links with offset
    const initSmoothScrolling = () => {
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                const targetId = this.getAttribute('href');
                if (targetId === '#') {
                    e.preventDefault();
                    return;
                }
                
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    e.preventDefault();
                    
                    // Close mobile menu if open
                    const mobileMenu = document.getElementById('mobile-menu');
                    if (mobileMenu && mobileMenu.classList.contains('active')) {
                        toggleMobileMenu();
                    }
                    
                    // Calculate scroll position with offset
                    const headerHeight = document.querySelector('header')?.offsetHeight || 80;
                    const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - headerHeight;
                    
                    // Smooth scroll
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                    
                    // Update URL without page jump
                    if (history.pushState) {
                        history.pushState(null, null, targetId);
                    } else {
                        location.hash = targetId;
                    }
                }
            });
        });
    };

    // Initialize scroll-based animations
    const initScrollAnimations = () => {
        let ticking = false;
        
        const updateElements = () => {
            // Add any scroll-based animations here
            ticking = false;
        };
        
        window.addEventListener('scroll', () => {
            if (!ticking) {
                window.requestAnimationFrame(updateElements);
                ticking = true;
            }
        }, { passive: true });
    };

    // Initialize all functionality
    const init = () => {
        initIntersectionObserver();
        initSmoothScrolling();
        initScrollAnimations();
        
        // Check for reduced motion preference
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
            document.documentElement.classList.add('reduced-motion');
        }
    };

    // Initialize when DOM is fully loaded
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Smooth scrolling for anchor links with accessibility enhancements
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        // Skip if it's a tab control or other interactive element
        if (anchor.getAttribute('role') === 'tab' || anchor.getAttribute('data-bs-toggle')) {
            return;
        }
        
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#' || targetId === '#!') {
                e.preventDefault();
                return;
            }
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                e.preventDefault();
                
                // Update URL without adding to history
                if (history.pushState) {
                    history.pushState(null, null, targetId);
                } else {
                    location.hash = targetId;
                }
                
                const headerOffset = 80; // Height of fixed header
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                
                // Smooth scroll
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
                
                // Focus management for keyboard users
                setTimeout(() => {
                    // Make the target focusable if it's not already
                    if (!targetElement.hasAttribute('tabindex')) {
                        targetElement.setAttribute('tabindex', '-1');
                    }
                    
                    // Focus the target
                    targetElement.focus();
                    
                    // Announce the section to screen readers
                    const sectionLabel = targetElement.getAttribute('aria-label') || 
                                      targetElement.getAttribute('aria-labelledby') ? 
                                      document.querySelector(`#${targetElement.getAttribute('aria-labelledby')}`)?.textContent : 
                                      targetElement.querySelector('h1, h2, h3, h4, h5, h6')?.textContent || 'Section';
                    
                    const liveRegion = document.querySelector('[aria-live]');
                    if (liveRegion) {
                        liveRegion.textContent = `Navigated to ${sectionLabel}`;
                    }
                }, 1000);
            }
        });
    });
    
    // Handle focus for elements with tabindex="-1"
    document.addEventListener('focus', function(e) {
        const target = e.target;
        if (target.getAttribute('tabindex') === '-1' && target !== document.activeElement) {
            target.focus();
        }
    }, true);
    
    // Intersection Observer for scroll animations and lazy loading
    const initIntersectionObserver = () => {
        // Animation observer
        const animateElements = document.querySelectorAll('.feature-card, .section-header, [data-animate]');
        const lazyImages = document.querySelectorAll('img[data-src], iframe[data-src]');
        
        // Animation observer
        const animationObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate');
                    
                    // If element has a delay, apply it
                    const delay = entry.target.dataset.animationDelay || 0;
                    if (delay) {
                        entry.target.style.animationDelay = `${delay}ms`;
                    }
                    
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });
        
        // Lazy load observer
        const lazyLoadObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const element = entry.target;
                    
                    if (element.tagName === 'IMG') {
                        element.src = element.dataset.src;
                        element.removeAttribute('data-src');
                        
                        // Handle srcset if present
                        if (element.dataset.srcset) {
                            element.srcset = element.dataset.srcset;
                            element.removeAttribute('data-srcset');
                        }
                        
                        // Add loaded class when image is loaded
                        element.addEventListener('load', () => {
                            element.classList.add('loaded');
                        });
                        
                        // Handle error state
                        element.addEventListener('error', () => {
                            console.error(`Failed to load image: ${element.dataset.src}`);
                            element.classList.add('load-error');
                        });
                    } else if (element.tagName === 'IFRAME') {
                        element.src = element.dataset.src;
                        element.removeAttribute('data-src');
                    }
                    
                    observer.unobserve(element);
                }
            });
        }, {
            rootMargin: '200px 0px',
            threshold: 0.01
        });
        
        // Observe all animation elements
        animateElements.forEach(element => {
            animationObserver.observe(element);
        });
        
        // Observe all lazy load elements
        lazyImages.forEach(element => {
            lazyLoadObserver.observe(element);
        });
        
        return {
            animationObserver,
            lazyLoadObserver
        };
    };
    
    // Initialize animations and lazy loading
    const observers = initIntersectionObserver();
    
    // Add loaded class to body to enable transitions
    // Use requestAnimationFrame to ensure the DOM is ready
    requestAnimationFrame(() => {
        document.body.classList.add('loaded');
        
        // Remove focus from body on initial load
        if (document.activeElement === document.body) {
            document.activeElement.blur();
        }
    });
    
    // Handle prefers-reduced-motion
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
    if (mediaQuery.matches) {
        document.documentElement.classList.add('reduced-motion');
    }
    
    mediaQuery.addEventListener('change', () => {
        if (mediaQuery.matches) {
            document.documentElement.classList.add('reduced-motion');
        } else {
            document.documentElement.classList.remove('reduced-motion');
        }
    });
    
    // Handle keyboard focus styles
    function handleFirstTab(e) {
        if (e.key === 'Tab' || e.keyCode === 9) {
            document.body.classList.add('user-is-tabbing');
            window.removeEventListener('keydown', handleFirstTab);
        }
    }
    
    window.addEventListener('keydown', handleFirstTab);
    
    // Handle focus visible polyfill if needed
    if (!CSS.supports('selector(:focus-visible)')) {
        import('focus-visible').then(module => {
            // Initialize focus-visible polyfill
            module.setupFocusVisible();
        }).catch(error => {
            console.warn('Failed to load focus-visible polyfill:', error);
        });
    }
    
    // Handle window resize events
    let resizeTimer;
    window.addEventListener('resize', () => {
        document.body.classList.add('resizing');
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
            document.body.classList.remove('resizing');
        }, 250);
    });
});
