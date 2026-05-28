/* ============================================================
   TADOW COCKTAIL LOUNGE — main.js
   Nav, scroll-reveal, gallery lightbox (arrows + swipe), reservation form
   ============================================================ */

(function () {
  'use strict';

  /* ----------------------------------------------------------
     ACTIVE NAV LINK
  ---------------------------------------------------------- */
  (function setActiveNav() {
    const page = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-links a').forEach(function (a) {
      const href = a.getAttribute('href');
      if (href === page || (page === '' && href === 'index.html')) {
        a.classList.add('active');
        a.setAttribute('aria-current', 'page');
      }
    });
  })();

  /* ----------------------------------------------------------
     MOBILE HAMBURGER TOGGLE
  ---------------------------------------------------------- */
  const navToggle = document.getElementById('nav-toggle');
  const navLinks  = document.getElementById('nav-links');

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', function () {
      const open = navLinks.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', String(open));
      const spans = navToggle.querySelectorAll('span');
      if (open) {
        spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
        spans[1].style.opacity   = '0';
        spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
      } else {
        spans[0].style.transform = '';
        spans[1].style.opacity   = '';
        spans[2].style.transform = '';
      }
    });

    navLinks.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        navLinks.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.querySelectorAll('span').forEach(function (s) {
          s.style.transform = '';
          s.style.opacity   = '';
        });
      });
    });
  }

  /* ----------------------------------------------------------
     SCROLL-REVEAL (IntersectionObserver)
  ---------------------------------------------------------- */
  function initScrollReveal() {
    const elements = document.querySelectorAll('.reveal');
    if (!elements.length) return;

    if (!('IntersectionObserver' in window)) {
      elements.forEach(function (el) { el.classList.add('visible'); });
      return;
    }

    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -30px 0px' });

    elements.forEach(function (el) { observer.observe(el); });
  }

  /* ----------------------------------------------------------
     GALLERY LIGHTBOX
     - Left/right arrow navigation
     - Keyboard ← → Escape
     - Touch swipe support
  ---------------------------------------------------------- */
  function initLightbox() {
    const lightbox   = document.getElementById('lightbox');
    if (!lightbox) return;

    const lbImg      = lightbox.querySelector('.lb-img');
    const lbClose    = lightbox.querySelector('.lightbox-close');
    const lbPrev     = lightbox.querySelector('.lightbox-arrow.prev');
    const lbNext     = lightbox.querySelector('.lightbox-arrow.next');
    const lbCounter  = lightbox.querySelector('.lightbox-counter');
    const items      = Array.from(document.querySelectorAll('.gallery-item'));

    let currentIndex = 0;
    let touchStartX  = 0;

    function openAt(index) {
      currentIndex = index;
      const item   = items[index];
      const img    = item.querySelector('img');
      if (!img) return;

      lbImg.src = img.src;
      lbImg.alt = img.alt;
      lightbox.classList.add('active');
      document.body.style.overflow = 'hidden';
      if (lbCounter) lbCounter.textContent = (index + 1) + ' / ' + items.length;
      lbClose.focus();
    }

    function closeLightbox() {
      lightbox.classList.remove('active');
      document.body.style.overflow = '';
      lbImg.src = '';
    }

    function showPrev() { openAt((currentIndex - 1 + items.length) % items.length); }
    function showNext() { openAt((currentIndex + 1)                 % items.length); }

    items.forEach(function (item, i) {
      item.setAttribute('tabindex', '0');
      item.addEventListener('click',   function () { openAt(i); });
      item.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openAt(i); }
      });
    });

    lbClose.addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', function (e) {
      if (e.target === lightbox) closeLightbox();
    });
    if (lbPrev) lbPrev.addEventListener('click', showPrev);
    if (lbNext) lbNext.addEventListener('click', showNext);

    /* Keyboard navigation */
    document.addEventListener('keydown', function (e) {
      if (!lightbox.classList.contains('active')) return;
      if (e.key === 'Escape')     closeLightbox();
      if (e.key === 'ArrowLeft')  showPrev();
      if (e.key === 'ArrowRight') showNext();
    });

    /* Touch swipe */
    lightbox.addEventListener('touchstart', function (e) {
      touchStartX = e.touches[0].clientX;
    }, { passive: true });

    lightbox.addEventListener('touchend', function (e) {
      const delta = e.changedTouches[0].clientX - touchStartX;
      if (Math.abs(delta) > 50) {
        if (delta < 0) showNext(); else showPrev();
      }
    }, { passive: true });
  }

  /* ----------------------------------------------------------
     RESERVATION FORM (visit.html)
  ---------------------------------------------------------- */
  function initReservationForm() {
    const submitBtn    = document.getElementById('reservation-submit');
    const confirmation = document.getElementById('reservation-confirm');
    const formWrapper  = document.getElementById('res-form-wrapper');
    if (!submitBtn) return;

    submitBtn.addEventListener('click', function () {
      const name    = document.getElementById('res-name');
      const date    = document.getElementById('res-date');
      const time    = document.getElementById('res-time');
      const party   = document.getElementById('res-party');

      let valid = true;
      [name, date, time, party].forEach(function (f) {
        if (!f) return;
        if (!f.value.trim()) {
          f.classList.add('error');
          valid = false;
        } else {
          f.classList.remove('error');
        }
      });
      if (!valid) return;

      /* Format date nicely */
      let displayDate = date.value;
      try {
        displayDate = new Date(date.value).toLocaleDateString('en-GB', {
          weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
        });
      } catch (e) { /* use raw value */ }

      if (formWrapper)  formWrapper.style.display = 'none';
      if (confirmation) {
        confirmation.style.display = 'block';
        confirmation.innerHTML =
          'Thank you, <strong>' + escapeHtml(name.value.trim()) + '</strong>!<br>' +
          'We\'ll confirm your table for <strong>' + partyLabel(party.value) + '</strong><br>' +
          'on <strong>' + displayDate + '</strong> at <strong>' + time.value + '</strong>.<br><br>' +
          'See you soon. 🥂';
      }
    });
  }

  function partyLabel(v) {
    return v === '1' ? '1 guest' : v + ' guests';
  }

  function escapeHtml(str) {
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  /* ----------------------------------------------------------
     INIT
  ---------------------------------------------------------- */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }

  function boot() {
    initScrollReveal();
    initLightbox();
    initReservationForm();
  }

})();
