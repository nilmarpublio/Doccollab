// DocCollab-v0
// AST é a única fonte de verdade.
// Nenhuma lógica fora do modelo semântico é permitida.

// editor-controller.js — controlador do editor de blocos (núcleo)
// PROMPT COPILOT
// Implemente o controlador central do editor de blocos.
// Ele coordena interações do usuário, atualização do AST e renderização.
// Toda ação do usuário deve resultar em uma alteração explícita do AST.
// Nunca permitir edição fora de blocos semânticos.
// Sempre atualizar o timestamp updatedAt.
// Não incluir lógica de exportação ou compilação.

import { renderBlock } from './block-renderer.js';
import { createBlock } from './block-factory.js';
import { validateAST } from '../core/validator.js';
import { allowedChildTypes, canCreate } from './block-rules.js';
import { createToolbar } from './toolbar.js';

let _rootEl = null;
let _ast = null;
let _blockEditHandler = null;
let _toolbarInsertHandler = null;
let _toolbarFormatHandler = null;
let _toolbarDeleteHandler = null;
let _toolbarMoveHandler = null;

function _nowISO() {
  return new Date().toISOString();
}

function findBlockById(id, nodes = null) {
  nodes = nodes || (_ast && (_ast.blocks || _ast.content) ) || [];
  for (const n of nodes) {
    if (n.id === id) return n;
    const children = n.content || n.children || n.blocks || [];
    const found = findBlockById(id, children);
    if (found) return found;
  }
  return null;
}

function findParentOf(id, nodes = null, parent = null) {
  nodes = nodes || (_ast && (_ast.blocks || _ast.content)) || [];
  for (const n of nodes) {
    if (n.id === id) return parent;
    const children = n.content || n.children || n.blocks || [];
    const found = findParentOf(id, children, n);
    if (found) return found;
  }
  return null;
}

function removeBlockById(id, nodes = null) {
  nodes = nodes || (_ast && (_ast.blocks || _ast.content)) || [];
  for (let i = 0; i < nodes.length; i++) {
    const n = nodes[i];
    if (n.id === id) {
      nodes.splice(i, 1);
      return true;
    }
    const children = n.content || n.children || n.blocks || [];
    if (removeBlockById(id, children)) return true;
  }
  return false;
}

function renderAll() {
  console.debug('renderAll called, _rootEl:', _rootEl, '_ast:', _ast);
  if (!_rootEl || !_ast) {
    console.warn('renderAll: missing _rootEl or _ast');
    return;
  }
  _rootEl.innerHTML = '';
  const children = _ast.blocks || _ast.content || [];
  console.debug('renderAll: rendering', children.length, 'blocks');
  for (const b of children) {
    const el = renderBlock(b);
    el.dataset.blockId = b.id;
    _rootEl.appendChild(el);
  }
  console.debug('renderAll: done, _rootEl.children.length:', _rootEl.children.length);
}

function _emitChange() {
  try {
    window.dispatchEvent(new CustomEvent('ast:changed', { detail: { ast: _ast } }));
  } catch (e) { /* ignore */ }
}

/**
 * Inicializa o editor no elemento `rootEl` com o AST fornecido.
 * O controlador NÃO altera o AST diretamente fora das APIs públicas.
 */
