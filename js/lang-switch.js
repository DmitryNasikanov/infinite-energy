// Language switcher - handles GitHub Pages subdirectory
// NOTE: This script is now inlined in _quarto.yml for reliability
// This file is kept for reference only

const LANGUAGES = { ru: '🇷🇺', en: '🇬🇧' };

function getBasePath() {
  // Extract base path before /ru/ or /en/
  // E.g., "/infinite-energy/ru/science/" -> "/infinite-energy"
  const match = window.location.pathname.match(/^(.*?)\/(ru|en)\//);
  return match ? match[1] : '';
}

function getCurrentLang() {
  const basePath = getBasePath();
  const path = window.location.pathname;
  const escaped = basePath.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const pattern = new RegExp(`^${escaped}/(ru|en)/`);
  const match = path.match(pattern);
  return match ? match[1] : 'ru';
}

function switchLanguage(targetLang) {
  const basePath = getBasePath();
  const path = window.location.pathname;
  const currentLang = getCurrentLang();
  if (currentLang === targetLang) return;

  sessionStorage.setItem('scrollY', window.scrollY);

  const escaped = basePath.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const langPattern = new RegExp(`^(${escaped})/(ru|en)/`);
  let newPath = path.replace(langPattern, `$1/${targetLang}/`);

  // Root page handling
  if (path === basePath + '/' || path === basePath + '/index.html' || path === basePath) {
    newPath = `${basePath}/${targetLang}/`;
  }

  window.location.href = newPath;
}

window.addEventListener('load', function() {
  const savedY = sessionStorage.getItem('scrollY');
  if (savedY) {
    window.scrollTo(0, parseInt(savedY));
    sessionStorage.removeItem('scrollY');
  }
});

document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.dropdown-item').forEach(el => {
    const text = el.textContent;
    for (const [langCode, flag] of Object.entries(LANGUAGES)) {
      if (text.includes(flag)) {
        el.addEventListener('click', function(e) {
          e.preventDefault();
          switchLanguage(langCode);
        });
        if (langCode === getCurrentLang()) {
          el.classList.add('active');
        }
        break;
      }
    }
  });
});
