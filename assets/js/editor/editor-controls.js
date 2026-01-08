// editor-controls.js — preview-like controls mounted at top of editor
const API_BASE = (typeof window !== 'undefined' && window.location && window.location.origin) ? window.location.origin : 'http://localhost:3000';

import { t } from '../i18n.js';
import { highlightErrors, clearHighlights } from './error-highlighter.js';

function el(tn, attrs = {}, ...children) {
  const e = document.createElement(tn);
  Object.entries(attrs).forEach(([k,v])=>{ if(k==='class') e.className = v; else if(k==='text') e.textContent = v; else e.setAttribute(k,v); });
  for(const c of children) if(c) e.appendChild(c);
  return e;
}

export function mountEditorControls(rootEl, getAST) {
  rootEl = rootEl || document.body;
  const container = el('div', { class: 'editor-controls' });

  const controls = el('div', { class: 'preview-controls' });
  const autoLabel = el('label', { class: 'inline' });
  const autoToggle = el('input', { type: 'checkbox' });
  autoLabel.appendChild(autoToggle);
  autoLabel.appendChild(document.createTextNode(' ' + t('preview.auto_label')));
  const updateBtn = el('button', { class: 'btn' }); updateBtn.textContent = t('preview.update_btn');
  const exportPdfBtn = el('button', { class: 'btn' }); exportPdfBtn.textContent = t('preview.export_pdf');
  const exportTexBtn = el('button', { class: 'btn' }); exportTexBtn.textContent = t('preview.export_tex');
  const exportBibBtn = el('button', { class: 'btn' }); exportBibBtn.textContent = t('preview.export_bib');
  const exportAstBtn = el('button', { class: 'btn' }); exportAstBtn.textContent = t('preview.export_ast');
  const clearHighlightsBtn = el('button', { class: 'btn' }); clearHighlightsBtn.textContent = t('preview.clear_highlights');

  controls.appendChild(autoLabel);
  controls.appendChild(updateBtn);
  controls.appendChild(exportPdfBtn);
  controls.appendChild(exportTexBtn);
  controls.appendChild(exportBibBtn);
  controls.appendChild(exportAstBtn);
  controls.appendChild(clearHighlightsBtn);

  const status = el('div', { class: 'preview-status' }); status.textContent = t('preview.status.ready');

  container.appendChild(controls);
  container.appendChild(status);
  // insert at top of editor
  rootEl.prepend(container);

  let running = false;

  async function fetchCompile(showErrors=true) {
    if (running) return;
    running = true;
    status.textContent = t('preview.status.generating');
    try {
      const ast = getAST();
      const body = JSON.stringify({ ast });
      const res = await fetch(API_BASE + '/api/compile', { method: 'POST', headers: { 'Content-Type':'application/json' }, body });
      const j = await res.json();
      if (j.success && j.pdfBase64) {
        status.textContent = t('preview.status.updated');
        // dispatch event so other components can react
        window.dispatchEvent(new CustomEvent('editor:compiled', { detail: { result: j } }));
      } else {
        status.textContent = t('preview.status.error') + ' ' + (j.error && j.error.message ? j.error.message : JSON.stringify(j));
        if (showErrors) {
          if (j.errors && Array.isArray(j.errors) && j.errors.length) {
            highlightErrors(j.errors);
          } else if (j.error && j.error.blockId) {
            highlightErrors(j.error);
          } else {
            clearHighlights();
          }
        }
      }
    } catch (e) {
      status.textContent = 'Falha: ' + e.message;
    }
    running = false;
  }

  function b64ToBlob(b64, mime) {
    const bin = atob(b64);
    const len = bin.length;
    const arr = new Uint8Array(len);
    for (let i = 0; i < len; i++) arr[i] = bin.charCodeAt(i);
    return new Blob([arr], { type: mime });
  }

  updateBtn.addEventListener('click', () => fetchCompile(true));
  exportPdfBtn.addEventListener('click', async () => {
    status.textContent = t('preview.status.exporting');
    try {
      const ast = getAST();
      const res = await fetch(API_BASE + '/api/compile', { method: 'POST', headers: { 'Content-Type':'application/json' }, body: JSON.stringify({ ast }) });
      const j = await res.json();
      if (j.success && j.pdfBase64) {
        const blob = b64ToBlob(j.pdfBase64, 'application/pdf');
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'doccollab.pdf';
        a.click();
        status.textContent = t('preview.status.updated');
      } else {
        status.textContent = 'Erro: ' + (j.error && j.error.message ? j.error.message : JSON.stringify(j));
      }
    } catch (e) { status.textContent = 'Falha: ' + e.message; }
  });

  exportTexBtn.addEventListener('click', async () => {
    status.textContent = t('preview.status.generating');
    try {
      const ast = getAST();
      const res = await fetch(API_BASE + '/api/render-tex', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ ast }) });
      const j = await res.json();
      if (j.success && j.tex) {
        const blob = new Blob([j.tex], { type: 'text/x-tex' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'document.tex';
        a.click();
        status.textContent = t('preview.status.updated');
      } else status.textContent = 'Erro: ' + JSON.stringify(j);
    } catch(e){ status.textContent = 'Falha: ' + e.message; }
  });

  exportBibBtn.addEventListener('click', async () => {
    status.textContent = t('preview.status.generating');
    try {
      const ast = getAST();
      const res = await fetch(API_BASE + '/api/render-bib', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({ ast }) });
      const j = await res.json();
      if (j.success && j.bib) {
        const blob = new Blob([j.bib], { type: 'text/plain' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'references.bib';
        a.click();
        status.textContent = t('preview.status.updated');
      } else status.textContent = 'Erro: ' + JSON.stringify(j);
    } catch(e){ status.textContent = 'Falha: ' + e.message; }
  });

  exportAstBtn.addEventListener('click', () => {
    status.textContent = 'Exportando AST...';
    try {
      const ast = getAST();
      const blob = new Blob([JSON.stringify(ast, null, 2)], { type: 'application/json' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'doccollab-ast.json';
      a.click();
      status.textContent = 'AST exportado.';
    } catch(e){ status.textContent = 'Falha: ' + e.message; }
  });

  clearHighlightsBtn.addEventListener('click', () => {
    try{ clearHighlights(); status.textContent = t('preview.status.ready'); } catch(e){ console.warn('clear highlights failed', e); }
  });

  // auto refresh on AST changes
  window.addEventListener('ast:changed', (ev) => {
    if (autoToggle.checked) {
      // simple debounce
      const last = JSON.stringify(ev.detail.ast);
      setTimeout(()=>{
        const cur = JSON.stringify(getAST());
        if (cur === last) fetchCompile(false);
      }, 350);
    }
  });

  return { fetchCompile };
}
