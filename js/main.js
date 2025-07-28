// Silicon Theme-Inspired JavaScript for AKM SecureKey

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize Silicon Theme Features
    initSiliconTheme();
    
    // Initialize Scroll Animations
    initScrollAnimations();
    
    // Initialize Interactive Elements
    initInteractiveElements();
    
    // Initialize Performance Monitoring
    initPerformanceMonitoring();
});

/**
 * Initialize Silicon Theme Features
 */
function initSiliconTheme() {
    console.log('🚀 Initializing Silicon Theme for AKM SecureKey');
    
    // Add loading animation to body
    document.body.classList.add('silicon-loaded');
    
    // Initialize smooth scrolling
    initSmoothScrolling();
    
    // Initialize parallax effects
    initParallaxEffects();
}

/**
 * Initialize Scroll Animations
 */
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                
                // Add staggered animation to child elements
                const children = entry.target.querySelectorAll('.col-xl-3, .col-xl-6, .col-11');
                children.forEach((child, index) => {
                    setTimeout(() => {
                        child.style.opacity = '1';
                        child.style.transform = 'translateY(0)';
                    }, index * 100);
                });
            }
        });
    }, observerOptions);
    
    // Observe all main sections
    document.querySelectorAll('.col-xxl-12').forEach(section => {
        observer.observe(section);
    });
}

/**
 * Initialize Interactive Elements
 */
function initInteractiveElements() {
    
    // Enhanced button interactions
    document.querySelectorAll('.border.border-3.border-white').forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px) scale(1.02)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
        
        button.addEventListener('click', function(e) {
            // Add ripple effect
            createRippleEffect(e, this);
        });
    });
    
    // Enhanced card interactions
    document.querySelectorAll('.bg-black.bg-opacity-10, .bg-white.bg-opacity-25').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
            this.style.boxShadow = '0 1rem 3rem rgba(0, 0, 0, 0.175)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 0.5rem 1rem rgba(0, 0, 0, 0.15)';
        });
    });
    
    // Enhanced link interactions
    document.querySelectorAll('.text-dark.fs-6.fw-normal.font-family-Inter').forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.color = '#0d6efd';
            this.style.transform = 'translateX(5px)';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.color = '';
            this.style.transform = 'translateX(0)';
        });
    });
    
    // Circular icon interactions
    document.querySelectorAll('.bg-black.bg-opacity-25.rounded-circle').forEach(icon => {
        icon.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1) rotate(5deg)';
        });
        
        icon.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) rotate(0deg)';
        });
    });
}

/**
 * Create Ripple Effect for Buttons
 */
function createRippleEffect(event, element) {
    const ripple = document.createElement('span');
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;
    
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    ripple.classList.add('ripple');
    
    element.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

/**
 * Initialize Smooth Scrolling
 */
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Initialize Parallax Effects
 */
function initParallaxEffects() {
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const parallaxElements = document.querySelectorAll('.bg-black.bg-opacity-75');
        
        parallaxElements.forEach(element => {
            const speed = 0.5;
            element.style.transform = `translateY(${scrolled * speed}px)`;
        });
    });
}

/**
 * Initialize Performance Monitoring
 */
function initPerformanceMonitoring() {
    // Monitor page load performance
    window.addEventListener('load', () => {
        const loadTime = performance.now();
        console.log(`📊 Page loaded in ${loadTime.toFixed(2)}ms`);
        
        // Add performance class to body
        if (loadTime < 2000) {
            document.body.classList.add('performance-fast');
        } else if (loadTime < 4000) {
            document.body.classList.add('performance-medium');
        } else {
            document.body.classList.add('performance-slow');
        }
    });
    
    // Monitor scroll performance
    let scrollTimeout;
    window.addEventListener('scroll', () => {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(() => {
            const scrollTime = performance.now();
            console.log(`📊 Scroll performance: ${scrollTime.toFixed(2)}ms`);
        }, 100);
    });
}

/**
 * Add CSS for Ripple Effect
 */
const rippleCSS = `
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .silicon-loaded {
        opacity: 1;
        transition: opacity 0.5s ease-in-out;
    }
    
    .performance-fast {
        --silicon-transition: all 0.2s ease-in-out;
    }
    
    .performance-medium {
        --silicon-transition: all 0.3s ease-in-out;
    }
    
    .performance-slow {
        --silicon-transition: all 0.4s ease-in-out;
    }
`;

// Inject CSS
const style = document.createElement('style');
style.textContent = rippleCSS;
document.head.appendChild(style);

/**
 * Utility Functions
 */
const SiliconUtils = {
    // Debounce function for performance
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
    
    // Throttle function for scroll events
    throttle: function(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },
    
    // Check if element is in viewport
    isInViewport: function(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }
};

// Export for global access
window.SiliconUtils = SiliconUtils; 