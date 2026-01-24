// Force page to start at the top on reload
if ('scrollRestoration' in history) {
  history.scrollRestoration = 'manual';
}

// If the user refreshes with a hash (e.g., #projects), remove it and scroll to top
if (window.location.hash) {
  history.replaceState(null, null, window.location.pathname);
}

// Mouse Follower Glow
const glow = document.createElement('div');
glow.className = 'mouse-glow';
document.body.appendChild(glow);

document.addEventListener('mousemove', (e) => {
  glow.style.left = e.clientX + 'px';
  glow.style.top = e.clientY + 'px';
  
  // Subtle parallax for background blobs
  const blobs = document.querySelectorAll('.blob');
  const x = e.clientX / window.innerWidth;
  const y = e.clientY / window.innerHeight;
  
  blobs.forEach((blob, index) => {
    const speed = (index + 1) * 20;
    blob.style.transform = `translate(${x * speed}px, ${y * speed}px)`;
  });
});

window.onload = function() {
  window.scrollTo(0, 0);
  typeWriter();
};

/* --- Intersection Observer for Scroll Animations --- */
const observerOptions = {
  threshold: 0.1,
  rootMargin: "0px"
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('show');
    }
  });
}, observerOptions);

// Select elements to animate
const hiddenElements = document.querySelectorAll('.section h2, .section p, .skill-category, .project-card, .education-item, .contact-item, .hero-content');

hiddenElements.forEach((el, index) => {
  el.classList.add('hidden');
  // Add staggered delays for grid items primarily
  if (el.classList.contains('project-card') || el.classList.contains('skill-category')) {
      // Simple modulo delay based on child index would be better but this is a quick approximation
     // Check if we can apply delay based on order in parent
  }
  observer.observe(el);
});

// Specific logic to add staggered delays to children of grids
document.querySelectorAll('.projects-grid, .skills-categories').forEach(grid => {
  const children = grid.children;
  Array.from(children).forEach((child, index) => {
    child.classList.add(`delay-${(index % 5) * 100 + 100}`); // Adds delay-100, delay-200, etc.
  });
});


/* --- Typing Effect --- */
const textElement = document.querySelector('.hero-content h3');
const originalText = textElement ? textElement.innerText : "Full Stack Developer";
if(textElement) textElement.innerText = ""; // Clear text initially

let i = 0;
function typeWriter() {
  if (i < originalText.length && textElement) {
    textElement.innerHTML += originalText.charAt(i);
    i++;
    setTimeout(typeWriter, 100);
  } else if (textElement) {
     textElement.classList.add('typing-cursor');
  }
}

// Copy email to clipboard
document.querySelectorAll('.email-link').forEach(link => {
  link.addEventListener('click', function () {
    const email = "ahmedbiram47@gmail.com";
    navigator.clipboard.writeText(email).then(() => {
      alert("Email copied: " + email);
    });
  });
});
