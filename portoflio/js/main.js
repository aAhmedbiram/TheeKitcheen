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

// Enhanced entrance animations with anime.js
window.addEventListener('load', () => {
  // Morphing background blobs
  anime({
    targets: '.blob',
    borderRadius: function() {
      return anime.random(25, 75) + '%';
    },
    scale: function() {
      return anime.random(0.8, 1.3);
    },
    rotate: function() {
      return anime.random(-180, 180);
    },
    duration: function() {
      return anime.random(8000, 12000);
    },
    delay: anime.stagger(200),
    loop: true,
    direction: 'alternate',
    easing: 'easeInOutQuad'
  });
  
  // Dramatic hero entrance animation
  anime.timeline({
    easing: 'easeOutExpo',
  })
  .add({
    targets: '.logo-img',
    scale: [0, 1.2, 1],
    opacity: [0, 1],
    rotate: [720, 0],
    duration: 2000,
    delay: 300
  })
  .add({
    targets: 'nav ul li',
    translateY: [100, 0],
    opacity: [0, 1],
    rotate: [15, 0],
    duration: 800,
    delay: anime.stagger(80, {start: 800})
  }, '-=1000')
  .add({
    targets: '.profile-img',
    scale: [0, 1.3, 1],
    opacity: [0, 1],
    borderRadius: ['50%', '30%', '50%'],
    duration: 1500,
    easing: 'easeOutElastic(1, .5)'
  }, '-=600')
  .add({
    targets: '.hero-content h1',
    translateY: [80, 0],
    opacity: [0, 1],
    scale: [0.8, 1],
    duration: 1200,
    easing: 'easeOutBack(1.7)'
  }, '-=800')
  .add({
    targets: '.hero-content h3',
    translateY: [60, 0],
    opacity: [0, 1],
    duration: 1000,
    complete: () => {
      // Start scramble animation for subtitle
      const fx = new TextScramble(document.querySelector('.hero-content h3'));
      fx.setText('Full Stack Developer');
    }
  }, '-=400')
  .add({
    targets: '.hero-content p',
    translateY: [40, 0],
    opacity: [0, 1],
    duration: 800
  }, '-=200')
  .add({
    targets: '.contact-info p',
    translateX: [-80, 0],
    opacity: [0, 1],
    duration: 600,
    delay: anime.stagger(100)
  })
  .add({
    targets: '.buttons .btn',
    translateY: [60, 0],
    opacity: [0, 1],
    scale: [0.5, 1],
    duration: 800,
    delay: anime.stagger(150),
    easing: 'easeOutBack(1.7)',
    begin: () => {
      particleSystem.burst(window.innerWidth / 2, window.innerHeight / 2, 30);
    }
  }, '-=200');
});

// Enhanced Scroll Animations with Anime.js
const observerOptions = {
  threshold: 0.1,
  rootMargin: "0px"
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const element = entry.target;
      
      // Animate section headers with scramble effect
      if (element.classList.contains('section') && element.querySelector('h2')) {
        const h2 = element.querySelector('h2');
        anime({
          targets: h2,
          translateY: [60, 0],
          opacity: [0, 1],
          duration: 1000,
          easing: 'easeOutQuad',
          complete: () => {
            const fx = new TextScramble(h2);
            fx.setText(h2.innerText);
          }
        });
      }
      
      // Animate paragraphs
      if (element.tagName === 'P' && element.parentElement.classList.contains('section')) {
        anime({
          targets: element,
          translateY: [40, 0],
          opacity: [0, 1],
          duration: 800,
          delay: 200,
          easing: 'easeOutQuad'
        });
      }
      
      // Animate skill categories with 3D effect
      if (element.classList.contains('skill-category')) {
        anime({
          targets: element,
          translateY: [80, 0],
          rotateX: [45, 0],
          opacity: [0, 1],
          duration: 1000,
          delay: anime.stagger(300),
          easing: 'easeOutQuad'
        });
        
        // Animate skill items with bounce effect
        const skillItems = element.querySelectorAll('.skills-grid span');
        anime({
          targets: skillItems,
          scale: [0, 1.2, 1],
          rotate: [180, 0],
          opacity: [0, 1],
          duration: 600,
          delay: anime.stagger(50, {start: 500}),
          easing: 'easeOutBack(1.7)'
        });
      }
      
      // 3D Card flip animations for projects
      if (element.classList.contains('project-card')) {
        anime({
          targets: element,
          rotateY: [90, 0],
          translateY: [100, 0],
          opacity: [0, 1],
          duration: 1000,
          delay: anime.stagger(200),
          easing: 'easeOutQuad',
          begin: () => {
            const rect = element.getBoundingClientRect();
            particleSystem.burst(rect.left + rect.width / 2, rect.top + rect.height / 2, 15);
          }
        });
      }
      
      // Animate education items
      if (element.classList.contains('education-item')) {
        anime({
          targets: element,
          translateX: [-100, 0],
          rotateZ: [10, 0],
          opacity: [0, 1],
          duration: 1000,
          easing: 'easeOutQuad'
        });
      }
      
      // Animate contact items
      if (element.classList.contains('contact-item')) {
        anime({
          targets: element,
          translateY: [50, 0],
          scale: [0.8, 1],
          opacity: [0, 1],
          duration: 800,
          delay: anime.stagger(150),
          easing: 'easeOutBack(1.7)'
        });
      }
      
      // Animate service list items
      if (element.parentElement.classList.contains('services')) {
        anime({
          targets: element,
          translateX: [-60, 0],
          opacity: [0, 1],
          duration: 600,
          delay: anime.stagger(100),
          easing: 'easeOutQuad'
        });
      }
      
      observer.unobserve(element);
    }
  });
}, observerOptions);

