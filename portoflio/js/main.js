// Force page to start at the top on reload
if ('scrollRestoration' in history) {
  history.scrollRestoration = 'manual';
}

// If the user refreshes with a hash (e.g., #projects), remove it and scroll to top
if (window.location.hash) {
  history.replaceState(null, null, window.location.pathname);
}

// Enhanced Mouse Follower with Magnetic Effect
const glow = document.createElement('div');
glow.className = 'mouse-glow';
document.body.appendChild(glow);

const cursor = document.createElement('div');
cursor.className = 'custom-cursor';
cursor.style.cssText = `
  position: fixed;
  width: 20px;
  height: 20px;
  background: #00f0ff;
  border-radius: 50%;
  pointer-events: none;
  z-index: 9999;
  mix-blend-mode: difference;
  transition: transform 0.1s ease;
`;
document.body.appendChild(cursor);

let mouseX = 0, mouseY = 0;
let cursorX = 0, cursorY = 0;

document.addEventListener('mousemove', (e) => {
  mouseX = e.clientX;
  mouseY = e.clientY;
  
  glow.style.left = e.clientX + 'px';
  glow.style.top = e.clientY + 'px';
  
  // Enhanced parallax for background blobs with anime.js
  const blobs = document.querySelectorAll('.blob');
  const x = e.clientX / window.innerWidth;
  const y = e.clientY / window.innerHeight;
  
  blobs.forEach((blob, index) => {
    const speed = (index + 1) * 40;
    anime({
      targets: blob,
      translateX: x * speed,
      translateY: y * speed,
      duration: 1200,
      easing: 'easeOutQuad'
    });
  });
});

// Smooth cursor follow animation
function animateCursor() {
  cursorX += (mouseX - cursorX) * 0.1;
  cursorY += (mouseY - cursorY) * 0.1;
  
  cursor.style.left = cursorX - 10 + 'px';
  cursor.style.top = cursorY - 10 + 'px';
  
  requestAnimationFrame(animateCursor);
}
animateCursor();

// Magnetic cursor effect for interactive elements
document.querySelectorAll('.btn, .project-card, .skills-grid span, nav a').forEach(element => {
  element.addEventListener('mouseenter', () => {
    anime({
      targets: cursor,
      scale: 2,
      duration: 300,
      easing: 'easeOutQuad'
    });
  });
  
  element.addEventListener('mouseleave', () => {
    anime({
      targets: cursor,
      scale: 1,
      duration: 300,
      easing: 'easeOutQuad'
    });
  });
});

// Text Scramble Animation
class TextScramble {
  constructor(el) {
    this.el = el;
    this.chars = '!<>-_\/[]{}—=+*^?#________';
    this.update = this.update.bind(this);
  }
  
  setText(newText) {
    const oldText = this.el.innerText;
    const length = Math.max(oldText.length, newText.length);
    const promise = new Promise((resolve) => this.resolve = resolve);
    this.queue = [];
    for (let i = 0; i < length; i++) {
      const from = oldText[i] || '';
      const to = newText[i] || '';
      const start = Math.floor(Math.random() * 40);
      const end = start + Math.floor(Math.random() * 40);
      this.queue.push({ from, to, start, end });
    }
    cancelAnimationFrame(this.frameRequest);
    this.frame = 0;
    this.update();
    return promise;
  }
  
  update() {
    let output = '';
    let complete = 0;
    for (let i = 0, n = this.queue.length; i < n; i++) {
      let { from, to, start, end, char } = this.queue[i];
      if (this.frame >= end) {
        complete++;
        output += to;
      } else if (this.frame >= start) {
        if (!char || Math.random() < 0.28) {
          char = this.randomChar();
          this.queue[i].char = char;
        }
        output += char;
      } else {
        output += from;
      }
    }
    this.el.innerHTML = output;
    if (complete === this.queue.length) {
      this.resolve();
    } else {
      this.frameRequest = requestAnimationFrame(this.update);
      this.frame++;
    }
  }
  
