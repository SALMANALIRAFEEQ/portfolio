// Blog post: reading progress bar, active table-of-contents item, TOC open on desktop / collapsed on mobile.
(() => {
  const body = document.querySelector('.post__body');
  if (!body) return;

  const bar = document.querySelector('.read-progress');
  const toc = document.querySelector('.toc');
  const tocLinks = [...document.querySelectorAll('.toc a')];
  const headings = tocLinks.map((a) => document.querySelector(a.getAttribute('href'))).filter(Boolean);

  // TOC: open on desktop (sticky sidebar), collapsed on mobile so the article starts right away
  const desktop = window.matchMedia('(min-width: 1024px)');
  const syncToc = () => { if (toc) toc.open = desktop.matches; };
  syncToc();
  desktop.addEventListener('change', syncToc);
  // On mobile, close the TOC after jumping to a section
  toc?.addEventListener('click', (e) => { if (e.target.closest('a') && !desktop.matches) toc.open = false; });

  let ticking = false;
  const update = () => {
    ticking = false;
    const box = body.getBoundingClientRect();
    const read = Math.min(1, Math.max(0, -box.top / (box.height - window.innerHeight * 0.6)));
    bar?.style.setProperty('--read', read.toFixed(3));

    // Active section = last heading that has passed the upper third of the screen
    const mark = window.innerHeight * 0.33;
    let active = -1;
    headings.forEach((h, i) => { if (h.getBoundingClientRect().top < mark) active = i; });
    tocLinks.forEach((a, i) => {
      a.classList.toggle('is-active', i === active);
      if (i === active) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
    });
  };
  const request = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
  window.addEventListener('scroll', request, { passive: true });
  window.addEventListener('resize', request);
  update();

  // "Readers right now" toast, fixed bottom-right so it is on screen wherever the reader is.
  // Shows 1s after landing (2–5 readers), then 9s after each hide (2–9, never the same twice); each stays 2.5s.
  // The 2nd and 3rd never drop below the first number; from the 4th on the count can go down.
  const SHOW_MS = 2500, GAP_MS = 9000, FIRST_MS = 1000;
  const note = document.createElement('p');
  note.className = 'readers';
  note.setAttribute('aria-hidden', 'true'); // decorative; repeating it to screen readers every 9s would be noise
  document.body.append(note);
  const messages = [
    (n) => `<b>${n} people</b> are reading this right now`,
    (n) => `<b>${n} readers</b> are on this article with you`,
    (n) => `You and <b>${n - 1} others</b> are reading this`,
  ];
  const rand = (min, max) => min + Math.floor(Math.random() * (max - min + 1));
  let first = 0, last = 0, shown = 0;
  const show = () => {
    if (document.hidden) { setTimeout(show, GAP_MS); return; } // only while the reader is actually on the page
    let n;
    if (!shown) n = first = rand(2, 5);
    else do { n = rand(shown < 3 ? first : 2, 9); } while (n === last);
    last = n;
    note.innerHTML = `<i></i><span>${messages[shown % messages.length](n)}</span>`;
    shown++;
    note.classList.add('is-visible');
    setTimeout(() => {
      note.classList.remove('is-visible');
      setTimeout(show, GAP_MS);
    }, SHOW_MS);
  };
  setTimeout(show, FIRST_MS);
})();
