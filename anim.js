/* Animations douces : apparition au scroll (auto sur les blocs clés) */
document.addEventListener('DOMContentLoaded', function () {
  var sel = '.hero, section, .card, .value, .act, .member, .callout, .steps li, .flag-banner, table';
  var els = document.querySelectorAll(sel);
  els.forEach(function (el, i) {
    el.classList.add('reveal');
    el.style.transitionDelay = (i % 6) * 60 + 'ms';
  });
  if (!('IntersectionObserver' in window)) {
    els.forEach(function (el) { el.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    });
  }, { threshold: 0.12 });
  els.forEach(function (el) { io.observe(el); });
});