  randomChar() {
    return this.chars[Math.floor(Math.random() * this.chars.length)];
  }
}

// Particle Animation System
class ParticleSystem {
  constructor() {
    this.particles = [];
    this.container = document.createElement('div');
    this.container.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 1;
    `;
    document.body.appendChild(this.container);
  }
  
  createParticle(x, y) {
    const particle = document.createElement('div');
    particle.style.cssText = `
      position: absolute;
      width: 4px;
      height: 4px;
      background: #00f0ff;
      border-radius: 50%;
      left: ${x}px;
      top: ${y}px;
      opacity: 0;
    `;
    
    this.container.appendChild(particle);
    
    const angle = Math.random() * Math.PI * 2;
    const velocity = Math.random() * 100 + 50;
    const lifetime = Math.random() * 1000 + 500;
    
    anime({
      targets: particle,
      translateX: Math.cos(angle) * velocity,
      translateY: Math.sin(angle) * velocity,
      opacity: [0, 1, 0],
      scale: [0, 1, 0],
      duration: lifetime,
      easing: 'easeOutQuad',
      complete: () => {
        particle.remove();
      }
    });
  }
  
  burst(x, y, count = 20) {
    for (let i = 0; i < count; i++) {
      setTimeout(() => this.createParticle(x, y), i * 20);
    }
  }
}

const particleSystem = new ParticleSystem();

// Enhanced entrance animations with anime.js - Ultra Smooth
window.addEventListener('load', () => {
  // Ultra-smooth morphing background blobs
  anime({
    targets: '.blob',
    borderRadius: function() {
      return anime.random(20, 80) + '%';
    },
    scale: function() {
      return anime.random(0.7, 1.4);
    },
    rotate: function() {
      return anime.random(-360, 360);
    },
    translateX: function() {
      return anime.random(-50, 50);
    },
    translateY: function() {
      return anime.random(-50, 50);
    },
    duration: function() {
      return anime.random(6000, 10000);
    },
    delay: anime.stagger(150),
    loop: true,
    direction: 'alternate',
    easing: 'easeInOutSine'
  });
  
  // Ultra-smooth hero entrance with more animations
  anime.timeline({
    easing: 'easeOutCirc',
  })
  .add({
    targets: '.logo-img',
    scale: [0, 1.3, 1],
    opacity: [0, 1],
    rotate: [540, 360, 0],
    filter: ['blur(20px)', 'blur(0px)'],
    duration: 1200,
    delay: 200
  })
  .add({
    targets: 'nav ul li',
    translateY: [80, 0],
    opacity: [0, 1],
    rotate: [20, 0],
    scale: [0.8, 1],
    duration: 600,
    delay: anime.stagger(60, {start: 400})
  }, '-=600')
  .add({
    targets: '.profile-img',
    scale: [0, 1.4, 1],
    opacity: [0, 1],
    borderRadius: ['50%', '20%', '50%'],
    rotate: [180, 0],
    filter: ['hue-rotate(90deg)', 'hue-rotate(0deg)'],
    duration: 1000,
    easing: 'easeOutElastic(1, .6)'
  }, '-=400')
  .add({
    targets: '.hero-content h1',
    translateY: [60, 0],
    opacity: [0, 1],
    scale: [0.7, 1.1, 1],
    rotateZ: [5, 0],
    duration: 900,
    easing: 'easeOutBack(1.8)'
  }, '-=500')
  .add({
    targets: '.hero-content h3',
    translateY: [40, 0],
    opacity: [0, 1],
    scale: [0.8, 1],
    duration: 700,
    complete: () => {
      const fx = new TextScramble(document.querySelector('.hero-content h3'));
      fx.setText('Full Stack Developer');
    }
  }, '-=300')
  .add({
    targets: '.hero-content p',
    translateY: [30, 0],
    opacity: [0, 1],
    translateX: [-20, 0],
    duration: 600
  }, '-=200')
  .add({
    targets: '.contact-info p',
    translateX: [-60, 0],
    opacity: [0, 1],
    rotate: [-5, 0],
    duration: 500,
    delay: anime.stagger(60)
  })
  .add({
    targets: '.buttons .btn',
    translateY: [40, 0],
    opacity: [0, 1],
    scale: [0.6, 1.1, 1],
    rotate: [-3, 0],
    duration: 600,
    delay: anime.stagger(100),
    easing: 'easeOutBack(1.9)',
    begin: () => {
      particleSystem.burst(window.innerWidth / 2, window.innerHeight / 2, 25);
    }
  }, '-=150');
});

// Ultra-smooth Scroll Animations with Anime.js
const observerOptions = {
  threshold: 0.15,
  rootMargin: "-50px 0px"
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const element = entry.target;
      
      // Ultra-smooth section headers with advanced effects
      if (element.classList.contains('section') && element.querySelector('h2')) {
        const h2 = element.querySelector('h2');
        anime({
          targets: h2,
          translateY: [50, 0],
          opacity: [0, 1],
          scale: [0.8, 1.05, 1],
          rotateX: [15, 0],
          duration: 800,
          easing: 'easeOutCubic',
          complete: () => {
            const fx = new TextScramble(h2);
            fx.setText(h2.innerText);
            // Add glow effect after text scramble
            anime({
              targets: h2,
              textShadow: ['0 0 0px rgba(0, 240, 255, 0)', '0 0 20px rgba(0, 240, 255, 0.5)', '0 0 0px rgba(0, 240, 255, 0)'],
              duration: 1000,
              delay: 500
            });
          }
        });
      }
      
      // Ultra-smooth paragraphs with wave effect
      if (element.tagName === 'P' && element.parentElement.classList.contains('section')) {
        anime({
          targets: element,
          translateY: [40, 0],
          opacity: [0, 1],
          translateX: [-10, 0],
          duration: 700,
          delay: 150,
          easing: 'easeOutCubic'
        });
      }
      
      // Ultra-smooth skill categories with 3D perspective
      if (element.classList.contains('skill-category')) {
        anime({
          targets: element,
          translateY: [60, 0],
          rotateX: [30, 0],
          rotateY: [-10, 0],
          scale: [0.85, 1],
          opacity: [0, 1],
          duration: 800,
          delay: anime.stagger(200),
          easing: 'easeOutCubic',
          begin: () => {
            // Add floating animation to category title
            const title = element.querySelector('h3');
            if (title) {
              anime({
                targets: title,
                translateY: [0, -5, 0],
                duration: 2000,
                delay: 800,
                loop: true,
                easing: 'easeInOutSine'
              });
            }
          }
        });
        
        // Ultra-smooth skill items with elastic bounce
        const skillItems = element.querySelectorAll('.skills-grid span');
        anime({
          targets: skillItems,
          scale: [0, 1.3, 1],
          rotate: [180, -10, 0],
          opacity: [0, 1],
          translateY: [20, 0],
          duration: 500,
          delay: anime.stagger(40, {start: 300}),
          easing: 'easeOutElastic(1, .8)'
        });
      }
      
      // Skip project card animations - removed as requested
      
      // Ultra-smooth education items
      if (element.classList.contains('education-item')) {
        anime({
          targets: element,
          translateX: [-80, 0],
          rotateZ: [8, 0],
          scale: [0.9, 1],
          opacity: [0, 1],
          duration: 800,
          easing: 'easeOutCubic'
        });
      }
      
      // Ultra-smooth contact items with pulse effect
      if (element.classList.contains('contact-item')) {
        anime({
          targets: element,
          translateY: [40, 0],
          scale: [0.85, 1],
          opacity: [0, 1],
          duration: 600,
          delay: anime.stagger(100),
          easing: 'easeOutBack(2)',
          complete: () => {
            // Add subtle pulse animation
            anime({
              targets: element,
              scale: [1, 1.02, 1],
              duration: 2000,
              delay: anime.random(0, 1000),
              loop: true,
              easing: 'easeInOutSine'
            });
          }
        });
      }
      
      // Ultra-smooth service list items with slide effect
      if (element.parentElement.classList.contains('services')) {
        anime({
          targets: element,
          translateX: [-50, 0],
          translateY: [10, 0],
          opacity: [0, 1],
          duration: 500,
          delay: anime.stagger(80),
          easing: 'easeOutCubic'
        });
      }
      
      observer.unobserve(element);
    }
  });
}, observerOptions);

// Select elements to observe for scroll animations
const elementsToAnimate = document.querySelectorAll('.section, .section h2, .section p, .skill-category, .education-item, .contact-item, .services li');

// Don't hide elements initially - let animations handle visibility
elementsToAnimate.forEach(el => {
  // Only hide if not already visible from initial load
  if (!el.classList.contains('hero-content')) {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
  }
  observer.observe(el);
});

// Fallback: Make content visible after 1.5 seconds if animations haven't triggered
setTimeout(() => {
  elementsToAnimate.forEach(el => {
    if (el.style.opacity === '0') {
      anime({
        targets: el,
        opacity: 1,
        translateY: 0,
        duration: 400, // Reduced from 800
        easing: 'easeOutQuad'
      });
    }
  });
}, 1500); // Reduced from 3000

// Interactive Hover Animations
// Enhanced button hover effects - Ultra Smooth
document.querySelectorAll('.btn').forEach(btn => {
  btn.addEventListener('mouseenter', () => {
    anime({
      targets: btn,
      scale: 1.12,
      translateY: -6,
      rotate: 2,
      boxShadow: '0 10px 30px rgba(0, 240, 255, 0.4)',
      duration: 300,
      easing: 'easeOutCubic'
    });
    
    const rect = btn.getBoundingClientRect();
    particleSystem.burst(rect.left + rect.width / 2, rect.top + rect.height / 2, 8);
  });
  
  btn.addEventListener('mouseleave', () => {
    anime({
      targets: btn,
      scale: 1,
      translateY: 0,
      rotate: 0,
      boxShadow: '0 0 0',
      duration: 400,
      easing: 'easeOutCubic'
    });
  });
});

// Project card hover animations - removed as requested

// Ultra-smooth skill item hover animations
document.querySelectorAll('.skills-grid span').forEach(skill => {
  skill.addEventListener('mouseenter', () => {
    anime({
      targets: skill,
      scale: 1.2,
      rotate: 8,
      backgroundColor: 'rgba(0, 240, 255, 0.4)',
      borderColor: '#00f0ff',
      boxShadow: '0 5px 15px rgba(0, 240, 255, 0.3)',
      duration: 300,
      easing: 'easeOutBack(2)'
    });
    
    const rect = skill.getBoundingClientRect();
    particleSystem.burst(rect.left + rect.width / 2, rect.top + rect.height / 2, 5);
  });
  
  skill.addEventListener('mouseleave', () => {
    anime({
      targets: skill,
      scale: 1,
      rotate: 0,
      backgroundColor: 'rgba(255, 255, 255, 0.03)',
      borderColor: 'rgba(255, 255, 255, 0.1)',
      boxShadow: '0 0 0',
      duration: 400,
      easing: 'easeOutCubic'
    });
  });
});

// Ultra-smooth navigation link hover effects
document.querySelectorAll('nav a').forEach(link => {
  link.addEventListener('mouseenter', () => {
    anime({
      targets: link,
      translateY: -4,
      scale: 1.08,
      color: '#00f0ff',
      textShadow: '0 0 10px rgba(0, 240, 255, 0.5)',
      duration: 250,
      easing: 'easeOutCubic'
    });
  });
  
  link.addEventListener('mouseleave', () => {
    anime({
      targets: link,
      translateY: 0,
      scale: 1,
      color: '#fff',
      textShadow: '0 0 0',
      duration: 300,
      easing: 'easeOutCubic'
    });
  });
});

// Ultra-smooth logo hover animation
document.querySelector('.logo-img').addEventListener('mouseenter', () => {
  anime({
    targets: '.logo-img',
    rotate: 360,
    scale: 1.25,
    filter: ['drop-shadow(0 0 30px rgba(0, 240, 255, 1))', 'hue-rotate(180deg)', 'drop-shadow(0 0 30px rgba(0, 240, 255, 1))'],
    duration: 800,
    easing: 'easeInOutCubic'
  });
  
  particleSystem.burst(window.innerWidth / 2, 100, 20);
});

// Ultra-smooth contact item hover animations
document.querySelectorAll('.contact-item').forEach(item => {
  item.addEventListener('mouseenter', () => {
    anime({
      targets: item,
      translateX: 12,
      backgroundColor: 'rgba(0, 240, 255, 0.2)',
      borderColor: '#00f0ff',
      boxShadow: '0 5px 20px rgba(0, 240, 255, 0.3)',
      duration: 300,
      easing: 'easeOutCubic'
    });
  });
  
  item.addEventListener('mouseleave', () => {
    anime({
      targets: item,
      translateX: 0,
      backgroundColor: '#111',
      borderColor: '#1f1f1f',
      boxShadow: '0 0 0',
      duration: 400,
      easing: 'easeOutCubic'
    });
  });
});

// Enhanced email copy with animation
document.querySelectorAll('.email-link').forEach(link => {
  link.addEventListener('click', function () {
    const email = "ahmedbiram47@gmail.com";
    navigator.clipboard.writeText(email).then(() => {
      // Create animated notification
      const notification = document.createElement('div');
      notification.textContent = 'Email Copied! ✨';
      notification.style.cssText = `
        position: fixed;
        top: 30px;
        right: 30px;
        background: linear-gradient(135deg, #00f0ff, #0080ff);
        color: #000;
        padding: 20px 30px;
        border-radius: 50px;
        font-weight: 700;
        font-size: 16px;
        z-index: 10000;
        opacity: 0;
        transform: translateY(-30px) scale(0.8);
        box-shadow: 0 10px 30px rgba(0, 240, 255, 0.5);
      `;
      document.body.appendChild(notification);
      
      // Animate notification
      anime.timeline({
        easing: 'easeOutExpo',
      })
      .add({
        targets: notification,
        opacity: [0, 1],
        translateY: [-30, 0],
        scale: [0.8, 1],
        duration: 600
      })
      .add({
        targets: notification,
        opacity: 0,
        translateY: -30,
        scale: 0.8,
        duration: 500,
        delay: 2000,
        easing: 'easeInQuad',
        complete: () => {
          notification.remove();
        }
      });
      
      // Create particle burst
      particleSystem.burst(window.innerWidth - 100, 60, 10); // Reduced from 20
    });
  });
});

// Enhanced smooth scroll with animation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      const targetPosition = target.offsetTop - 50;
      
      anime({
        targets: 'html, body',
        scrollTop: targetPosition,
        duration: 600,
        easing: 'easeInOutCubic'
      });
    }
  });
});

// Add more ambient particles with varied effects
setInterval(() => {
  const x = Math.random() * window.innerWidth;
  const y = Math.random() * window.innerHeight;
  particleSystem.createParticle(x, y);
}, 800);

// Add floating animation to hero section
setInterval(() => {
  anime({
    targets: '.hero-content',
    translateY: [0, -2, 0],
    duration: 4000,
    easing: 'easeInOutSine'
  });
}, 4000);

// Add subtle pulse to buttons
setInterval(() => {
  anime({
    targets: '.btn',
    scale: [1, 1.02, 1],
    duration: 2000,
    delay: anime.stagger(200),
    easing: 'easeInOutSine'
  });
}, 5000);
