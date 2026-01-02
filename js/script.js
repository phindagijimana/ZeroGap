// Page Navigation
function showPage(pageId) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });
    
    // Show selected page
    document.getElementById(pageId).classList.add('active');
    
    // Scroll to top
    window.scrollTo(0, 0);
}

// Smooth scroll to section
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Mobile menu toggle
function toggleMenu() {
    const menu = document.getElementById('nav-menu');
    menu.classList.toggle('active');
}

// Close mobile menu
function closeMenu() {
    const menu = document.getElementById('nav-menu');
    menu.classList.remove('active');
}

// Contact form submission
function handleSubmit(event) {
    event.preventDefault();
    
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;

    const subject = encodeURIComponent(`Message from ${name}`);
    const body = encodeURIComponent(`From: ${name}
Email: ${email}

Message:
${message}`);
    
    window.location.href = `mailto:contact@zerogap.tech?subject=${subject}&body=${body}`;
    
    document.querySelector('.contact-form').reset();
    
    alert('Opening your email client...');
}

// Close menu when clicking outside
document.addEventListener('click', function(event) {
    const menu = document.getElementById('nav-menu');
    const nav = document.querySelector('nav');
    
    if (!nav.contains(event.target) && menu.classList.contains('active')) {
        menu.classList.remove('active');
    }
});

