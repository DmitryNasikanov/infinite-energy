// Конфигурация языков — легко добавить новые
const LANGUAGES = {
  ru: { code: 'ru', flag: '🇷🇺' },
  en: { code: 'en', flag: '🇬🇧' },
  // zh: { code: 'zh', flag: '🇨🇳' },
  // es: { code: 'es', flag: '🇪🇸' },
};

// Определить текущий язык из URL
function getCurrentLang() {
  const match = window.location.pathname.match(/^\/(ru|en|zh|es)\//);
  return match ? match[1] : 'ru'; // default: ru
}

// Переключить на другой язык
function switchLanguage(targetLang) {
  const path = window.location.pathname;
  const currentLang = getCurrentLang();

  if (currentLang === targetLang) return;

  // Сохранить позицию скролла
  sessionStorage.setItem('scrollY', window.scrollY);

  // Заменить язык в пути
  const langPattern = new RegExp(`^/(${Object.keys(LANGUAGES).join('|')})/`);
  let newPath = path.replace(langPattern, `/${targetLang}/`);

  // Корневая страница
  if (path === '/' || path === '/index.html') {
    newPath = `/${targetLang}/`;
  }

  window.location.href = newPath;
}

// Восстановить позицию после загрузки
window.addEventListener('load', function() {
  const savedY = sessionStorage.getItem('scrollY');
  if (savedY) {
    window.scrollTo(0, parseInt(savedY));
    sessionStorage.removeItem('scrollY');
  }
});

// Навесить обработчики на кнопки языков
document.addEventListener('DOMContentLoaded', function() {
  // Найти элементы меню по флагу в тексте
  document.querySelectorAll('.dropdown-item').forEach(el => {
    const text = el.textContent;

    // Определить язык по флагу
    for (const [langCode, langConfig] of Object.entries(LANGUAGES)) {
      if (text.includes(langConfig.flag)) {
        // Перехватить клик
        el.addEventListener('click', function(e) {
          e.preventDefault();
          switchLanguage(langCode);
        });

        // Подсветить текущий язык
        if (langCode === getCurrentLang()) {
          el.classList.add('active');
        }
        break;
      }
    }
  });
});
