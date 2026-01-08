// DocCollab-v0
// AST é a única fonte de verdade.
// Nenhuma lógica fora do modelo semântico é permitida.

function escapeText(s){ if(!s) return ''; return String(s).replace(/\\/g,'\\\\').replace(/\{/g,'\\{').replace(/\}/g,'\\}').replace(/\$/g,'\\$').replace(/%/g,'\\%').replace(/_/g,'\\_'); }
function comment(id){ return `% DOCCOLLAB-BLOCK-ID: ${id}\n`; }
function renderChildren(block){
  const children = block.content || block.children || block.blocks || [];
  return children.map(renderBlock).join('');
}
function normalizeParagraphs(s){ if(!s && s !== 0) return ''; let t = String(s); t = t.replace(/\r\n/g,'\n').replace(/\r/g,'\n'); t = t.replace(/<br\s*\/?>(\s*)/gi,'\n'); t = t.replace(/<\/p>\s*<p>/gi,'\n\n'); t = t.replace(/\n{3,}/g,'\n\n'); t = t.replace(/^\s+|\s+$/g,''); return t; }
function htmlToLaTeX(s){ if(!s && s !== 0) return ''; let t = String(s); t = t.replace(/<em>([\s\S]*?)<\/em>/gi, (m, inner)=>`\\emph{${escapeText(inner.replace(/<[^>]+>/g,''))}}`); t = t.replace(/<i>([\s\S]*?)<\/i>/gi, (m, inner)=>`\\emph{${escapeText(inner.replace(/<[^>]+>/g,''))}}`); t = t.replace(/<(strong|b)>([\s\S]*?)<\/(?:strong|b)>/gi, (m, tag, inner)=>`\\textbf{${escapeText(inner.replace(/<[^>]+>/g,''))}}`); t = t.replace(/<code>([\s\S]*?)<\/code>/gi, (m, inner)=>`\\texttt{${escapeText(inner.replace(/<[^>]+>/g,''))}}`); t = t.replace(/<[^>]+>/g,''); return t; }
function renderParagraph(block){ const txt = normalizeParagraphs(block.text || ''); if(!txt) return comment(block.id)+'\n'; const paras = txt.split(/\n{2,}/); return comment(block.id) + paras.map(p=>htmlToLaTeX(p)).join('\n\n') + '\n\n'; }
function renderSection(block){ return comment(block.id) + `\n\\section{${htmlToLaTeX(normalizeParagraphs(block.title||''))}}\n` + renderChildren(block); }
function renderSubsection(block){ return comment(block.id) + `\n\\subsection{${htmlToLaTeX(normalizeParagraphs(block.title||''))}}\n` + renderChildren(block); }
function renderEquation(block){ return comment(block.id) + `\n\\begin{equation}\\label{blk:${block.id}}\n${block.latex || block.text || ''}\n\\end{equation}\n`; }
function renderFigure(block){ let src = block.src||''; src = src.replace(/\\\\/g,'/'); const caption = htmlToLaTeX(normalizeParagraphs(block.caption||'')); return comment(block.id)+`\n\\begin{figure}[h]\n\\centering\n\\IfFileExists{${src}}{\\includegraphics[width=0.8\\linewidth]{${src}}}{\\fbox{Missing image: ${src}}}\\caption{${caption}}\\label{blk:${block.id}}\\end{figure}\n`; }
function renderTable(block){ const rows = block.rows || [[{text:''},{text:''}],[{text:''},{text:''}]]; const numCols = rows.length>0 ? rows[0].length : 2; const colSpec = 'l'.repeat(numCols); let latex = comment(block.id)+`\n\\begin{table}[h]\n\\centering\n\\begin{tabular}{|${colSpec.split('').join('|')}|}\n\\hline\n`; rows.forEach((row,rIdx)=> { const cells = row.map(c=>htmlToLaTeX(normalizeParagraphs(c.text||''))); latex += cells.join(' & ') + ' \\\\\n\\hline\n'; }); latex += `\\end{tabular}\n\\caption{${htmlToLaTeX(normalizeParagraphs(block.caption||''))}}\\label{blk:${block.id}}\n\\end{table}\n`; return latex; }
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
    case 'title': return comment(block.id)+`\\title{${htmlToLaTeX(normalizeParagraphs(block.text||block.title||''))}}\n`;
    case 'author': return comment(block.id)+`\\author{${htmlToLaTeX(normalizeParagraphs(block.text||block.name||''))}}\n`;
    case 'abstract': {
      const txt = normalizeParagraphs(block.text || '');
      const paras = txt ? txt.split(/\n{2,}/).map(p=>htmlToLaTeX(p)).join('\n\n') : '';
      return comment(block.id)+`\\begin{abstract}\n${paras}\n\\end{abstract}\n`;
    }
    case 'section': return renderSection(block);
    case 'subsection': return renderSubsection(block);
    case 'paragraph': return renderParagraph(block);
    case 'equation': return renderEquation(block);
    case 'figure': return renderFigure(block);
    case 'table': return renderTable(block);
    case 'pagebreak': return comment(block.id)+`\\newpage\n`;
    case 'citation': return comment(block.id)+`\\begin{quote}\\textit{${htmlToLaTeX(normalizeParagraphs(block.text||''))}}\\end{quote}\n`;
    case 'bibliography': return comment(block.id) + renderChildren(block);
    default: return comment(block.id) + renderChildren(block);
  }
}
function renderHeader(meta, template){
  const title = meta && meta.title ? `\\title{${htmlToLaTeX(normalizeParagraphs(meta.title))}}\n` : '';
  const author = meta && meta.author ? `\\author{${htmlToLaTeX(normalizeParagraphs(meta.author))}}\n` : '';
  // ensure sensible defaults for UTF-8 and fonts, enable page numbers
  const defaultPkgs = `\\usepackage[utf8]{inputenc}\n\\usepackage[T1]{fontenc}\n\\usepackage{lmodern}\n\\usepackage{graphicx}\n\\usepackage{fancyhdr}\n\\pagestyle{fancy}\n\\fancyhf{}\n\\fancyfoot[C]{\\thepage}\n\\renewcommand{\\headrulewidth}{0pt}\n`;
  const pkgs = (template && template.packages) ? template.packages.map(p=>`\\usepackage{${p}}`).join('\n') + '\n' : '';
  return `\\documentclass[11pt]{article}\n${defaultPkgs}${pkgs}${title}${author}\\begin{document}\n`;
}
function generateLaTeX(ast, template){
  const meta = ast.metadata || {};
  const header = renderHeader(meta, template);
  const bodyNodes = ast.blocks || ast.content || [];
  
  // separate title/author from rest of body
  let titleBlock = null;
  let authorBlock = null;
  const contentBlocks = [];
  
  for (const b of bodyNodes) {
    if (b.type === 'title' && !titleBlock) titleBlock = b;
    else if (b.type === 'author' && !authorBlock) authorBlock = b;
    else contentBlocks.push(b);
  }
  
  let preamble = '';
  if (titleBlock) preamble += renderBlock(titleBlock);
  if (authorBlock) preamble += renderBlock(authorBlock);
  if (titleBlock || authorBlock) preamble += '\\maketitle\n\\vspace{1em}\n';
  
  const body = contentBlocks.map(renderBlock).join('');
  const bibliography = renderBibliography(ast);
  const end = '\n\\end{document}\n';
  return header + preamble + body + bibliography + end;
}
module.exports = { generateLaTeX };
