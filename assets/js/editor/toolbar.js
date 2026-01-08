// Toolbar for DocCollab editor
console.log('=== TOOLBAR.JS CARREGADO - VERSÃO 004 ===');
export function createToolbar() {
  console.log('=== createToolbar() CHAMADO ===');
  const toolbar = document.createElement('div');
  toolbar.className = 'doc-toolbar';

  // tooltip element (custom visual tooltip to show shortcuts/help)
  const tooltipEl = document.createElement('div');
  tooltipEl.className = 'toolbar-tooltip';
  Object.assign(tooltipEl.style, {
    position: 'fixed',
    padding: '6px 8px',
    background: 'rgba(0,0,0,0.85)',
    color: '#fff',
    borderRadius: '4px',
    fontSize: '12px',
    zIndex: 10000,
    display: 'none',
    pointerEvents: 'none',
    transition: 'opacity 0.12s ease',
    opacity: '0'
  });
  document.addEventListener('DOMContentLoaded', () => {
    document.body.appendChild(tooltipEl);
  });

  function showTooltip(btn, text) {
    if (!text) return;
    tooltipEl.textContent = text;
    tooltipEl.style.display = 'block';
    tooltipEl.style.opacity = '1';
    const r = btn.getBoundingClientRect();
    const left = Math.max(8, r.left + r.width / 2 - 60);
    const top = r.top - 10;
    tooltipEl.style.left = left + 'px';
    // place above button if possible otherwise below
    if (top > 24) tooltipEl.style.top = (top - tooltipEl.offsetHeight) + 'px';
    else tooltipEl.style.top = (r.bottom + 8) + 'px';
  }

  function hideTooltip() {
    tooltipEl.style.opacity = '0';
    // keep display none after transition
    setTimeout(() => (tooltipEl.style.display = 'none'), 140);
  }

  function makeButton(text, title, cb) {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'toolbar-btn';
    btn.textContent = text;
    // set accessible tooltip/title so hover shows shortcut/help
    if (title) {
      btn.title = title;
      btn.setAttribute('aria-label', title);
    }
    btn.addEventListener('click', (e) => { e.preventDefault(); cb(); });
    // custom tooltip handlers (visual) + keyboard focus
    btn.addEventListener('mouseenter', () => { if (title) showTooltip(btn, title); });
    btn.addEventListener('mouseleave', hideTooltip);
    btn.addEventListener('focus', () => { if (title) showTooltip(btn, title); });
    btn.addEventListener('blur', hideTooltip);
    return btn;
  }

  function applyTag(tag) {
    const sel = window.getSelection();
    if (!sel || sel.rangeCount === 0) return;
    const range = sel.getRangeAt(0);
    if (!range || range.collapsed) return;
    // Wrap selection in a tag preserving HTML
    const wrapper = document.createElement(tag);
    try {
      wrapper.appendChild(range.extractContents());
      range.insertNode(wrapper);
      // move caret after inserted node
      range.setStartAfter(wrapper);
      range.collapse(true);
      sel.removeAllRanges();
      sel.addRange(range);
      // emit block:edited so controller updates AST
      let node = wrapper;
      while (node && !node.dataset?.blockId) node = node.parentElement;
      // try finding enclosing block div
      let blockEl = wrapper.closest('.block');
      if (blockEl) {
        const id = blockEl.dataset.blockId;
        const field = blockEl.querySelector('p,div,h1,h2,h3,pre') ? 'text' : 'text';
        window.dispatchEvent(new CustomEvent('block:edited', { detail: { id, field, value: blockEl.innerHTML } }));
      }
    } catch (e) {
      console.error('applyTag error', e);
    }
  }

  toolbar.appendChild(makeButton('B', 'Negrito (Ctrl+B)', () => applyTag('strong')));
  toolbar.appendChild(makeButton('I', 'Itálico (Ctrl+I)', () => applyTag('em')));
  toolbar.appendChild(makeButton('{ }', 'Código', () => applyTag('code')));
  // delete button
  toolbar.appendChild(makeButton('🗑', 'Apagar bloco atual (Del)', () => window.dispatchEvent(new CustomEvent('toolbar:delete'))));
  toolbar.appendChild(makeButton('↑', 'Mover bloco para cima', () => window.dispatchEvent(new CustomEvent('toolbar:move', { detail: { dir: 'up' } }))));
  toolbar.appendChild(makeButton('↓', 'Mover bloco para baixo', () => window.dispatchEvent(new CustomEvent('toolbar:move', { detail: { dir: 'down' } }))));
  // insert buttons
  toolbar.appendChild(makeButton('\u2795 Sec', 'Inserir Seção', () => window.dispatchEvent(new CustomEvent('toolbar:insert', { detail: { type: 'section' } }))));
  toolbar.appendChild(makeButton('\u2795 Sub', 'Inserir Subseção', () => window.dispatchEvent(new CustomEvent('toolbar:insert', { detail: { type: 'subsection' } }))));
  toolbar.appendChild(makeButton('\u2795 ¶', 'Inserir Parágrafo', () => window.dispatchEvent(new CustomEvent('toolbar:insert', { detail: { type: 'paragraph' } }))));
  toolbar.appendChild(makeButton('\u2795 Σ', 'Inserir Equação', () => window.dispatchEvent(new CustomEvent('toolbar:insert', { detail: { type: 'equation' } }))));
  toolbar.appendChild(makeButton('\u2795 🖼', 'Inserir Figura', () => window.dispatchEvent(new CustomEvent('toolbar:insert', { detail: { type: 'figure' } }))));
  toolbar.appendChild(makeButton('\u2795 ⌗', 'Inserir Tabela', () => window.dispatchEvent(new CustomEvent('toolbar:insert', { detail: { type: 'table' } }))));
  toolbar.appendChild(makeButton('\u2795 📄', 'Inserir Quebra de Página', () => window.dispatchEvent(new CustomEvent('toolbar:insert', { detail: { type: 'pagebreak' } }))));
  toolbar.appendChild(makeButton('\u2795 ✎', 'Inserir Citação', () => window.dispatchEvent(new CustomEvent('toolbar:insert', { detail: { type: 'citation' } }))));
  toolbar.appendChild(makeButton('\u2795 📚', 'Inserir Bibliografia', () => { console.debug('Botão Bibliografia Clicado!'); window.dispatchEvent(new CustomEvent('toolbar:insert', { detail: { type: 'bibliography' } })); }));

  return toolbar;
}

// keyboard shortcuts for formatting (delegated)
window.addEventListener('keydown', (e)=>{
  if((e.ctrlKey||e.metaKey) && e.key.toLowerCase()==='b'){ e.preventDefault(); window.dispatchEvent(new CustomEvent('toolbar:format', { detail: { cmd: 'bold' } })); }
  if((e.ctrlKey||e.metaKey) && e.key.toLowerCase()==='i'){ e.preventDefault(); window.dispatchEvent(new CustomEvent('toolbar:format', { detail: { cmd: 'italic' } })); }
  // Delete key: delete current block if cursor is at start/end and block is empty or has minimal content
  if(e.key === 'Delete' && (e.ctrlKey || e.metaKey)){ e.preventDefault(); window.dispatchEvent(new CustomEvent('toolbar:delete')); }
});
