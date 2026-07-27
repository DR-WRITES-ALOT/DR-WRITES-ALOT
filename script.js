// Custom Cursor Logic
const cursor = document.querySelector('.cursor');
const follower = document.querySelector('.cursor-follower');
const links = document.querySelectorAll('a, .btn, .skill-item, .contact-card');

document.addEventListener('mousemove', (e) => {
    // Update cursor position directly for instant response
    cursor.style.left = e.clientX + 'px';
    cursor.style.top = e.clientY + 'px';

    // Use GSAP to animate follower with slight delay for smooth effect
    gsap.to(follower, {
        x: e.clientX,
        y: e.clientY,
        duration: 0.1,
        ease: 'power2.out'
    });
});

// Add hover effect to interactive elements
links.forEach(link => {
    link.addEventListener('mouseenter', () => {
        cursor.classList.add('hovered');
        follower.classList.add('hovered');
    });

    link.addEventListener('mouseleave', () => {
        cursor.classList.remove('hovered');
        follower.classList.remove('hovered');
    });
});

// GSAP Animations
gsap.registerPlugin(ScrollTrigger);

// Hero Section Initial Animation
const tl = gsap.timeline();

tl.to(".hero-content", {
    y: 0,
    opacity: 1,
    duration: 1,
    ease: "power3.out",
    delay: 0.2
});

// Navbar background change on scroll
window.addEventListener('scroll', () => {
    const nav = document.querySelector('nav');
    if (window.scrollY > 50) {
        nav.style.background = 'rgba(10, 10, 10, 0.95)';
        nav.style.boxShadow = '0 10px 30px -10px rgba(2,12,27,0.7)';
    } else {
        nav.style.background = 'rgba(10, 10, 10, 0.85)';
        nav.style.boxShadow = 'none';
    }
});

// Scroll Animations for About Section
gsap.from(".about-text", {
    scrollTrigger: {
        trigger: "#about",
        start: "top 80%",
    },
    y: 50,
    opacity: 0,
    duration: 0.8,
    ease: "power2.out"
});

gsap.from(".skill-item", {
    scrollTrigger: {
        trigger: ".skills",
        start: "top 85%",
    },
    y: 50,
    opacity: 0,
    duration: 0.6,
    stagger: 0.15,
    ease: "back.out(1.7)"
});

// Scroll Animations for Contact Section
gsap.from(".contact-text", {
    scrollTrigger: {
        trigger: "#contact",
        start: "top 80%",
    },
    y: 30,
    opacity: 0,
    duration: 0.8,
    ease: "power2.out"
});

gsap.from(".contact-card", {
    scrollTrigger: {
        trigger: ".contact-cards",
        start: "top 85%",
    },
    y: 50,
    opacity: 0,
    duration: 0.6,
    stagger: 0.2,
    ease: "power3.out"
});
