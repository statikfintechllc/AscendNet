document.addEventListener('DOMContentLoaded', function () {
  const sections = document.querySelectorAll(
    'h1, h2, h3, h4, h5, h6, p, ul, ol, img, code, pre, .glass'
  );

  // GitHub-style slug generator
  function githubSlug(text) {
    return text
      .trim()
      .toLowerCase()
      .replace(/[\s+]+/g, '-')              // spaces to hyphens
      .replace(/[^a-z0-9\-]/g, '')          // remove non-alphanumeric
      .replace(/\-+/g, '-')                 // collapse dashes
      .replace(/^\-+|\-+$/g, '');           // trim leading/trailing hyphens
  }

  // Assign reliable IDs to all headers if missing
  document.querySelectorAll('h1, h2, h3, h4, h5, h6').forEach(header => {
    if (!header.id) {
      header.id = githubSlug(header.textContent);
    }
  });

  // TOC anchor link handling (prevent crash on bad targets)
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    const targetId = link.getAttribute('href').slice(1);
    const target = document.getElementById(targetId);
    if (target) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
        history.pushState(null, null, `#${targetId}`);
      });
    } else {
      console.warn(`Broken TOC link: #${targetId}`);
    }
  });

  // Animate sections on scroll
  const reveal = (el) => {
    el.style.opacity = 1;
    el.style.transform = 'translateY(0)';
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        reveal(entry.target);
      }
    });
  }, { threshold: 0.1 });

  sections.forEach((el) => {
    el.style.opacity = 0;
    el.style.transform = 'translateY(50px)';
    el.style.transition = 'all 0.5s ease-out';
    observer.observe(el);
  });
});
