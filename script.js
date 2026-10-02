(() => {
  document.documentElement.classList.add('js');

  const nav = document.getElementById('nav');
  const toggle = document.querySelector('.nav__toggle');
  const menu = document.getElementById('menu');
  const links = [...document.querySelectorAll('.nav__link')];

  // Preloader
  const hidePreloader = () => document.querySelector('.preloader')?.classList.add('is-done');
  window.addEventListener('load', () => setTimeout(hidePreloader, 400));
  setTimeout(hidePreloader, 3000);

  // Nav shadow on scroll
  const onScroll = () => nav.classList.toggle('is-scrolled', window.scrollY > 10);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  // Mobile menu
  const setMenu = (open) => {
    menu.classList.toggle('is-open', open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  };
  toggle.addEventListener('click', () => setMenu(!menu.classList.contains('is-open')));
  menu.addEventListener('click', (e) => { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setMenu(false); });

  // Scroll reveals
  const reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => {
        if (en.isIntersecting) { en.target.classList.add('is-visible'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12 });
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add('is-visible'));
  }

  // Active section highlight
  const sections = links.map((a) => document.querySelector(a.getAttribute('href'))).filter(Boolean);
  const spy = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      links.forEach((a) => {
        const on = a.getAttribute('href') === '#' + en.target.id;
        a.classList.toggle('is-active', on);
        if (on) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
      });
    });
  }, { rootMargin: '-45% 0px -50% 0px' });
  sections.forEach((s) => spy.observe(s));
  new IntersectionObserver(([en]) => {
    if (en.isIntersecting) links.forEach((a) => { a.classList.remove('is-active'); a.removeAttribute('aria-current'); });
  }, { rootMargin: '-45% 0px -50% 0px' }).observe(document.getElementById('hero'));

  // Journey: fill the track as it scrolls past the middle of the screen and light up reached steps.
  const journey = document.getElementById('journey');
  if (journey) {
    const steps = [...journey.querySelectorAll('.journey__step')];
    let ticking = false;
    const update = () => {
      ticking = false;
      const mark = window.innerHeight * 0.6;
      const box = journey.getBoundingClientRect();
      const progress = Math.min(1, Math.max(0, (mark - box.top) / box.height));
      journey.style.setProperty('--progress', progress.toFixed(3));
      steps.forEach((s) => s.classList.toggle('is-active', s.getBoundingClientRect().top + 20 < mark));
    };
    const request = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
    window.addEventListener('scroll', request, { passive: true });
    window.addEventListener('resize', request);
    update();
  }

  // Skills rows: on touch screens (no hover) the row crossing the middle of the screen fills in.
  if (window.matchMedia('(hover: none)').matches) {
    const rowSpy = new IntersectionObserver((entries) => {
      entries.forEach((en) => en.target.classList.toggle('is-active', en.isIntersecting));
    }, { rootMargin: '-45% 0px -45% 0px' });
    document.querySelectorAll('.stack__row').forEach((r) => rowSpy.observe(r));
  }

  // Email buttons: Gmail compose in a new tab on desktop; phones keep mailto so the mail app opens.
  const isTouch = window.matchMedia('(hover: none), (pointer: coarse)').matches;
  document.querySelectorAll('.js-email').forEach((a) => {
    a.addEventListener('click', (e) => {
      if (isTouch) return;
      e.preventDefault();
      const to = a.getAttribute('href').replace('mailto:', '');
      window.open('https://mail.google.com/mail/?view=cm&fs=1&to=' + encodeURIComponent(to), '_blank', 'noopener');
    });
  });

  document.getElementById('year').textContent = new Date().getFullYear();
})();
