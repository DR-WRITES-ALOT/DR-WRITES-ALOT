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

// Hero Dashboard Initial Animation
const tl = gsap.timeline();

tl.to(".dashboard-container", {
    opacity: 1,
    duration: 0.5,
    delay: 0.2
})
.from(".ide-window", {
    y: 50,
    scale: 0.9,
    opacity: 0,
    duration: 0.8,
    ease: "back.out(1.5)"
})
.from(".status-widget", {
    x: -50,
    opacity: 0,
    duration: 0.6,
    ease: "power2.out"
}, "-=0.4")
.from(".tech-widget", {
    x: 50,
    opacity: 0,
    duration: 0.6,
    ease: "power2.out"
}, "-=0.4")
.add(() => startTypingAnimation(), "-=0.2"); // Start typing right after IDE appears

// Typewriter Effect for IDE
const typeTextElement = document.getElementById('typewriter-text');
const codeLines = [
    { text: "const ", class: "ide-keyword" },
    { text: "developer", class: "ide-string" },
    { text: " = ", class: "" },
    { text: "{\n", class: "" },
    { text: "  name: ", class: "" },
    { text: "'Sreejith S H'", class: "ide-string" },
    { text: ",\n  role: ", class: "" },
    { text: "'Software Engineer'", class: "ide-string" },
    { text: ",\n  passion: ", class: "" },
    { text: "'Building cool stuff!'", class: "ide-string" },
    { text: "\n};\n\n", class: "" },
    { text: "// Let's build something awesome", class: "ide-comment" }
];

function startTypingAnimation() {
    let currentLine = 0;
    let currentChar = 0;
    let currentSpan = null;

    function typeNextChar() {
        if (currentLine < codeLines.length) {
            const lineData = codeLines[currentLine];

            if (currentChar === 0) {
                if (lineData.class) {
                    currentSpan = document.createElement('span');
                    currentSpan.className = lineData.class;
                    typeTextElement.appendChild(currentSpan);
                } else {
                    currentSpan = document.createElement('span');
                    typeTextElement.appendChild(currentSpan);
                }
            }

            if (currentChar < lineData.text.length) {
                let char = lineData.text[currentChar];

                if (char === '\n') {
                    currentSpan.appendChild(document.createElement('br'));
                } else if (char === ' ') {
                    currentSpan.innerHTML += '&nbsp;';
                } else {
                    currentSpan.appendChild(document.createTextNode(char));
                }

                currentChar++;

                const typingSpeed = Math.random() * 50 + 20;
                setTimeout(typeNextChar, typingSpeed);
            } else {
                currentLine++;
                currentChar = 0;
                setTimeout(typeNextChar, 100);
            }
        }
    }
    typeNextChar();
}

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
