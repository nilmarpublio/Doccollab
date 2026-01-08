/*
PROMPT COPILOT
Implemente o validador formal do AST do DocCollab-v0.
O validador deve analisar o documento inteiro e retornar uma lista estruturada de erros.
Não lançar exceções — sempre retornar erros de forma previsível.
Cada erro deve conter: código, mensagem legível, bloco relacionado (se houver).
Regras obrigatórias:
  • Exatamente um título
  • Resumo antes da primeira seção
  • Subsection só pode existir dentro de Section
  • Equações não podem existir fora de Section/Subsection
  • Documento não pode estar vazio
Não incluir lógica de UI ou mensagens hardcoded fora do sistema de i18n.
*/
// validator.js — validações formais do AST (frontend)
export function validateAST(ast) {
  const errors = [];
  const warnings = [];

  if (!ast || !Array.isArray(ast.blocks) && !Array.isArray(ast.content)) {
    errors.push({ code: 'EMPTY_DOCUMENT', message: 'Documento vazio ou AST mal formado.' });
    return { errors, warnings };
  }

  // normalize root children array (support blocks or content)
  const rootChildren = Array.isArray(ast.blocks) ? ast.blocks : (Array.isArray(ast.content) ? ast.content : []);

  // utilities
  function traverse(node, ancestors = []){
    if (!node) return;
    const nodeType = node.type;
    // collect
    allNodes.push({ node, ancestors });
    const children = node.blocks || node.content || node.children || [];
    for (const c of children) traverse(c, ancestors.concat(node));
  }

  const allNodes = [];
  for (const b of rootChildren) traverse(b, []);

  // Rule: document cannot be empty
  if (allNodes.length === 0) {
    errors.push({ code: 'DOCUMENT_EMPTY', message: 'O documento não pode ficar vazio.' });
  }

  // Rule: only 1 title
  const titles = allNodes.filter(x => x.node.type === 'title');
  if (titles.length !== 1) {
    errors.push({ code: 'INVALID_TITLE_COUNT', message: 'O documento deve conter exatamente um título.' });
  }

  // Rule: abstract before first section (top-level)
  const top = rootChildren;
  const firstSectionIndex = top.findIndex(n => n.type === 'section');
  const abstractIndex = top.findIndex(n => n.type === 'abstract');
  if (abstractIndex !== -1 && firstSectionIndex !== -1 && abstractIndex > firstSectionIndex) {
    errors.push({ code: 'ABSTRACT_POSITION', message: 'Resumo (abstract) deve aparecer antes da primeira seção.' });
  }

  // Rule: subsection only inside section
  const subsections = allNodes.filter(x => x.node.type === 'subsection');
  for (const s of subsections) {
    const hasSectionAncestor = s.ancestors.some(a => a.type === 'section');
    if (!hasSectionAncestor) {
      errors.push({ code: 'SUBSECTION_OUTSIDE_SECTION', message: 'Subsection só é permitida dentro de uma Section.' });
    }
  }

  // Rule: equation only inside section/subsection
  const equations = allNodes.filter(x => x.node.type === 'equation');
  for (const e of equations) {
    const ok = e.ancestors.some(a => a.type === 'section' || a.type === 'subsection');
    if (!ok) {
      errors.push({ code: 'EQUATION_OUTSIDE_SECTION', message: 'Equações só são permitidas dentro de Section ou Subsection.' });
    }
  }

  // Rule: references only if cited
  // Collect citation ids and bibliography entries
  const citations = new Set(allNodes.filter(x => x.node.type === 'citation').map(x => x.node.ref || x.node.id || x.node.key).filter(Boolean));
  const bibEntries = [];
  for (const item of allNodes.filter(x => x.node.type === 'bibliography')) {
    const entries = item.node.entries || [];
    for (const e of entries) {
      if (e.id) bibEntries.push(e.id);
      else if (e.key) bibEntries.push(e.key);
    }
  }
  // Check duplicate bib keys
  const bibKeys = allNodes.filter(x => x.node.type === 'bibliography').flatMap(x => (x.node.entries||[]).map(e => e.id || e.key)).filter(Boolean);
  const dup = bibKeys.filter((k,i,arr)=> arr.indexOf(k)!==i);
  if (dup.length>0) {
    errors.push({ code: 'BIB_DUPLICATE_KEY', message: `Chaves de bibliografia duplicadas: ${[...new Set(dup)].join(', ')}` });
  }
  for (const be of bibEntries) {
    if (!citations.has(be)) {
      errors.push({ code: 'BIB_ENTRY_NOT_CITED', message: `Entrada de bibliografia '${be}' não foi citada no documento.` });
    }
  }

  return { errors, warnings };
}
