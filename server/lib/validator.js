// DocCollab-v0
// AST é a única fonte de verdade.
// Nenhuma lógica fora do modelo semântico é permitida.

// server/lib/validator.js — CommonJS validator para testes e uso server-side
function traverseCollect(rootChildren) {
  const all = [];
  function traverse(node, ancestors = []){
    if (!node) return;
    all.push({ node, ancestors });
    const children = node.blocks || node.content || node.children || [];
    for (const c of children) traverse(c, ancestors.concat(node));
  }
  for (const b of rootChildren) traverse(b, []);
  return all;
}

function validate(ast){
  const errors = [];
  const warnings = [];
  const rootChildren = Array.isArray(ast.blocks) ? ast.blocks : (Array.isArray(ast.content) ? ast.content : []);

  if (!ast || (!Array.isArray(rootChildren))) {
    errors.push({ code: 'EMPTY_DOCUMENT', message: 'Documento vazio ou AST mal formado.' });
    return { errors, warnings };
  }

  const allNodes = traverseCollect(rootChildren);
  if (allNodes.length === 0) errors.push({ code: 'DOCUMENT_EMPTY', message: 'O documento não pode ficar vazio.' });

  const titles = allNodes.filter(x => x.node.type === 'title');
  if (titles.length !== 1) errors.push({ code: 'INVALID_TITLE_COUNT', message: 'O documento deve conter exatamente um título.' });

  const firstSectionIndex = rootChildren.findIndex(n => n.type === 'section');
  const abstractIndex = rootChildren.findIndex(n => n.type === 'abstract');
  if (abstractIndex !== -1 && firstSectionIndex !== -1 && abstractIndex > firstSectionIndex) {
    errors.push({ code: 'ABSTRACT_POSITION', message: 'Resumo (abstract) deve aparecer antes da primeira seção.' });
  }

  const subsections = allNodes.filter(x => x.node.type === 'subsection');
  for (const s of subsections) {
    const hasSectionAncestor = s.ancestors.some(a => a.type === 'section');
    if (!hasSectionAncestor) errors.push({ code: 'SUBSECTION_OUTSIDE_SECTION', message: 'Subsection só é permitida dentro de uma Section.' });
  }

  const equations = allNodes.filter(x => x.node.type === 'equation');
  for (const e of equations) {
    const ok = e.ancestors.some(a => a.type === 'section' || a.type === 'subsection');
    if (!ok) errors.push({ code: 'EQUATION_OUTSIDE_SECTION', message: 'Equações só são permitidas dentro de Section ou Subsection.' });
  }

  const citations = new Set(allNodes.filter(x => x.node.type === 'citation').map(x => x.node.ref || x.node.id || x.node.key).filter(Boolean));
  const bibEntries = [];
  for (const item of allNodes.filter(x => x.node.type === 'bibliography')) {
    const entries = item.node.entries || [];
    for (const e of entries) {
      if (e.id) bibEntries.push(e.id);
      else if (e.key) bibEntries.push(e.key);
    }
  }
  for (const be of bibEntries) {
    if (!citations.has(be)) errors.push({ code: 'BIB_ENTRY_NOT_CITED', message: `Entrada de bibliografia '${be}' não foi citada no documento.` });
  }

  return { errors, warnings };
}

module.exports = { validate };
