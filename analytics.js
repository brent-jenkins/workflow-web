// Google Analytics 4 in Consent Mode, and campaign tags passed on to Google Play.
// See privacy.html ("This website") and CLAUDE.md ("Analytics").
//
// - Nothing is stored and no cookie is set until a visitor says yes in the
//   banner. Until then (or after "No thanks") Google Analytics only gets
//   cookieless pings with no identifier, which it uses for modelled totals.
// - Advertising signals are always off: Zayvori doesn't advertise with Google data.
// - The choice is kept in localStorage ("zayvori-analytics": granted | denied);
//   privacy.html has a button to change it.
// - Loaded directly (gtag.js), not through Tag Manager, so what runs is what's
//   written here. The setup wizard also made a Tag Manager container
//   (GTM-WNPLFFJW) holding this same ID; it isn't used.
// - Campaign tags in the address (utm_source, utm_medium, utm_campaign…) are
//   kept for the visit (sessionStorage) and added to every Google Play link as
//   Play's install referrer, so Play Console reports installs per channel.
(function () {
  var MEASUREMENT_ID = 'G-0JTQS1CLRC'; // the GA4 web stream for zayvori.com
  var CHOICE_KEY = 'zayvori-analytics';
  var UTM_KEY = 'zayvori-utm';
  var UTM_PARAMS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];

  function read(store, key) { try { return window[store].getItem(key); } catch (e) { return null; } }
  function write(store, key, value) { try { window[store].setItem(key, value); } catch (e) { /* private mode */ } }
  function remove(store, key) { try { window[store].removeItem(key); } catch (e) { /* private mode */ } }

  // --- Campaign tags → Google Play install referrer -------------------------
  var params = new URLSearchParams(window.location.search);
  var utm = UTM_PARAMS.filter(function (p) { return params.get(p); })
    .map(function (p) { return p + '=' + encodeURIComponent(params.get(p)); }).join('&');
  if (utm) write('sessionStorage', UTM_KEY, utm);
  else utm = read('sessionStorage', UTM_KEY) || '';
  // Visits with no tags still say they came through the website.
  var referrer = utm || 'utm_source=zayvori.com&utm_medium=website';
  document.querySelectorAll('a[href^="https://play.google.com/store/apps/details"]').forEach(function (a) {
    var url = new URL(a.href);
    url.searchParams.set('referrer', referrer);
    a.href = url.toString();
  });

  // --- Google Analytics -----------------------------------------------------
  if (!/^G-[A-Z0-9]{6,}$/.test(MEASUREMENT_ID)) return;

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = gtag;

  var choice = read('localStorage', CHOICE_KEY);
  gtag('consent', 'default', {
    analytics_storage: choice === 'granted' ? 'granted' : 'denied',
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
  });
  gtag('set', 'ads_data_redaction', true);
  gtag('js', new Date());
  gtag('config', MEASUREMENT_ID, { allow_google_signals: false, allow_ad_personalization_signals: false });

  var s = document.createElement('script');
  s.async = true;
  s.src = 'https://www.googletagmanager.com/gtag/js?id=' + MEASUREMENT_ID;
  document.head.appendChild(s);

  // Installs start with a tap on a Play link: the event play_store_click.
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href^="https://play.google.com/"]');
    if (a) gtag('event', 'play_store_click', { link_text: (a.textContent || '').trim().slice(0, 40) });
  });

  // --- The banner -------------------------------------------------------------
  function decide(value) {
    write('localStorage', CHOICE_KEY, value);
    gtag('consent', 'update', { analytics_storage: value });
    // This page was only a cookieless ping until now, which reports don't
    // show; counted properly once the visitor agrees.
    if (value === 'granted') gtag('event', 'page_view');
    var b = document.querySelector('.consent');
    if (b) b.remove();
  }

  function showBanner() {
    if (document.querySelector('.consent')) return;
    var b = document.createElement('div');
    b.className = 'consent';
    b.setAttribute('role', 'region');
    b.setAttribute('aria-label', 'Cookie choice');
    b.innerHTML =
      '<p>We use Google Analytics cookies to see how people find Zayvori. ' +
      'Nothing in the app is tracked. <a href="/privacy.html#website">More</a></p>' +
      '<div class="consent__buttons">' +
      '<button type="button" class="btn btn--ghost btn--sm consent__no">No thanks</button>' +
      '<button type="button" class="btn btn--primary btn--sm consent__yes">That’s fine</button>' +
      '</div>';
    b.querySelector('.consent__yes').addEventListener('click', function () { decide('granted'); });
    b.querySelector('.consent__no').addEventListener('click', function () { decide('denied'); });
    document.body.appendChild(b);
  }

  if (choice !== 'granted' && choice !== 'denied') showBanner();

  // privacy.html: "Change your cookie choice".
  document.querySelectorAll('[data-cookie-choice]').forEach(function (el) {
    el.hidden = false;
    el.addEventListener('click', function (e) {
      e.preventDefault();
      remove('localStorage', CHOICE_KEY);
      showBanner();
    });
  });
})();
