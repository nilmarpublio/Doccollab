import { JSDOM } from 'jsdom';
import { highlightErrors, clearHighlights, scrollToBlock } from '../assets/js/editor/error-highlighter.js';

// monta um DOM mínimo e verifica que o highlighter aplica classes e realiza scroll
const dom = new JSDOM(`<!doctype html><html><head></head><body><div id="editor"></div></body></html>`);
global.window = dom.window;
global.document = dom.window.document;
global.HTMLElement = dom.window.HTMLElement;
global.Node = dom.window.Node;

function setupDOM(){
  const editor = document.getElementById('editor');
  ['b1','b2','b3'].forEach(id => {
    const d = document.createElement('div');
    d.className = 'block';
    d.setAttribute('data-block-id', id);
    d.textContent = `Block ${id}`;
    d.style.height = '40px';
    editor.appendChild(d);
  });
}

async function run(){
  try{
    setupDOM();
    clearHighlights();
    highlightErrors({ blockId: 'b2', message: 'Erro de teste' });
    const el = document.querySelector('[data-block-id="b2"]');
    if(!el){ console.error('FALHA: elemento não encontrado'); process.exit(2); }
    if(!el.classList.contains('doccollab-block-error')){ console.error('FALHA: classe de destaque não aplicada'); process.exit(3); }
    const sc = scrollToBlock('b2');
    if(!sc){ console.error('FALHA: scrollToBlock retornou falso'); process.exit(4); }
    console.log('OK: highlight e scroll funcionaram');
    process.exit(0);
  }catch(e){
    console.error('FALHA (exceção):', e);
    process.exit(1);
  }
}

run();