export function mountEditor(rootEl, ast) {
  console.debug('mountEditor called with rootEl:', rootEl, 'ast:', ast);
  // Clean up before remounting
  if (_rootEl) {
    console.debug('Cleaning up previous mount');
    _rootEl.innerHTML = '';
  }
  
  _rootEl = rootEl;
  console.debug('setAST will be called...');
  setAST(ast || { metadata: {}, blocks: [] });
  console.debug('setAST completed, mounting event listeners...');
  
  // attach global listener to handle inline edits emitted by renderers
  try{
    if(_blockEditHandler) window.removeEventListener('block:edited', _blockEditHandler);
    _blockEditHandler = (ev) => {
      const d = ev && ev.detail;
      if(!d || !d.id) return;
      const patch = {};
      if(d.field) patch[d.field] = d.value;
      try{ updateBlock(d.id, patch); }catch(e){ /* swallow */ }
    };
    window.addEventListener('block:edited', _blockEditHandler);
  }catch(e){}
  // mount formatting toolbar inside the editor container (vertical at left)
  // formatting toolbar is mounted by the application shell (outside this controller)
  // handle toolbar insert commands
  try{
    if(_toolbarInsertHandler) window.removeEventListener('toolbar:insert', _toolbarInsertHandler);
    _toolbarInsertHandler = (ev) => {
      const t = ev && ev.detail && ev.detail.type;
      if(!t) return;
      if(t === 'bibliography') console.debug('Handler recebeu bibliography! Vai tentar criar no root.');
      // determine parent and insertion point: nearest block to selection
      let parentId = null;
      let afterBlockId = null;
      if(t === 'bibliography') console.debug('Iniciando detecção de parentId/afterBlockId...');
      try{
        const sel = window.getSelection();
        if(sel && sel.rangeCount){
          const node = sel.anchorNode && (sel.anchorNode.nodeType===3 ? sel.anchorNode.parentElement : sel.anchorNode);
          const blockEl = node && node.closest && node.closest('.block');
          if(blockEl) {
            const currentBlockId = blockEl.dataset.blockId || null;
            const currentBlock = currentBlockId ? findBlockById(currentBlockId) : null;
            console.debug('toolbar:insert', t, 'current block:', currentBlockId, currentBlock?.type);
            
            // For section-level blocks, insert as sibling at root level after current top-level block
            if (t === 'section' || t === 'bibliography') {
              parentId = null;
              // Find the top-level block (section or root-level block)
              let topBlock = currentBlock;
              let topBlockParent = currentBlockId ? findParentOf(currentBlockId) : null;
              while (topBlockParent && topBlockParent.type !== 'document' && topBlockParent.id) {
                topBlock = topBlockParent;
                topBlockParent = findParentOf(topBlock.id);
              }
              afterBlockId = topBlock ? topBlock.id : currentBlockId;
              console.debug('Inserting section after top-level block:', afterBlockId);
              if(t === 'bibliography') console.debug('Detectou que é section/bibliography, afterBlockId: ' + afterBlockId);
            } else {
              // For content blocks, try to insert inside current block if it's a container
              if (currentBlock && (currentBlock.type === 'section' || currentBlock.type === 'subsection')) {
                parentId = currentBlockId;
                afterBlockId = null; // append at end of section
                console.debug('Inserting', t, 'inside', currentBlock.type, parentId);
              } else {
                // insert as sibling after current block
                const parent = currentBlockId ? findParentOf(currentBlockId) : null;
                parentId = parent ? parent.id : null;
                afterBlockId = currentBlockId;
                console.debug('Inserting', t, 'as sibling after', afterBlockId, 'parent:', parentId);
              }
            }
          }
        }
      }catch(e){ console.error('toolbar:insert parentId detection error', e); if(t === 'bibliography') console.error('ERRO no try-catch:', e); }
      // create sensible defaults for props per type
      const defaults = { paragraph: { text: '' }, section: { title: 'Nova Seção' }, subsection: { title: 'Nova Subseção' }, equation: { latex: '' }, figure: { src: '', caption: '' }, table: { caption: '', rows: [[{text:'Cabeçalho 1'},{text:'Cabeçalho 2'}],[{text:''},{text:''}],[{text:''},{text:''}]] }, pagebreak: {}, citation: { text: '' }, bibliography: { entries: [] } };
      const props = defaults[t] || {};
      if(t === 'bibliography') console.debug('Antes de createBlockAt - parentId: ' + parentId + ', afterBlockId: ' + afterBlockId + ', props: ' + JSON.stringify(props));
      console.debug('Type:', t, 'Props:', props);
      console.debug('Calling createBlockAt with parentId:', parentId, 'afterBlockId:', afterBlockId);
      const res = createBlockAt(t, props, parentId, afterBlockId);
      console.log('=== createBlockAt retornou:', res);
      if(t === 'bibliography') console.debug('createBlockAt para bibliography retornou: ' + (res && res.ok ? 'OK - id:' + res.block.id : 'FALHOU - ' + (res ? res.error : 'null')));
      if(res && res.ok && res.block){
        console.log('=== Bloco criado com sucesso, ID:', res.block.id);
        // focus new block in DOM
        setTimeout(()=>{
          const el = document.querySelector(`[data-block-id="${res.block.id}"]`);
          if(el){
            const editable = el.querySelector('p,div,h1,h2,h3,pre,li');
            if(editable){ editable.focus();
              // place caret at end
              const range = document.createRange(); range.selectNodeContents(editable); range.collapse(false);
              const sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(range);
            }
          }
        },50);
        // show undo notification for this insertion
        try{
          showInsertNotification(res.block.id, 'Bloco inserido — desfazer?');
        }catch(e){}
      }
    };
    window.addEventListener('toolbar:insert', _toolbarInsertHandler);
  }catch(e){}
  // handle keyboard-dispatched format commands (from toolbar key shortcuts)
  try{
    if(_toolbarFormatHandler) window.removeEventListener('toolbar:format', _toolbarFormatHandler);
    _toolbarFormatHandler = (ev)=>{
      const cmd = ev && ev.detail && ev.detail.cmd;
      if(!cmd) return;
      // map commands to tags
      const tagMap = { bold: 'strong', italic: 'em', code: 'code' };
      const tag = tagMap[cmd] || null;
      if(!tag) return;
      try{
        const sel = window.getSelection();
        if (!sel || sel.rangeCount === 0) return;
        const range = sel.getRangeAt(0);
        if (!range || range.collapsed) return;
        const wrapper = document.createElement(tag);
        wrapper.appendChild(range.extractContents());
        range.insertNode(wrapper);
        range.setStartAfter(wrapper);
        range.collapse(true);
        sel.removeAllRanges(); sel.addRange(range);
        // find enclosing block element and emit block:edited
        const blockEl = wrapper.closest && wrapper.closest('.block');
        if(blockEl){
          const id = blockEl.dataset.blockId;
          const field = blockEl.querySelector('p,div,h1,h2,h3,pre') ? 'text' : 'text';
          window.dispatchEvent(new CustomEvent('block:edited', { detail: { id, field, value: blockEl.innerHTML } }));
        }
      }catch(e){ console.error('toolbar:format handler error', e); }
    };
    window.addEventListener('toolbar:format', _toolbarFormatHandler);
  }catch(e){}
  // handle delete block command
  try{
    if(_toolbarDeleteHandler) window.removeEventListener('toolbar:delete', _toolbarDeleteHandler);
    _toolbarDeleteHandler = (ev)=>{
      try{
        const sel = window.getSelection();
        if(!sel || !sel.rangeCount) return;
        const node = sel.anchorNode && (sel.anchorNode.nodeType===3 ? sel.anchorNode.parentElement : sel.anchorNode);
        const blockEl = node && node.closest && node.closest('.block');
        if(!blockEl) return;
        const blockId = blockEl.dataset.blockId;
        if(!blockId) return;
        // Confirm deletion
        if(!confirm('Apagar este bloco?')) return;
        const result = deleteBlock(blockId);
        if(result && result.ok){
          console.debug('Block deleted:', blockId);
        } else {
          console.error('Failed to delete block:', result);
          console.warn('Não foi possível apagar o bloco.');
        }
      }catch(e){ console.error('toolbar:delete handler error', e); }
    };
    window.addEventListener('toolbar:delete', _toolbarDeleteHandler);
  }catch(e){}
  // handle move up/down commands from toolbar
  try{
    if(_toolbarMoveHandler) window.removeEventListener('toolbar:move', _toolbarMoveHandler);
    _toolbarMoveHandler = (ev)=>{
      try{
        const dir = ev && ev.detail && ev.detail.dir;
        if(!dir) return;
        const sel = window.getSelection();
        if(!sel || !sel.rangeCount) return;
        const node = sel.anchorNode && (sel.anchorNode.nodeType===3 ? sel.anchorNode.parentElement : sel.anchorNode);
        const blockEl = node && node.closest && node.closest('.block');
        if(!blockEl) return;
        const blockId = blockEl.dataset.blockId;
        if(!blockId) return;
        const parent = findParentOf(blockId);
        const parentId = parent ? parent.id : null;
        const siblings = parent ? (parent.content = parent.content || []) : (_ast.blocks = _ast.blocks || []);
        const idx = siblings.findIndex(b => b.id === blockId);
        if(idx === -1) return;
        const newIndex = dir === 'up' ? idx - 1 : idx + 1;
        if(newIndex < 0 || newIndex >= siblings.length) return; // can't move
        const result = moveBlock(blockId, parentId, newIndex);
        if(!result || !result.ok) console.warn('moveBlock failed', result);
      }catch(e){ console.error('toolbar:move handler error', e); }
    };
    window.addEventListener('toolbar:move', _toolbarMoveHandler);
  }catch(e){}
}

