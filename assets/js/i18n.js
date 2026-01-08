// DocCollab-v0
// AST é a única fonte de verdade.
// Nenhuma lógica fora do modelo semântico é permitida.

// i18n.js — minimal internationalization loader
const DEFAULT_LOCALE = 'pt-BR';
let _locale = DEFAULT_LOCALE;
let _strings = {};

async function loadLocale(locale){
  _locale = locale || DEFAULT_LOCALE;
  try{
    const res = await fetch(`/assets/i18n/${_locale}.json`);
    if(!res.ok) throw new Error('locale not found');
    _strings = await res.json();
  }catch(e){
    console.warn('i18n: failed to load', e);
    _strings = {};
  }
}

function t(key, fallback){
  return (_strings && _strings[key]) || fallback || key;
}

function translateDOM(root = document){
  const nodes = root.querySelectorAll('[data-i18n]');
  nodes.forEach(n => {
    const k = n.getAttribute('data-i18n');
    const txt = t(k);
    if(n.placeholder !== undefined && (n.tagName === 'INPUT' || n.tagName === 'TEXTAREA')) n.placeholder = txt;
    else if(n.tagName === 'IMG') n.alt = txt;
    else n.textContent = txt;
  });
}

export { loadLocale, t, translateDOM };
