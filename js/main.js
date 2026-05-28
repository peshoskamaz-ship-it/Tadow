/* ============================================================
   TADOW COCKTAIL LOUNGE — main.js
   Shared vanilla JS: nav, scroll-reveal, lightbox, reservation
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
     MOBILE NAV TOGGLE
  ---------------------------------------------------------- */
  const navToggle = document.getElementById('nav-toggle');
  const navLinks  = document.getElementById('nav-links');

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', function () {
      const open = navLinks.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', String(open));
      navToggle.querySelector('span:nth-child(1)').style.transform =
        open ? 'rotate(45deg) translate(5px, 5px)' : '';
      navToggle.querySelector('span:nth-child(2)').style.opacity =
        open ? '0' : '';
      navToggle.querySelector('span:nth-child(3)').style.transform =
        open ? 'rotate(-45deg) translate(5px, -5px)' : '';
    });

    /* Close on nav link click (mobile) */
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
     LANGUAGE TOGGLE STUB
  ---------------------------------------------------------- */
  const langBtn = document.getElementById('lang-toggle');
  if (langBtn) {
    langBtn.addEventListener('click', function () {
      const current = langBtn.textContent.trim();
      langBtn.textContent = current === 'EN' ? 'BG' : 'EN';
      /* Stub — wire up real translations here */
    });
  }

  /* ----------------------------------------------------------
     SCROLL-REVEAL
  ---------------------------------------------------------- */
  function initScrollReveal() {
    const elements = document.querySelectorAll('.reveal');
    if (!elements.length) return;

    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

      elements.forEach(function (el) { observer.observe(el); });
    } else {
      /* Fallback: show all immediately */
      elements.forEach(function (el) { el.classList.add('visible'); });
    }
  }

  /* ----------------------------------------------------------
     GALLERY LIGHTBOX
  ---------------------------------------------------------- */
  function initLightbox() {
    const lightbox = document.getElementById('lightbox');
    if (!lightbox) return;

    const lbImgWrap = lightbox.querySelector('.lightbox-img');
    const lbClose   = lightbox.querySelector('.lightbox-close');
    const items     = document.querySelectorAll('.gallery-item');

    function openLightbox(label) {
      lbImgWrap.textContent = label || 'Photo placeholder';
      lightbox.classList.add('active');
      document.body.style.overflow = 'hidden';
      lbClose.focus();
    }

    function closeLightbox() {
      lightbox.classList.remove('active');
      document.body.style.overflow = '';
    }

    items.forEach(function (item) {
      item.addEventListener('click', function () {
        openLightbox(item.dataset.label || '');
      });
      item.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          openLightbox(item.dataset.label || '');
        }
      });
    });

    if (lbClose) {
      lbClose.addEventListener('click', closeLightbox);
    }

    lightbox.addEventListener('click', function (e) {
      if (e.target === lightbox) closeLightbox();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && lightbox.classList.contains('active')) {
        closeLightbox();
      }
    });
  }

  /* ----------------------------------------------------------
     RESERVATION FORM (visit.html)
  ---------------------------------------------------------- */
  function initReservationForm() {
    const form = document.getElementById('reservation-form');
    if (!form) return;

    const submitBtn     = document.getElementById('reservation-submit');
    const confirmation  = document.getElementById('reservation-confirm');

    if (!submitBtn) return;

    submitBtn.addEventListener('click', function () {
      /* Basic field presence check */
      const name    = form.querySelector('#res-name');
      const date    = form.querySelector('#res-date');
      const time    = form.querySelector('#res-time');
      const party   = form.querySelector('#res-party');

      let valid = true;

      [name, date, time, party].forEach(function (field) {
        if (!field) return;
        if (!field.value.trim()) {
          field.style.borderColor = '#9B2D1F';
          valid = false;
        } else {
          field.style.borderColor = '';
        }
      });

      if (!valid) return;

      /* Show confirmation */
      const guestName = name ? name.value.trim() : 'Guest';
      const resDate   = date ? date.value : '';
      const resTime   = time ? time.value : '';
      const partySize = party ? party.value : '';

      if (confirmation) {
        confirmation.style.display = 'block';
        confirmation.innerHTML =
          '&#10003; Thank you, <strong>' + guestName + '</strong>! ' +
          'Your request for <strong>' + partySize + ' guest' +
          (partySize === '1' ? '' : 's') + '</strong> on ' +
          '<strong>' + resDate + ' at ' + resTime + '</strong> ' +
          'has been received. We will confirm shortly via phone.';
      }

      /* Reset form fields */
      form.querySelectorAll('input, select, textarea').forEach(function (f) {
        f.value = '';
      });
    });
  }

  /* ----------------------------------------------------------
     INIT ON DOM READY
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
