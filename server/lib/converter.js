// DocCollab-v0
// AST é a única fonte de verdade.
// Nenhuma lógica fora do modelo semântico é permitida.

// Conversor simples AST -> LaTeX (módulo CommonJS)
// Objetivo: gerar `.tex` determinístico com marcadores de bloco para rastreabilidade.

function escapeText(s) {
  if (!s) return '';
  return String(s)
    .replace(/\\/g, '\\\\')
    .replace(/\{/g, '\\{')
    .replace(/\}/g, '\\}')
    .replace(/\$/g, '\\\$')
    .replace(/%/g, '\\%')
    .replace(/_/g, '\\_')
    .replace(/\^/g, '\\^{}')
    .replace(/~/g, '\\~{}');
}

function comment(id) {
  return `% DOCCOLLAB-BLOCK-ID: ${id}\n`;
}

function renderBlock(block) {
  if (!block || typeof block !== 'object') return '';
  const id = block.id || 'unknown';
  switch (block.type) {
    case 'title':
      return comment(id) + `\\title{${escapeText(block.text || block.title || '')}}\\maketitle\\n\\vspace{1em}\\n`;
    case 'author':
      return comment(id) + `\\author{${escapeText(block.text || block.name || '')}}\\n`;
    case 'abstract':
      return comment(id) + `\\begin{abstract}\\n${escapeText(block.text || '')}\\n\\end{abstract}\\n`;
    case 'section':
      return comment(id) + `\\section{${escapeText(block.title || '')}}\\n` + renderChildren(block);
    case 'subsection':
      return comment(id) + `\\subsection{${escapeText(block.title || '')}}\\n` + renderChildren(block);
    case 'paragraph':
      return comment(id) + `${escapeText(block.text || '')}\\n\\n`;
    case 'equation':
      return comment(id) + `\\begin{equation}\\label{blk:${id}}\\n${block.latex || escapeText(block.text || '')}\\n\\end{equation}\\n`;
    case 'figure':
      const src = escapeText(block.src || '');
      const caption = escapeText(block.caption || '');
      return comment(id) + `\\begin{figure}[h]\\centering\\includegraphics[width=0.8\\linewidth]{${src}}\\caption{${caption}}\\label{blk:${id}}\\end{figure}\\n`;
    case 'bibliography':
      // simple inline bibliography rendering
      return comment(id) + renderBibliography(block.entries || []);
    case 'document':
      return renderChildren(block);
    default:
      // unknown block: try to render children if any
      return comment(id) + renderChildren(block);
  }
}

function renderChildren(block) {
  if (!block) return '';
  const children = block.content || block.children || [];
  return children.map(renderBlock).join('');
}

function renderBibliography(entries) {
  if (!entries || !entries.length) return '';
  const items = entries.map((e, i) => {
    const key = e.id || `ref${i+1}`;
    const text = escapeText(e.text || e.title || '');
    return `\\bibitem{${key}} ${text}\\n`;
  }).join('');
  return `\\begin{thebibliography}{99}\\n${items}\\end{thebibliography}\\n`;
}

function buildPreamble(meta) {
  const title = meta && (meta.title || meta.documentTitle) ? `\\title{${escapeText(meta.title || meta.documentTitle)}}\\n` : '';
  const author = meta && meta.author ? `\\author{${escapeText(meta.author)}}\\n` : '';
  return `\\documentclass[11pt]{article}\\n\\usepackage[utf8]{inputenc}\\n\\usepackage{amsmath,amssymb}\\n\\usepackage{graphicx}\\n\\usepackage{hyperref}\\n${title}${author}\\n\\begin{document}\\n`;
}

function convert(ast, options) {
  options = options || {};
  const meta = ast.meta || options.meta || {};
  const pre = buildPreamble(meta);
  const body = renderBlock(ast);
  const end = '\\n\\end{document}\\n';
  // deterministic output: stable ordering, no timestamps
  return pre + body + end;
}

module.exports = { convert };
