// DocCollab-v0
// AST é a única fonte de verdade.
// Nenhuma lógica fora do modelo semântico é permitida.

// Validações do Editor por Blocos — JS puro
// Exporta `validateDocument(ast)` que retorna { errors: [], warnings: [] }

function isObject(v){return v!==null && typeof v==='object' && !Array.isArray(v)}

function traverseBlocks(blocks, cb, parent=null, path=[]){
  if(!Array.isArray(blocks)) return;
  for(let i=0;i<blocks.length;i++){
    const b = blocks[i];
    const p = path.concat(i);
    cb(b, parent, p);
    if(Array.isArray(b.content)) traverseBlocks(b.content, cb, b, p.concat('content'));
  }
}

function validateDocument(ast){
  const errors = [];
  const warnings = [];

  if(!isObject(ast)){
    errors.push({message:'AST inválido: documento deve ser um objeto', path:[]});
    return {errors,warnings};
  }

  const content = Array.isArray(ast.content)? ast.content : [];

  // regra: apenas 1 title
  let titles = [];
  traverseBlocks(content, (b,parent,path)=>{ if(b && b.type==='title') titles.push({b,parent,path}); });
  if(titles.length===0){
    warnings.push({message:'Documento não contém `title` (recomendado)', path:[]});
  } else if(titles.length>1){
    errors.push({message:`Documento contém ${titles.length} blocos 'title' (apenas 1 permitido)`, path: titles.map(t=>t.path)});
  }

  // regra: abstract antes da primeira section
  let firstSectionIndex = -1;
  let abstractIndex = -1;
  for(let i=0;i<content.length;i++){
    const t = content[i].type;
    if(firstSectionIndex===-1 && t==='section') firstSectionIndex = i;
    if(abstractIndex===-1 && t==='abstract') abstractIndex = i;
  }
  if(firstSectionIndex!==-1){
    if(abstractIndex===-1){
      warnings.push({message:'Documento não contém `abstract` antes da primeira seção', path:[]});
    } else if(abstractIndex>firstSectionIndex){
      errors.push({message:'`abstract` aparece depois da primeira `section` — deve ficar antes', path:['content',abstractIndex]});
    }
  }

  // coletar citações e bibliografia
  const citedKeys = new Set();
  traverseBlocks(content,(b,parent,path)=>{ if(b && b.type==='citation' && typeof b.key==='string') citedKeys.add(b.key); });
  const biblio = (ast.metadata && Array.isArray(ast.metadata.bibliography))? ast.metadata.bibliography : null;
  if(biblio){
    // referências não citadas
    const unused = biblio.filter(k=>!citedKeys.has(k));
    if(unused.length>0) warnings.push({message:`Entradas de bibliografia não citadas: ${unused.join(', ')}`, path:['metadata','bibliography']});
    // citações sem entrada
    const missing = Array.from(citedKeys).filter(k=>!biblio.includes(k));
    if(missing.length>0) errors.push({message:`Citações sem entrada na bibliografia: ${missing.join(', ')}`, path:['content']});
  } else if(citedKeys.size>0){
    errors.push({message:'Existem citações no documento mas sem `metadata.bibliography` definido', path:['metadata']});
  }

  // regras contextuais: subsection must have parent section; equation must be inside a section
  traverseBlocks(content,(b,parent,path)=>{
    if(!b || typeof b.type!=='string') return;
    if(b.type==='subsection'){
      if(!parent || parent.type!=='section'){
        errors.push({message:'`subsection` encontrado sem `section` pai', path});
      }
    }
    if(b.type==='equation'){
      // check ancestor chain for a section
      let foundSection=false;
      // parent is immediate; we cannot access grandparents here easily — instead, examine path
      // path contains indices and 'content' strings; we can check ancestors by scanning upward using path
      // But we don't have direct ancestor objects; easier: during traversal we passed parent argument, and parent may be subsection/section
      let anc = parent;
      while(anc){
        if(anc.type==='section'){ foundSection=true; break; }
        anc = anc.__parent || null;
      }
      if(!foundSection){
        errors.push({message:'`equation` fora de `section` (equações devem estar dentro de seções)', path});
      }
    }
    if(b.type==='figure' && b.label){
      // simple label uniqueness check could be deferred; we'll collect labels
    }
  });

  // label uniqueness check (figures/tables/equations)
  const labels = new Map();
  traverseBlocks(content,(b,parent,path)=>{
    if(b && typeof b.label==='string'){
      const l = b.label;
      if(labels.has(l)) labels.set(l, labels.get(l).concat([path])); else labels.set(l,[path]);
    }
  });
  for(const [l,arr] of labels.entries()){
    if(arr.length>1) errors.push({message:`Label duplicado '${l}' encontrado em múltiplos blocos`, paths:arr});
  }

  return {errors,warnings};
}

// Helper to attach parent pointers to blocks for ancestor checks (non-destructive clone)
function attachParents(ast){
  const root = Object.assign({}, ast);
  function recur(node, parent){
    if(isObject(node)){
      node.__parent = parent || null;
      if(Array.isArray(node.content)){
        for(const child of node.content) recur(child,node);
      }
    }
  }
  recur(root,null);
  return root;
}

module.exports = { validateDocument, attachParents };
