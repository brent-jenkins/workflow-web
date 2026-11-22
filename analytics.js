// Visitor counts with Cloudflare Web Analytics, and campaign tags passed on to
// Google Play. See privacy.html ("This website") and CLAUDE.md ("Analytics").
//
// - Cloudflare Web Analytics sets no cookies and stores nothing in the browser,
//   so there's no cookie banner anywhere. It reports page views, referrers,
//   countries, device types and browsers as totals, with no visitor identifier.
//   Replaced Google Analytics on 22 November 2026, which needed a banner.
// - Campaign tags in the address (utm_source, utm_medium, utm_campaign…) are
//   carried in the site's own links rather than stored, and added to every
//   Google Play link as Play's install referrer, so Play Console reports
//   installs per channel.
(function () {
  var CF_TOKEN = 'adf4def97174484e8c10831c3a199557'; // Cloudflare dashboard → Web Analytics → zayvori.com (public, not a secret)
  var UTM_PARAMS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];

  // --- Campaign tags → the site's links and the Google Play install referrer ---
  var params = new URLSearchParams(window.location.search);
  var tags = UTM_PARAMS.filter(function (p) { return params.get(p); });
  var utm = tags.map(function (p) { return p + '=' + encodeURIComponent(params.get(p)); }).join('&');
  // Visits with no tags still say they came through the website. Play's
  // reports break installs down by source and campaign, so a campaign is
  // always sent.
  var referrer = utm || 'utm_source=zayvori.com&utm_medium=website';
  if (!params.get('utm_campaign')) referrer += '&utm_campaign=website';

  document.querySelectorAll('a[href]').forEach(function (a) {
    var url;
    try { url = new URL(a.href, window.location.href); } catch (e) { return; }
    if (url.hostname === 'play.google.com' && url.pathname === '/store/apps/details') {
      url.searchParams.set('referrer', referrer);
      a.href = url.toString();
    } else if (tags.length && url.origin === window.location.origin && !/^(mailto|tel):/.test(a.href)) {
      // Keep the tags for the next page of the visit (not for links within this page).
      if (url.pathname === window.location.pathname && url.hash) return;
      tags.forEach(function (p) { url.searchParams.set(p, params.get(p)); });
      a.href = url.toString();
    }
  });

  // --- Cloudflare Web Analytics ---------------------------------------------
  if (!/^[0-9A-Za-z]{20,}$/.test(CF_TOKEN)) return;
  var s = document.createElement('script');
  s.defer = true;
  s.src = 'https://static.cloudflareinsights.com/beacon.min.js';
  s.setAttribute('data-cf-beacon', JSON.stringify({ token: CF_TOKEN }));
  document.head.appendChild(s);
})();
