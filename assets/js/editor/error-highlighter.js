// DocCollab-v0
// AST é a única fonte de verdade.
// Nenhuma lógica fora do modelo semântico é permitida.
// error-highlighter.js — destaca blocos referentes a erros de compilação

const STYLE_ID = 'doccollab-error-highlights-style';

function ensureStyle(){
  if (document.getElementById(STYLE_ID)) return;
  const css = `
  .doccollab-block-error {
    outline: 3px solid rgba(220,38,38,0.9) !important;
    background: rgba(255,230,230,0.6) !important;
    transition: box-shadow 180ms ease, background 180ms ease;
  }
  `;
  const s = document.createElement('style'); s.id = STYLE_ID; s.textContent = css; document.head.appendChild(s);
}

let current = [];

export function clearHighlights(){
  current.forEach(el => { if(el && el.classList) el.classList.remove('doccollab-block-error'); });
  current = [];
}

export function scrollToBlock(blockId){
  const el = document.querySelector(`[data-block-id="${blockId}"]`);
  if(!el) return false;
  if (typeof el.scrollIntoView === 'function') {
    try{ el.scrollIntoView({ behavior: 'smooth', block: 'center' }); }catch(e){ el.scrollIntoView(); }
  }
  return true;
}

// errors: array of { blockId, message?, severity? }
export function highlightErrors(errors){
  ensureStyle();
  clearHighlights();
  if(!errors) return;
  const arr = Array.isArray(errors) ? errors : [errors];
  for(const err of arr){
    if(!err || !err.blockId) continue;
    const el = document.querySelector(`[data-block-id="${err.blockId}"]`);
    if(!el) continue;
    el.classList.add('doccollab-block-error');
    if(err.message) el.setAttribute('title', err.message);
    current.push(el);
  }
  // scroll to first (guard para ambientes sem DOM completo)
  if(current.length) {
    const first = current[0];
    if (first && typeof first.scrollIntoView === 'function') {
      try{ first.scrollIntoView({ behavior: 'smooth', block: 'center' }); }catch(e){ first.scrollIntoView(); }
    }
  }
}

// default export convenience
export default { highlightErrors, clearHighlights, scrollToBlock };
