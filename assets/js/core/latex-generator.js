// DocCollab-v0
// AST é a única fonte de verdade.
// Nenhuma lógica fora do modelo semântico é permitida.
// client-side LaTeX generator (deterministic, synchronous)

function escapeText(s) {
  if (!s && s !== 0) return "";
  return String(s)
    .replace(/\\/g, "\\\\")
    .replace(/\{/g, "\\{")
    .replace(/\}/g, "\\}")
    .replace(/\$/g, "\\$")
    .replace(/%/g, "\\%")
    .replace(/_/g, "\\_");
}
function comment(id) {
  return `% DOCCOLLAB-BLOCK-ID: ${id}\n`;
}

function normalizeParagraphs(s) {
  if (!s && s !== 0) return "";
  let t = String(s);
  // normalize line endings
  t = t.replace(/\r\n/g, "\n").replace(/\r/g, "\n");
  // convert HTML breaks to newlines
  t = t.replace(/<br\s*\/?>(\s*)/gi, "\n");
  // convert adjacent paragraph tags to double newline
  t = t.replace(/<\/p>\s*<p>/gi, "\n\n");
  // strip remaining tags (keep content)
  t = t.replace(/<[^>]+>/g, "");
  // collapse excessive newlines to max two (one paragraph gap)
  t = t.replace(/\n{3,}/g, "\n\n");
  // trim edges
  t = t.replace(/^\s+|\s+$/g, "");
  return t;
}

function htmlToLaTeX(s) {
  if (!s && s !== 0) return "";
  let t = String(s);
  // convert common inline tags to LaTeX, escaping their inner text
  t = t.replace(/<em>([\s\S]*?)<\/em>/gi, (m, inner) => `\\emph{${escapeText(inner.replace(/<[^>]+>/g, ''))}}`);
  t = t.replace(/<i>([\s\S]*?)<\/i>/gi, (m, inner) => `\\emph{${escapeText(inner.replace(/<[^>]+>/g, ''))}}`);
  t = t.replace(/<(strong|b)>([\s\S]*?)<\/(?:strong|b)>/gi, (m, tag, inner) => `\\textbf{${escapeText(inner.replace(/<[^>]+>/g, ''))}}`);
  t = t.replace(/<code>([\s\S]*?)<\/code>/gi, (m, inner) => `\\texttt{${escapeText(inner.replace(/<[^>]+>/g, ''))}}`);
  // remove any remaining tags but keep content
  t = t.replace(/<[^>]+>/g, '');
  return t;
}

function renderChildren(block) {
  const children = block.content || block.children || block.blocks || [];
  return children.map(renderBlock).join("");
}

function renderParagraph(block) {
  const txt = normalizeParagraphs(block.text || "");
  if (!txt) return comment(block.id) + "\n";
  const paras = txt.split(/\n{2,}/);
  // convert inline HTML to LaTeX (paras already trimmed)
  return comment(block.id) + paras.map((p) => htmlToLaTeX(p)).join("\n\n") + "\n\n";
}
function renderSection(block) {
  return (
    comment(block.id) +
    `\n\\section{${htmlToLaTeX(normalizeParagraphs(block.title || ""))}}\n` +
    renderChildren(block)
  );
}
function renderSubsection(block) {
  return (
    comment(block.id) +
    `\n\\subsection{${htmlToLaTeX(normalizeParagraphs(block.title || ""))}}\n` +
    renderChildren(block)
  );
}
function renderEquation(block) {
  return (
    comment(block.id) +
    `\n\\begin{equation}\\label{blk:${block.id}}\n${
      block.latex || escapeText(block.text || "")
    }\n\\end{equation}\n`
  );
}
function renderFigure(block) {
  const src = escapeText(block.src || "");
  const caption = htmlToLaTeX(normalizeParagraphs(block.caption || ""));
  return (
    comment(block.id) +
    `\n\\begin{figure}[h]\n\\centering\n\\IfFileExists{${src}}{\\includegraphics[width=0.8\\linewidth]{${src}}}{\\fbox{Missing image: ${src}}}\\caption{${caption}}\\label{blk:${block.id}}\\end{figure}\n`
  );
}

function renderBibliography(ast) {
  const entries = [];
  const nodes = ast.blocks || ast.content || [];
  function walk(n) {
    if (!n) return;
    if (n.type === "bibliography") {
      for (const e of n.entries || []) entries.push(e);
    }
    const ch = n.content || n.children || n.blocks || [];
    for (const c of ch) walk(c);
  }
  for (const n of nodes) walk(n);
  if (entries.length === 0) return "";
  const items = entries
    .map(
      (e, i) =>
        `\\bibitem{${e.id || e.key || "ref" + (i + 1)}} ${escapeText(
          e.text || e.title || ""
        )}\n`
    )
    .join("");
  return `% DOCCOLLAB-BIB\n\\begin{thebibliography}{99}\n${items}\\end{thebibliography}\n`;
}

function renderBlock(block) {
  switch (block.type) {
    case "title":
      return (
        comment(block.id) +
        `\\title{${htmlToLaTeX(normalizeParagraphs(block.text || block.title || ""))}\\maketitle\n\\vspace{1em}\n`
      );
    case "author":
      return (
        comment(block.id) +
        `\\author{${htmlToLaTeX(normalizeParagraphs(block.text || block.name || ""))}}\n`
      );
    case "abstract":
      {
        const txt = normalizeParagraphs(block.text || "");
        const paras = txt ? txt.split(/\n{2,}/).map((p) => htmlToLaTeX(p)).join("\n\n") : "";
        return comment(block.id) + `\\begin{abstract}\n${paras}\n\\end{abstract}\n`;
      }
    case "section":
      return renderSection(block);
    case "subsection":
      return renderSubsection(block);
    case "paragraph":
      return renderParagraph(block);
    case "equation":
      return renderEquation(block);
    case "figure":
      return renderFigure(block);
    case "bibliography":
      return comment(block.id) + renderChildren(block);
    default:
      return comment(block.id) + renderChildren(block);
  }
}

function renderHeader(meta, template) {
  const title =
    meta && meta.title ? `\\title{${htmlToLaTeX(normalizeParagraphs(meta.title))}}\n` : "";
  const author =
    meta && meta.author ? `\\author{${htmlToLaTeX(normalizeParagraphs(meta.author))}}\n` : "";
  const pkgs =
    template && template.packages
      ? template.packages.map((p) => `\\usepackage{${p}}`).join("\n") + "\n"
      : "";
  return `\\documentclass[11pt]{article}\n${pkgs}${title}${author}\\begin{document}\n`;
}

export function generateLaTeX(ast, template) {
  const meta =
    ast && (ast.metadata || ast.meta) ? ast.metadata || ast.meta : {};
  const header = renderHeader(meta, template);
  const bodyNodes = ast.blocks || ast.content || [];
  const body = bodyNodes.map(renderBlock).join("");
  const bibliography = renderBibliography(ast);
  const end = "\n\\end{document}\n";
  return header + body + bibliography + end;
}

export default { generateLaTeX };
