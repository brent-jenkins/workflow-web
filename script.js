// Mobile menu, the nav's border once scrolled, and gentle fade-ins.
// Nothing stored here; analytics and the cookie choice are in analytics.js (see privacy.html).
(function () {
  var nav = document.querySelector('.nav');
  var burger = document.querySelector('.nav__hamburger');

  if (nav && burger) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('nav--open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    });
    // Close the menu after following one of its links.
    nav.querySelectorAll('.nav__links a').forEach(function (a) {
      a.addEventListener('click', function () {
        nav.classList.remove('nav--open');
        burger.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Language menu: a <details> opens itself; close it on an outside tap or Escape.
  var lang = document.querySelector('.nav__lang');
  if (lang) {
    document.addEventListener('click', function (e) { if (lang.open && !lang.contains(e.target)) lang.open = false; });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') lang.open = false; });
  }

  if (nav) {
    var onScroll = function () { nav.classList.toggle('nav--scrolled', window.scrollY > 8); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // Sections fade in as they scroll into view (styles.css .fade; none with reduced motion).
  var fades = document.querySelectorAll('.fade');
  if (!('IntersectionObserver' in window)) {
    fades.forEach(function (el) { el.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { rootMargin: '0px 0px -60px 0px' });
  fades.forEach(function (el) { io.observe(el); });
})();
