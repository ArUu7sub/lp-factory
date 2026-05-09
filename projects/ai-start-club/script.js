/* ===================================
   AIスタートクラブ — LP スクリプト
   =================================== */

(function () {
  'use strict';

  /* ── ヘッダー: スクロール時クラス付与 ── */
  const header = document.getElementById('header');
  if (header) {
    window.addEventListener('scroll', function () {
      if (window.scrollY > 40) {
        header.classList.add('is-scrolled');
      } else {
        header.classList.remove('is-scrolled');
      }
    }, { passive: true });
  }

  /* ── ハンバーガーメニュー ── */
  const hamburger = document.getElementById('hamburger');
  const mobileNav = document.getElementById('mobileNav');
  if (hamburger && mobileNav) {
    hamburger.addEventListener('click', function () {
      const isOpen = mobileNav.classList.toggle('is-open');
      hamburger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    // モバイルナビのリンクをクリックしたら閉じる
    mobileNav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        mobileNav.classList.remove('is-open');
        hamburger.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ── スクロールリビール (Intersection Observer) ── */
  const revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length > 0 && 'IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
    );
    revealEls.forEach(function (el, i) {
      // 子要素の連鎖アニメーション用の遅延
      el.style.transitionDelay = (i % 4) * 0.08 + 's';
      revealObserver.observe(el);
    });
  } else {
    // フォールバック: オブザーバー非対応ブラウザ
    revealEls.forEach(function (el) {
      el.classList.add('is-visible');
    });
  }

  /* ── スムーズスクロール（ヘッダー高さ分オフセット） ── */
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      const href = this.getAttribute('href');
      if (href === '#') return;
      const target = document.querySelector(href);
      if (!target) return;
      e.preventDefault();
      const headerHeight = header ? header.offsetHeight : 0;
      const top = target.getBoundingClientRect().top + window.scrollY - headerHeight - 16;
      window.scrollTo({ top: top, behavior: 'smooth' });
    });
  });

  /* ── FAQ: details要素アニメーション ── */
  document.querySelectorAll('.faq__item').forEach(function (details) {
    details.addEventListener('toggle', function () {
      // open/close でアロー回転は CSS で対応済み
    });
  });

  /* ── CTAボタン: クリック追跡（オプション） ── */
  document.querySelectorAll('.btn--primary').forEach(function (btn) {
    btn.addEventListener('click', function () {
      // Google Analyticsや計測ツールがある場合はここに追記
      // 例: gtag('event', 'cta_click', { 'button_text': btn.textContent.trim() });
    });
  });

})();
