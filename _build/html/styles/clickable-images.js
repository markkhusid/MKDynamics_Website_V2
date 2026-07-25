(function () {
  function ensureOverlay() {
    var el = document.getElementById('mk-lightbox-overlay');
    if (el) return el;
    el = document.createElement('div');
    el.id = 'mk-lightbox-overlay';
    el.setAttribute('role', 'dialog');
    el.setAttribute('aria-modal', 'true');
    el.innerHTML = '<span id="mk-lightbox-close" aria-label="Close">&times;</span><img alt="" />';
    document.body.appendChild(el);
    function close() { el.classList.remove('open'); }
    el.addEventListener('click', function (e) {
      if (e.target === el || e.target.id === 'mk-lightbox-close' || e.target.tagName === 'IMG') close();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') close();
    });
    return el;
  }
  function openLightbox(src, alt) {
    var el = ensureOverlay();
    var img = el.querySelector('img');
    img.src = src;
    img.alt = alt || '';
    el.classList.add('open');
  }
  function isContentFigureImage(img) {
    if (!img || img.tagName !== 'IMG') return false;
    // Never intercept card / navigation chrome — cards must keep working as links
    if (img.closest('.myst-card') || img.closest('[class*="myst-card"]')) return false;
    if (img.closest('nav') || img.closest('header.myst-card-header')) return false;
    if (img.closest('button')) return false;
    if (img.closest('#mk-lightbox-overlay')) return false;
    // Only expand figures in article content (not bare card thumbs / logos)
    var fig = img.closest('figure.fig-figure, figure.clickable-figure, figure');
    if (!fig) return false;
    if (!img.closest('article, main, .article, .content')) return false;
    // skip tiny icons
    var w = img.naturalWidth || img.width || 0;
    var h = img.naturalHeight || img.height || 0;
    if (w && h && w < 48 && h < 48) return false;
    var src = img.getAttribute('src') || '';
    if (!src || src.indexOf('data:image/svg') === 0) return false;
    if (src.indexOf('favicon') !== -1) return false;
    return true;
  }
  document.addEventListener('click', function (e) {
    var img = e.target.closest && e.target.closest('img');
    if (!isContentFigureImage(img)) return;
    e.preventDefault();
    e.stopPropagation();
    openLightbox(img.currentSrc || img.src, img.alt);
  }, true);
})();