// Select elements to observe for scroll animations
const elementsToAnimate = document.querySelectorAll('.section, .section h2, .section p, .skill-category, .project-card, .education-item, .contact-item, .services li');

elementsToAnimate.forEach(el => {
  el.style.opacity = '0';
  observer.observe(el);
});

// Interactive Hover Animations
// Enhanced button hover effects
document.querySelectorAll('.btn').forEach(btn => {
  btn.addEventListener('mouseenter', () => {
    anime({
      targets: btn,
      scale: 1.15,
      translateY: -8,
      rotate: 2,
      duration: 300,
      easing: 'easeOutQuad'
    });
    
    const rect = btn.getBoundingClientRect();
    particleSystem.burst(rect.left + rect.width / 2, rect.top + rect.height / 2, 10);
  });
  
  btn.addEventListener('mouseleave', () => {
    anime({
      targets: btn,
      scale: 1,
      translateY: 0,
      rotate: 0,
      duration: 300,
      easing: 'easeOutQuad'
    });
  });
});

// 3D Project card hover animations
document.querySelectorAll('.project-card').forEach(card => {
  card.addEventListener('mouseenter', () => {
    anime({
      targets: card,
      translateY: -20,
      scale: 1.08,
      rotateX: 5,
      rotateY: 5,
      boxShadow: '0 30px 60px rgba(0, 240, 255, 0.4)',
      duration: 400,
      easing: 'easeOutQuad'
    });
  });
  
  card.addEventListener('mouseleave', () => {
    anime({
      targets: card,
      translateY: 0,
      scale: 1,
      rotateX: 0,
      rotateY: 0,
      boxShadow: '0 20px 40px rgba(0, 0, 0, 0.4), 0 0 20px rgba(0, 240, 255, 0.1)',
      duration: 400,
      easing: 'easeOutQuad'
    });
  });
});

// Skill item hover animations
document.querySelectorAll('.skills-grid span').forEach(skill => {
  skill.addEventListener('mouseenter', () => {
    anime({
      targets: skill,
      scale: 1.3,
      rotate: 10,
      backgroundColor: 'rgba(0, 240, 255, 0.3)',
      borderColor: '#00f0ff',
      duration: 300,
      easing: 'easeOutBack(1.7)'
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
      duration: 300,
      easing: 'easeOutQuad'
    });
  });
});

// Navigation link hover effects
document.querySelectorAll('nav a').forEach(link => {
  link.addEventListener('mouseenter', () => {
    anime({
      targets: link,
      translateY: -5,
      scale: 1.1,
      color: '#00f0ff',
      duration: 200,
      easing: 'easeOutQuad'
    });
  });
  
  link.addEventListener('mouseleave', () => {
    anime({
      targets: link,
      translateY: 0,
      scale: 1,
      color: '#fff',
      duration: 200,
      easing: 'easeOutQuad'
    });
  });
});

// Logo hover animation
document.querySelector('.logo-img').addEventListener('mouseenter', () => {
  anime({
    targets: '.logo-img',
    rotate: 360,
    scale: 1.3,
    filter: 'drop-shadow(0 0 40px rgba(0, 240, 255, 1))',
    duration: 1000,
    easing: 'easeInOutQuad'
  });
  
  particleSystem.burst(window.innerWidth / 2, 100, 25);
});

// Contact item hover animations
document.querySelectorAll('.contact-item').forEach(item => {
  item.addEventListener('mouseenter', () => {
    anime({
      targets: item,
      translateX: 15,
      backgroundColor: 'rgba(0, 240, 255, 0.15)',
      borderColor: '#00f0ff',
      duration: 300,
      easing: 'easeOutQuad'
    });
  });
  
  item.addEventListener('mouseleave', () => {
    anime({
      targets: item,
      translateX: 0,
      backgroundColor: '#111',
      borderColor: '#1f1f1f',
      duration: 300,
      easing: 'easeOutQuad'
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
      particleSystem.burst(window.innerWidth - 100, 60, 20);
    });
  });
});

// Smooth scroll with animation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      const targetPosition = target.offsetTop - 50;
      
      anime({
        targets: 'html, body',
        scrollTop: targetPosition,
        duration: 1200,
        easing: 'easeInOutQuad'
      });
    }
  });
});

// Add some ambient particles periodically
setInterval(() => {
  const x = Math.random() * window.innerWidth;
  const y = Math.random() * window.innerHeight;
  particleSystem.createParticle(x, y);
}, 500);