/**
 * Substitui o AST atual. Atualiza timestamps e re-renderiza.
 */
export function setAST(ast) {
  console.debug('setAST called with:', ast);
  _ast = ast;
  if (!_ast.metadata) _ast.metadata = { id: `id-${Date.now()}` };
  if (!Array.isArray(_ast.blocks) && Array.isArray(_ast.content)) {
    _ast.blocks = _ast.content;
  }
  _ast.metadata.updatedAt = _nowISO();
  console.debug('setAST: calling renderAll...');
  renderAll();
  console.debug('setAST: renderAll done, emitting change...');
  _emitChange();
  console.debug('setAST: complete');
}

export function getAST() { return _ast; }

/**
 * Cria um bloco do tipo `type` como filho de `parentId` (ou no root
 * se parentId for null). Aplica regras declarativas via `block-rules`.
 * Retorna { ok, block, errors }.
 * Se afterBlockId for fornecido, insere após esse bloco (irmão).
 */
export function createBlockAt(type, props = {}, parentId = null, afterBlockId = null) {
  if(type === 'bibliography') console.debug('DENTRO de createBlockAt - type: ' + type + ', parentId: ' + parentId);
  if (!_ast) return { ok: false, error: 'NO_AST' };

  // Verifica se a criação é permitida pelo parentType
  const parent = parentId ? findBlockById(parentId) : null;
  const parentType = parent ? parent.type : null;
  if (!canCreate(type, parentType)) {
    return { ok: false, error: 'NOT_ALLOWED_BY_RULES', allowed: allowedChildTypes(parentType) };
  }

  const block = createBlock(type, props);
  
  // Determine target array and insertion index
  const targetArray = parent ? (parent.content = parent.content || []) : (_ast.blocks = _ast.blocks || []);
  
  let insertIndex = targetArray.length; // default: append at end
  
  // If afterBlockId is specified, find it and insert after
  if (afterBlockId) {
    const idx = targetArray.findIndex(b => b.id === afterBlockId);
    console.debug('createBlockAt: looking for afterBlockId', afterBlockId, 'in array of', targetArray.length, 'items, found at index:', idx);
    if (idx !== -1) insertIndex = idx + 1;
  }
  
  console.debug('createBlockAt: inserting', type, 'at index', insertIndex, 'of', targetArray.length);
  targetArray.splice(insertIndex, 0, block);

  _ast.metadata.updatedAt = _nowISO();

  const validation = validateAST(_ast);
  if (validation.errors && validation.errors.length) {
    // rollback
    removeBlockById(block.id);
    _ast.metadata.updatedAt = _nowISO();
    return { ok: false, errors: validation.errors };
  }

  renderAll();
  _emitChange();
  // sanity-check: ensure newly created block is present in DOM
  try {
    const sel = document.querySelector(`[data-block-id="${block.id}"]`);
    if (!sel) {
      // gather context for debugging
      const rootCount = (_ast && (_ast.blocks || _ast.content) || []).length;
      console.warn('AVISO: bloco criado, mas NÃO encontrado no DOM.', { type, blockId: block.id, rootChildrenCount: rootCount, parentId, afterBlockId });
      console.debug('Debug info: created block present in AST but not in DOM', { type, blockId: block.id, rootCount, parentId, afterBlockId });
    }
  } catch (e) { console.error('createBlockAt dom-check error', e); }
  return { ok: true, block };
}

