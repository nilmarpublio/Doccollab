// DocCollab-v0
// AST é a única fonte de verdade.
// Nenhuma lógica fora do modelo semântico é permitida.

// server/lib/bib-generator.js — exporta .bib a partir do AST
function escape(v){ if(v==null) return ''; return String(v).replace(/\n/g,' ').replace(/\r/g,' ').trim(); }
function toBibEntry(entry){
  const key = entry.id || entry.key || 'ref';
  const type = entry.type || 'article';
  const fields = Object.entries(entry).filter(([k])=>!['id','key','type'].includes(k)).map(([k,v])=>`  ${k} = {${escape(v)}}`).join(',\n');
  return `@${type}{${key},\n${fields}\n}`;
}
function generateBib(ast){
  const nodes = ast.blocks || ast.content || [];
  const entries = [];
  function walk(n){ if(!n) return; if(n.type==='bibliography'){ for(const e of (n.entries||[])) entries.push(e); } const ch = n.content||n.children||n.blocks||[]; for(const c of ch) walk(c); }
  for(const n of nodes) walk(n);
  if(entries.length===0) return '';
  return entries.map(toBibEntry).join('\n\n');
}
module.exports = { generateBib };
