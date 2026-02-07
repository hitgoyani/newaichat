/**
 * Landing Page Interactions
 * Handles typing animation, scroll effects, and counter animations
 */

// Typing animation texts
const typingTexts = [
    'Helpdesk Assistant',
    'Study Companion',
    'Knowledge Base',
    'Smart Guide'
];
let currentTextIndex = 0;
let currentCharIndex = 0;
let isDeleting = false;
let typingSpeed = 150;

function typeText() {
    const typingElement = document.getElementById('typingText');
    if (!typingElement) return;

    const currentText = typingTexts[currentTextIndex];

    if (!isDeleting && currentCharIndex < currentText.length) {
        // Typing
        typingElement.textContent = currentText.substring(0, currentCharIndex + 1);
        currentCharIndex++;
        typingSpeed = 150;
    } else if (isDeleting && currentCharIndex > 0) {
        // Deleting
        typingElement.textContent = currentText.substring(0, currentCharIndex - 1);
        currentCharIndex--;
        typingSpeed = 100;
    } else {
        // Switch between typing and deleting
        if (!isDeleting) {
            isDeleting = true;
            typingSpeed = 2000; // Pause before deleting
        } else {
            isDeleting = false;
            currentTextIndex = (currentTextIndex + 1) % typingTexts.length;
            typingSpeed = 500; // Pause before typing next word
        }
    }

    setTimeout(typeText, typingSpeed);
}

// Animated counter
function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const increment = target / (duration / 16); // 60fps
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

// Intersection Observer for scroll animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');

            // Animate counters when stats become visible
            if (entry.target.classList.contains('hero-stats')) {
                const statNumbers = entry.target.querySelectorAll('.stat-number');
                statNumbers.forEach(stat => {
                    const target = parseInt(stat.dataset.target);
                    animateCounter(stat, target);
                });
            }

            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Stagger animation for feature cards
function staggerFeatureCards() {
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach((card, index) => {
        setTimeout(() => {
            observer.observe(card);
        }, index * 100);
    });
}

// Smooth scroll for anchor links
function setupSmoothScroll() {
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

// Parallax effect on scroll
function setupParallax() {
    let ticking = false;

    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                const scrolled = window.pageYOffset;
                const floatingElements = document.querySelectorAll('.float-item');

                floatingElements.forEach((element, index) => {
                    const speed = 0.5 + (index * 0.1);
                    const yPos = -(scrolled * speed);
                    element.style.transform = `translateY(${yPos}px)`;
                });

                ticking = false;
            });
            ticking = true;
        }
    });
}

// Initialize all functionality
function init() {
    // Start typing animation
    setTimeout(typeText, 1000);

    // Setup scroll animations
    staggerFeatureCards();

    // Observe steps section
    const steps = document.querySelectorAll('.step');
    steps.forEach((step, index) => {
        setTimeout(() => {
            observer.observe(step);
        }, index * 200);
    });

    // Observe stats for counter animation
    const statsSection = document.querySelector('.hero-stats');
    if (statsSection) {
        observer.observe(statsSection);
    }

    // Setup smooth scroll
    setupSmoothScroll();

    // Setup parallax
    setupParallax();

    console.log('✨ Landing page initialized');
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', init);

// Add loading class removal for smooth entrance
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
});