/**
 * Atualiza propriedades de um bloco (conteúdo, metadados). Sempre atualiza
 * `metadata.updatedAt` e valida o AST.
 */
export function updateBlock(blockId, patch = {}) {
  const block = findBlockById(blockId);
  if (!block) return { ok: false, error: 'BLOCK_NOT_FOUND' };

  // Não permitir edição fora de blocos semânticos: apenas atualizar
  // campos permitidos (tipo e id são imutáveis aqui).
  const allowedKeys = Object.keys(block).filter(k => !['id','type'].includes(k));
  for (const key of Object.keys(patch)) {
    if (!allowedKeys.includes(key) && !(key in block)) continue;
    block[key] = patch[key];
  }

  _ast.metadata.updatedAt = _nowISO();
  const validation = validateAST(_ast);
  if (validation.errors && validation.errors.length) {
    return { ok: false, errors: validation.errors };
  }

  // Don't re-render during inline edits — DOM is already updated by contentEditable
  // Only emit change event to trigger autosave
  _emitChange();
  return { ok: true, block };
}

export function deleteBlock(blockId) {
  const ok = removeBlockById(blockId);
  if (!ok) return { ok: false, error: 'BLOCK_NOT_FOUND' };
  _ast.metadata.updatedAt = _nowISO();
  const validation = validateAST(_ast);
  if (validation.errors && validation.errors.length) {
    return { ok: false, errors: validation.errors };
  }
  renderAll();
  _emitChange();
  return { ok: true };
}

