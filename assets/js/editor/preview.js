// DocCollab-v0
// AST é a única fonte de verdade.
// Nenhuma lógica fora do modelo semântico é permitida.

// preview.js — preview and export controls for editor

const API_BASE = (typeof window !== 'undefined' && window.location && window.location.origin) ? window.location.origin : 'http://localhost:3000';

function el(t, attrs = {}, ...children) {
  const e = document.createElement(t);
  Object.entries(attrs).forEach(([k,v])=>{ if(k==='class') e.className = v; else if(k==='text') e.textContent = v; else e.setAttribute(k,v); });
  for(const c of children) if(c) e.appendChild(c);
  return e;
}

import { t } from '../i18n.js';
import { highlightErrors, clearHighlights } from './error-highlighter.js';

export function mountPreview(rootEl, getAST) {
  rootEl = rootEl || document.body;
  const container = el('div', { class: 'preview-panel' });

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
  const viewLogBtn = el('button', { class: 'btn' }); viewLogBtn.textContent = t('preview.view_log') || 'Mostrar log';

  controls.appendChild(autoLabel);
  controls.appendChild(updateBtn);
  controls.appendChild(exportPdfBtn);
  controls.appendChild(exportTexBtn);
  controls.appendChild(exportBibBtn);
  controls.appendChild(exportAstBtn);
  controls.appendChild(clearHighlightsBtn);
  controls.appendChild(viewLogBtn);

  const iframe = el('iframe', { class: 'preview-iframe', style: 'width:100%;height:600px;border:1px solid #ddd' });
  const status = el('div', { class: 'preview-status' }); status.textContent = t('preview.status.ready');

  container.appendChild(controls);
  container.appendChild(status);
  container.appendChild(iframe);
  rootEl.appendChild(container);

  let lastAstJson = null;
  let running = false;
  let lastLog = null;

  async function fetchCompile(showErrors=true) {
    if (running) return;
    running = true;
    status.textContent = t('preview.status.generating');
    try {
      const ast = getAST();
      const body = JSON.stringify({ ast });
      try{ console.log('preview: sending AST to /api/compile', JSON.parse(body)); }catch(e){}
      const res = await fetch(API_BASE + '/api/compile', { method: 'POST', headers: { 'Content-Type':'application/json' }, body });
      const j = await res.json();
      if (j.success && j.pdfBase64) {
        const blob = b64ToBlob(j.pdfBase64, 'application/pdf');
        const url = URL.createObjectURL(blob);
        iframe.src = url;
        status.textContent = t('preview.status.updated');
        // Clear any previous error highlights on successful compile
        clearHighlights();
        lastLog = null;
      } else {
        status.textContent = t('preview.status.error') + ' ' + (j.error && j.error.message ? j.error.message : JSON.stringify(j));
        // capture server log for debugging and expose to view button
        lastLog = j.log || j.logText || null;
        if (lastLog) console.error('compile log:\n', lastLog);
        if (showErrors) {
          // server may return either `error` single or `errors` array
          if (j.errors && Array.isArray(j.errors) && j.errors.length) {
            highlightErrors(j.errors);
          } else if (j.error && j.error.blockId) {
            highlightErrors(j.error);
          } else {
            // clear any previous highlights if no block-level info
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
      const payload = { ast };
      try{ console.log('preview: exporting TEX, AST payload=', payload); }catch(e){}
      const res = await fetch(API_BASE + '/api/render-tex', { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) });
      const j = await res.json();
      try{ console.log('preview: render-tex response', j && (j.tex ? ('tex length ' + j.tex.length) : j)); }catch(e){}
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

  viewLogBtn.addEventListener('click', () => {
    try{
      if(!lastLog) { status.textContent = 'Nenhum log disponível'; return; }
      const blob = new Blob([lastLog], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      window.open(url, '_blank');
    } catch(e){ console.warn('open log failed', e); status.textContent = 'Falha ao abrir log'; }
  });

  // auto refresh on AST changes
  window.addEventListener('ast:changed', (ev) => {
    if (autoToggle.checked) {
      // simple debounce
      lastAstJson = JSON.stringify(ev.detail.ast);
      setTimeout(()=>{
        const cur = JSON.stringify(getAST());
        if (cur === lastAstJson) fetchCompile(false);
      }, 350);
    }
  });

  return { fetchCompile };
}
