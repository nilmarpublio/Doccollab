// DocCollab-v0
// AST é a única fonte de verdade.
// Nenhuma lógica fora do modelo semântico é permitida.

// server/lib/latex-generator.js — CommonJS LaTeX generator (used for server-side tests)
function escapeText(s){ if(!s) return ''; return String(s).replace(/\\/g,'\\\\').replace(/\{/g,'\\{').replace(/\}/g,'\\}').replace(/\$/g,'\\$').replace(/%/g,'\\%').replace(/_/g,'\\_'); }
function htmlToLaTeX(s){ if(!s) return ''; let t = String(s); // convert common inline tags to LaTeX, escaping inner text
  t = t.replace(/<em>([\s\S]*?)<\/em>/gi, (m, inner) => `\\emph{${escapeText(inner.replace(/<[^>]+>/g,''))}}`);
  t = t.replace(/<i>([\s\S]*?)<\/i>/gi, (m, inner) => `\\emph{${escapeText(inner.replace(/<[^>]+>/g,''))}}`);
  t = t.replace(/<(strong|b)>([\s\S]*?)<\/(?:strong|b)>/gi, (m, tag, inner) => `\\textbf{${escapeText(inner.replace(/<[^>]+>/g,''))}}`);
  t = t.replace(/<code>([\s\S]*?)<\/code>/gi, (m, inner) => `\\texttt{${escapeText(inner.replace(/<[^>]+>/g,''))}}`);
  t = t.replace(/<br\s*\/?>(\s*)/gi,'\\\\\n');
  t = t.replace(/<[^>]+>/g,'');
  return t;
}
function comment(id){ return `% DOCCOLLAB-BLOCK-ID: ${id}\n`; }
function renderChildren(block){
  const children = block.content || block.children || block.blocks || [];
  return children.map(renderBlock).join('');
}
function renderParagraph(block){ const txt = block.text || ''; return comment(block.id) + `${htmlToLaTeX(txt)}\n\n`; }
function renderSection(block){ return comment(block.id) + `\n\\section{${htmlToLaTeX(block.title||'')}}\n` + renderChildren(block); }
function renderSubsection(block){ return comment(block.id) + `\n\\subsection{${htmlToLaTeX(block.title||'')}}\n` + renderChildren(block); }
function renderEquation(block){ return comment(block.id) + `\n\\begin{equation}\\label{blk:${block.id}}\n${block.latex || escapeText(block.text||'')}\n\\end{equation}\n`; }
function renderFigure(block){ const src = escapeText(block.src||''); const caption = escapeText(block.caption||''); return comment(block.id)+`\n\\begin{figure}[h]\n\\centering\n\\IfFileExists{${src}}{\\includegraphics[width=0.8\\linewidth]{${src}}}{\\fbox{Missing image: ${src}}}\\caption{${caption}}\\label{blk:${block.id}}\\end{figure}\n`; }
function renderBibliography(ast){
  const entries=[]; const nodes=(ast.blocks||ast.content||[]);
  function walk(n){ if(!n) return; if(n.type==='bibliography'){ for(const e of (n.entries||[])) entries.push(e); } const ch=n.content||n.children||n.blocks||[]; for(const c of ch) walk(c); }
  for(const n of nodes) walk(n);
  if(entries.length===0) return '';
  const items = entries.map((e,i)=>`\\bibitem{${e.id||e.key||('ref'+(i+1))}} ${escapeText(e.text||e.title||'')}\n`).join('');
  return `% DOCCOLLAB-BIB\n\\begin{thebibliography}{99}\n${items}\\end{thebibliography}\n`;
}
function renderBlock(block){
  switch(block.type){
    case 'title': return comment(block.id)+`\\title{${escapeText(block.text||block.title||'')}}\\maketitle\n\\vspace{1em}\n`;
    case 'author': return comment(block.id)+`\\author{${escapeText(block.text||block.name||'')}}\n`;
    case 'abstract': return comment(block.id)+`\\begin{abstract}\n${escapeText(block.text||'')}\n\\end{abstract}\n`;
    case 'section': return renderSection(block);
    case 'subsection': return renderSubsection(block);
    case 'paragraph': return renderParagraph(block);
    case 'equation': return renderEquation(block);
    case 'figure': return renderFigure(block);
    case 'bibliography': return comment(block.id) + renderChildren(block);
    default: return comment(block.id) + renderChildren(block);
  }
}
function renderHeader(meta, template){
  const title = meta && meta.title ? `\\title{${htmlToLaTeX(meta.title)}}\n` : '';
  const author = meta && meta.author ? `\\author{${htmlToLaTeX(meta.author)}}\n` : '';
  const pkgs = (template && template.packages) ? template.packages.map(p=>`\\usepackage{${p}}`).join('\n') + '\n' : '';
  return `\\documentclass[11pt]{article}\n${pkgs}${title}${author}\n\\begin{document}\n`;
}
function generateLaTeX(ast, template){
  const meta = ast.metadata || {};
  const header = renderHeader(meta, template);
  const bodyNodes = ast.blocks || ast.content || [];
  const body = bodyNodes.map(renderBlock).join('');
  const bibliography = renderBibliography(ast);
  const end = '\n\\end{document}\n';
  return header + body + bibliography + end;
}
module.exports = { generateLaTeX };