/**
 * Move um bloco para outro pai (ou root). Mantém integridade da árvore.
 */
export function moveBlock(blockId, newParentId = null, index = null) {
  const block = findBlockById(blockId);
  if (!block) return { ok: false, error: 'BLOCK_NOT_FOUND' };
  const oldParent = findParentOf(blockId);
  // remove from old parent
  const removed = removeBlockById(blockId);
  if (!removed) return { ok: false, error: 'REMOVE_FAILED' };

  const newParent = newParentId ? findBlockById(newParentId) : null;
  const parentType = newParent ? newParent.type : null;
  if (!canCreate(block.type, parentType)) {
    // rollback: reinsert into old parent
    if (oldParent) {
      oldParent.content = oldParent.content || [];
      oldParent.content.push(block);
    } else {
      _ast.blocks = _ast.blocks || [];
      _ast.blocks.push(block);
    }
    return { ok: false, error: 'NOT_ALLOWED_BY_RULES' };
  }

  if (newParent) {
    newParent.content = newParent.content || [];
    if (typeof index === 'number') newParent.content.splice(index, 0, block);
    else newParent.content.push(block);
  } else {
    _ast.blocks = _ast.blocks || [];
    if (typeof index === 'number') _ast.blocks.splice(index, 0, block);
    else _ast.blocks.push(block);
  }

  _ast.metadata.updatedAt = _nowISO();
  const validation = validateAST(_ast);
  if (validation.errors && validation.errors.length) {
    return { ok: false, errors: validation.errors };
  }

  renderAll();
  _emitChange();
  return { ok: true };
}

export function replaceAST(newAst) {
  setAST(newAst);
}

// Simple insertion-notification UI with undo
function showInsertNotification(blockId, message) {
  const container = document.createElement('div');
  container.className = 'insert-notification';
  container.style.cssText = 'position:fixed;bottom:16px;left:16px;padding:10px 12px;background:#222;color:#fff;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,0.2);z-index:9999;display:flex;gap:8px;align-items:center;';
  const msg = document.createElement('span'); msg.textContent = message || 'Inserido';
  const undo = document.createElement('button'); undo.textContent = 'Desfazer'; undo.style.cssText = 'background:#fff;color:#000;border:none;padding:6px 8px;border-radius:4px;cursor:pointer;';
  container.appendChild(msg); container.appendChild(undo);
  document.body.appendChild(container);
  const cleanup = () => { try{ container.remove(); }catch(e){} };
  const tid = setTimeout(()=> cleanup(), 6000);
  undo.addEventListener('click', ()=>{
    clearTimeout(tid);
    // call deleteBlock to remove created block
    try{ deleteBlock(blockId); }catch(e){}
    cleanup();
  });
}
