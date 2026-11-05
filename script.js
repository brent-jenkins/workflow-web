// Mobile menu and the nav's border once scrolled.
// No tracking and nothing stored — see privacy.html.
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

  if (nav) {
    var onScroll = function () { nav.classList.toggle('nav--scrolled', window.scrollY > 8); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

})();
