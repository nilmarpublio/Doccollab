// DocCollab-v0 - VERSÃO COM CITATION RENDERER - 2026-01-02-001
// AST é a única fonte de verdade.
// Nenhuma lógica fora do modelo semântico é permitida.
// block-renderer.js — mapeia blocos do AST para DOM editável
export function renderBlock(block){
  const wrapper = document.createElement('div');
  wrapper.className = 'block';
  wrapper.dataset.blockId = block.id;

  function emitChange(detail){
    try { window.dispatchEvent(new CustomEvent('block:edited', { detail })); } catch(e){}
  }

  // renderers per type
  switch(block.type){
    case 'title': {
      const h = document.createElement('h1');
      h.contentEditable = 'true';
      h.innerHTML = block.text || block.title || '';
      h.addEventListener('input', ()=> emitChange({ id: block.id, field: 'text', value: h.innerHTML }));
      wrapper.appendChild(h);
      return wrapper;
    }
    case 'author': {
      const p = document.createElement('p'); p.className='author'; p.contentEditable='true'; p.innerHTML = block.text || block.name || '';
      p.addEventListener('input', ()=> emitChange({ id: block.id, field: 'text', value: p.innerHTML }));
      wrapper.appendChild(p); return wrapper;
    }
    case 'abstract': {
      const div = document.createElement('div'); div.className='abstract'; div.contentEditable='true'; div.innerHTML = block.text || '';
      div.addEventListener('input', ()=> emitChange({ id: block.id, field: 'text', value: div.innerHTML }));
      wrapper.appendChild(div); return wrapper;
    }
    case 'section': {
      const h = document.createElement('h2'); h.contentEditable='true'; h.innerHTML = block.title || '';
      h.addEventListener('input', ()=> emitChange({ id: block.id, field: 'title', value: h.innerHTML }));
      wrapper.appendChild(h);
      const container = document.createElement('div'); container.className='section-children';
      const children = block.content || [];
      for(const c of children){ container.appendChild(renderBlock(c)); }
      wrapper.appendChild(container);
      return wrapper;
    }
    case 'subsection': {
      const h = document.createElement('h3'); h.contentEditable='true'; h.innerHTML = block.title || '';
      h.addEventListener('input', ()=> emitChange({ id: block.id, field: 'title', value: h.innerHTML }));
      wrapper.appendChild(h);
      const container = document.createElement('div'); container.className='subsection-children';
      const children = block.content || [];
      for(const c of children){ container.appendChild(renderBlock(c)); }
      wrapper.appendChild(container);
      return wrapper;
    }
    case 'paragraph': {
      const p = document.createElement('p'); p.contentEditable='true'; p.innerHTML = block.text || '';
      p.addEventListener('input', ()=> emitChange({ id: block.id, field: 'text', value: p.innerHTML }));
      wrapper.appendChild(p); return wrapper;
    }
    case 'equation': {
      const eqDiv = document.createElement('div'); eqDiv.className='equation-block';
      
      // Barra de ferramentas matemáticas
      const mathToolbar = document.createElement('div'); 
      mathToolbar.style.cssText='display:flex;gap:4px;margin-bottom:8px;flex-wrap:wrap;background:#f5f5f5;padding:8px;border-radius:4px;';
      
      const symbols = [
        { label: '∫', code: '\\int ' },
        { label: '∫ᵇₐ', code: '\\int_{a}^{b} ' },
        { label: '∬', code: '\\iint ' },
        { label: '∭', code: '\\iiint ' },
        { label: '∑', code: '\\sum ' },
        { label: '∑ⁿᵢ', code: '\\sum_{i=1}^{n} ' },
        { label: '∏', code: '\\prod ' },
        { label: '√', code: '\\sqrt{} ', cursorBack: 2 },
        { label: 'ⁿ√', code: '\\sqrt[n]{} ', cursorBack: 2 },
        { label: 'x²', code: '^{} ', cursorBack: 2 },
        { label: 'xᵢ', code: '_{} ', cursorBack: 2 },
        { label: 'x/y', code: '\\frac{}{} ', cursorBack: 2 },
        { label: 'lim', code: '\\lim_{x \\to } ', cursorBack: 2 },
        { label: '∞', code: '\\infty ' },
        { label: '≤', code: '\\leq ' },
        { label: '≥', code: '\\geq ' },
        { label: '≠', code: '\\neq ' },
        { label: '≈', code: '\\approx ' },
        { label: 'α', code: '\\alpha ' },
        { label: 'β', code: '\\beta ' },
        { label: 'γ', code: '\\gamma ' },
        { label: 'δ', code: '\\delta ' },
        { label: 'θ', code: '\\theta ' },
        { label: 'λ', code: '\\lambda ' },
        { label: 'μ', code: '\\mu ' },
        { label: 'π', code: '\\pi ' },
        { label: 'σ', code: '\\sigma ' },
        { label: 'Σ', code: '\\Sigma ' },
        { label: 'Δ', code: '\\Delta ' },
        { label: 'Ω', code: '\\omega ' }
      ];
      
      const pre = document.createElement('pre'); 
      pre.className='equation'; 
      pre.contentEditable='true'; 
      pre.textContent = block.latex || block.text || '';
      pre.style.cssText='border:1px solid #ccc;padding:12px;border-radius:4px;font-family:monospace;min-height:60px;';
      
      symbols.forEach(sym => {
        const btn = document.createElement('button');
        btn.textContent = sym.label;
        btn.title = sym.code.trim();
        btn.style.cssText='padding:4px 8px;border:1px solid #ccc;background:white;border-radius:3px;cursor:pointer;font-size:0.95em;';
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          pre.focus();
          const sel = window.getSelection();
          if (sel.rangeCount > 0) {
            const range = sel.getRangeAt(0);
            const textNode = document.createTextNode(sym.code);
            range.insertNode(textNode);
            range.setStartAfter(textNode);
            if (sym.cursorBack) {
              range.setStart(textNode, textNode.textContent.length - sym.cursorBack);
            }
            range.collapse(true);
            sel.removeAllRanges();
            sel.addRange(range);
          } else {
            pre.textContent += sym.code;
          }
          emitChange({ id: block.id, field: 'latex', value: pre.textContent });
        });
        mathToolbar.appendChild(btn);
      });
      
      pre.addEventListener('input', ()=> emitChange({ id: block.id, field: 'latex', value: pre.textContent }));
      eqDiv.appendChild(mathToolbar);
      eqDiv.appendChild(pre);
      wrapper.appendChild(eqDiv); 
      return wrapper;
    }
    case 'figure': {
      const fig = document.createElement('div'); fig.className='figure';
      // Campo editável para o caminho da imagem
      const srcLabel = document.createElement('div'); srcLabel.className='figure-src-label'; srcLabel.textContent='Caminho da imagem:'; srcLabel.style.cssText='font-size:0.9em;color:#666;margin-bottom:4px;';
      const srcInput = document.createElement('div'); srcInput.contentEditable='true'; srcInput.className='figure-src'; srcInput.textContent = block.src || '';
      srcInput.style.cssText='border:1px solid #ccc;padding:6px;border-radius:4px;margin-bottom:8px;font-family:monospace;font-size:0.9em;';
      // Imagem (preview) - DECLARAR ANTES do event listener
      const img = document.createElement('img'); img.src = block.src || ''; img.alt = block.caption || '';
      img.style.cssText='max-width:100%;height:auto;margin:8px 0;border:1px solid #ddd;';
      srcInput.addEventListener('input', ()=> {
        emitChange({ id: block.id, field: 'src', value: srcInput.textContent });
        // Atualizar preview da imagem
        if(img) img.src = srcInput.textContent;
      });
      // Campo editável para legenda
      const captionLabel = document.createElement('div'); captionLabel.className='figure-caption-label'; captionLabel.textContent='Legenda:'; captionLabel.style.cssText='font-size:0.9em;color:#666;margin-top:8px;margin-bottom:4px;';
      const caption = document.createElement('div'); caption.contentEditable='true'; caption.className='figure-caption'; caption.innerHTML = block.caption || '';
      caption.style.cssText='border:1px solid #ccc;padding:6px;border-radius:4px;';
      caption.addEventListener('input', ()=> emitChange({ id: block.id, field: 'caption', value: caption.innerHTML }));
      fig.appendChild(srcLabel); fig.appendChild(srcInput); fig.appendChild(img); fig.appendChild(captionLabel); fig.appendChild(caption); wrapper.appendChild(fig); return wrapper;
    }
    case 'pagebreak': {
      const hr = document.createElement('hr'); hr.className='pagebreak'; hr.style.cssText='border:none;border-top:2px dashed #999;margin:2em 0;';
      const label = document.createElement('div'); label.className='pagebreak-label'; label.textContent='— Quebra de Página —'; label.style.cssText='text-align:center;color:#999;font-size:0.9em;margin:-1.2em 0 1em;';
      wrapper.appendChild(hr); wrapper.appendChild(label); return wrapper;
    }
    case 'table': {
      const tableDiv = document.createElement('div'); tableDiv.className='table-block';
      const captionLabel = document.createElement('div'); captionLabel.textContent='Legenda da tabela:'; captionLabel.style.cssText='font-size:0.9em;color:#666;margin-bottom:4px;';
      const caption = document.createElement('div'); caption.contentEditable='true'; caption.className='table-caption'; caption.innerHTML = block.caption || '';
      caption.style.cssText='border:1px solid #ccc;padding:6px;border-radius:4px;margin-bottom:8px;';
      caption.addEventListener('input', ()=> emitChange({ id: block.id, field: 'caption', value: caption.innerHTML }));
      
      // Botões de controle
      const controls = document.createElement('div'); controls.style.cssText='margin-bottom:8px;display:flex;gap:8px;';
      const addRowBtn = document.createElement('button'); addRowBtn.textContent='+ Linha'; addRowBtn.style.cssText='padding:4px 8px;font-size:0.9em;cursor:pointer;';
      const removeRowBtn = document.createElement('button'); removeRowBtn.textContent='- Linha'; removeRowBtn.style.cssText='padding:4px 8px;font-size:0.9em;cursor:pointer;';
      const addColBtn = document.createElement('button'); addColBtn.textContent='+ Coluna'; addColBtn.style.cssText='padding:4px 8px;font-size:0.9em;cursor:pointer;';
      const removeColBtn = document.createElement('button'); removeColBtn.textContent='- Coluna'; removeColBtn.style.cssText='padding:4px 8px;font-size:0.9em;cursor:pointer;';
      
      const table = document.createElement('table'); table.style.cssText='width:100%;border-collapse:collapse;margin:8px 0;';
      const rows = block.rows || [[{text:''},{text:''}],[{text:''},{text:''}]];
      
      const renderTable = () => {
        table.innerHTML = '';
        rows.forEach((row, rIdx) => {
          const tr = document.createElement('tr');
          row.forEach((cell, cIdx) => {
            const td = document.createElement(rIdx===0?'th':'td'); td.contentEditable='true'; td.innerHTML = cell.text || '';
            td.style.cssText='border:1px solid #ccc;padding:8px;'+(rIdx===0?'background:#f0f0f0;font-weight:bold;':'');
            td.addEventListener('input', ()=> {
              rows[rIdx][cIdx] = { text: td.innerHTML };
              emitChange({ id: block.id, field: 'rows', value: rows });
            });
            tr.appendChild(td);
          });
          table.appendChild(tr);
        });
      };
      
      addRowBtn.addEventListener('click', (e)=> { e.preventDefault(); const numCols = rows[0]?.length || 2; rows.push(Array(numCols).fill(null).map(()=>({text:''}))); emitChange({ id: block.id, field: 'rows', value: rows }); renderTable(); });
      removeRowBtn.addEventListener('click', (e)=> { e.preventDefault(); if(rows.length>1) { rows.pop(); emitChange({ id: block.id, field: 'rows', value: rows }); renderTable(); } });
      addColBtn.addEventListener('click', (e)=> { e.preventDefault(); rows.forEach(row => row.push({text:''})); emitChange({ id: block.id, field: 'rows', value: rows }); renderTable(); });
      removeColBtn.addEventListener('click', (e)=> { e.preventDefault(); if(rows[0]?.length>1) { rows.forEach(row => row.pop()); emitChange({ id: block.id, field: 'rows', value: rows }); renderTable(); } });
      
      renderTable();
      controls.appendChild(addRowBtn); controls.appendChild(removeRowBtn); controls.appendChild(addColBtn); controls.appendChild(removeColBtn);
      tableDiv.appendChild(captionLabel); tableDiv.appendChild(caption); tableDiv.appendChild(controls); tableDiv.appendChild(table); wrapper.appendChild(tableDiv); return wrapper;
    }
    case 'citation': {
      const citationDiv = document.createElement('div'); citationDiv.className='citation-block';
      citationDiv.style.cssText='border-left:4px solid #ccc;padding:12px 16px;margin:16px 0;background:#f9f9f9;font-style:italic;';
      const text = document.createElement('div'); text.contentEditable='true'; text.innerHTML = block.text || '';
      text.addEventListener('input', ()=> emitChange({ id: block.id, field: 'text', value: text.innerHTML }));
      citationDiv.appendChild(text); wrapper.appendChild(citationDiv); return wrapper;
    }
    case 'bibliography': {
      const div = document.createElement('div'); div.className='bibliography';
      div.style.cssText = 'padding:8px;border:1px dashed #ddd;border-radius:6px;background:#fafafa;';

      const controls = document.createElement('div'); controls.style.cssText = 'display:flex;gap:8px;align-items:center;margin-bottom:8px;';
      const addBtn = document.createElement('button'); addBtn.textContent = 'Adicionar entrada'; addBtn.style.cssText='padding:6px 10px;border-radius:4px;cursor:pointer;';
      controls.appendChild(addBtn);

      const list = document.createElement('ul'); list.style.cssText = 'padding-left:18px;margin:0;';
      let entries = Array.isArray(block.entries) ? (block.entries.map(e => ({ ...e }))) : [];

      function renderList(){
        list.innerHTML = '';
        if(entries.length === 0){
          const empty = document.createElement('div'); empty.style.cssText='color:#666;font-size:0.95em;margin-bottom:6px;'; empty.textContent = 'Nenhuma entrada. Clique em "Adicionar entrada" para começar.';
          list.appendChild(empty); return;
        }
        entries.forEach((e, idx) => {
          const li = document.createElement('li'); li.style.cssText='margin:6px 0;display:flex;gap:8px;align-items:flex-start;';
          const textDiv = document.createElement('div'); textDiv.contentEditable='true'; textDiv.innerHTML = e.text || e.title || '';
          textDiv.style.cssText='flex:1;border:1px solid #eee;padding:6px;border-radius:4px;min-height:24px;background:#fff;';
          textDiv.addEventListener('input', ()=>{
            entries[idx] = { ...(entries[idx]||{}), text: textDiv.innerHTML };
            emitChange({ id: block.id, field: 'entries', value: entries });
          });
          const removeBtn = document.createElement('button'); removeBtn.textContent = 'Remover'; removeBtn.style.cssText='padding:6px;border-radius:4px;cursor:pointer;';
          removeBtn.addEventListener('click', (ev)=>{ ev.preventDefault(); entries.splice(idx,1); emitChange({ id: block.id, field: 'entries', value: entries }); renderList(); });
          li.appendChild(textDiv); li.appendChild(removeBtn); list.appendChild(li);
        });
      }

      addBtn.addEventListener('click', (e)=>{ e.preventDefault(); const newEntry = { id: `bib_${Date.now()}_${Math.random().toString(36).slice(2,6)}`, text: '' }; entries.push(newEntry); emitChange({ id: block.id, field: 'entries', value: entries }); renderList(); });

      renderList();
      div.appendChild(controls); div.appendChild(list); wrapper.appendChild(div); return wrapper;
    }
    default: {
      const el = document.createElement('div'); el.textContent = block.type; wrapper.appendChild(el); return wrapper;
    }
  }
}
