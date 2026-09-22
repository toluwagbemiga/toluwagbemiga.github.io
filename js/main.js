// Theme toggle, mobile nav, project filters, scroll reveals, active section in the header.
(() => {
  const root = document.documentElement;

  // theme
  document.getElementById('theme')?.addEventListener('click', () => {
    const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    try {
      localStorage.setItem('theme', next);
    } catch {
      /* private mode */
    }
  });

  // mobile nav
  const nav = document.getElementById('nav');
  const navToggle = document.getElementById('nav-toggle');
  navToggle?.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    navToggle.setAttribute('aria-expanded', String(open));
  });
  nav?.addEventListener('click', (e) => {
    if (e.target.tagName === 'A') {
      nav.classList.remove('is-open');
      navToggle?.setAttribute('aria-expanded', 'false');
    }
  });

  // header hairline once scrolled
  const header = document.querySelector('.site-header');
  const onScroll = () => header?.classList.toggle('is-stuck', window.scrollY > 8);
  onScroll();
  addEventListener('scroll', onScroll, { passive: true });

  // project filters
  const grid = document.getElementById('projects-grid');
  document.querySelectorAll('.filter').forEach((button) => {
    button.addEventListener('click', () => {
      const tag = button.dataset.filter;
      document.querySelectorAll('.filter').forEach((b) => b.setAttribute('aria-pressed', String(b === button)));
      grid?.querySelectorAll('.project').forEach((card) => {
        const tags = (card.dataset.tags || '').split(',');
        card.style.display = tag === 'All' || tags.includes(tag) ? '' : 'none';
      });
    });
  });

  // reveal on scroll; anything still hidden after 1.2s is shown anyway (printing, no scroll, odd browsers)
  const hidden = [...document.querySelectorAll('[data-reveal]')];
  const show = (el) => el.classList.add('is-visible');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      (entries) => entries.forEach((entry) => entry.isIntersecting && (show(entry.target), io.unobserve(entry.target))),
      { rootMargin: '0px 0px -8% 0px' },
    );
    hidden.forEach((el) => io.observe(el));
    setTimeout(() => hidden.forEach(show), 1200);
  } else {
    hidden.forEach(show);
  }

  // highlight the section you're in
  const links = [...document.querySelectorAll('.nav a')];
  const sections = links.map((a) => document.querySelector(a.getAttribute('href'))).filter(Boolean);
  if ('IntersectionObserver' in window && sections.length) {
    const spy = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          links.forEach((a) => a.classList.toggle('is-active', a.getAttribute('href') === `#${entry.target.id}`));
        });
      },
      { rootMargin: '-45% 0px -50% 0px' },
    );
    sections.forEach((s) => spy.observe(s));
  }
})();
