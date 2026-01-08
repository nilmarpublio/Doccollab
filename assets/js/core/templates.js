// templates.js — definições de templates (não modificam o AST)
// PROMPT COPILOT
// Sistema de templates do DocCollab-v0. Cada template define ordem,
// blocos obrigatórios/opcionais e pacotes LaTeX recomendados. Não
// aplica alterações ao AST; fornece apenas funções de inspeção.

export const Templates = {
  scientific_article: {
    id: 'scientific-article',
    name: 'Scientific Article',
    order: ['title','author','abstract','section','bibliography'],
    required: ['title','author','abstract'],
    optional: ['bibliography','figure','equation','table'],
    packages: ['amsmath','amssymb','graphicx','hyperref'],
    numberingStyle: { sections: 'arabic', equations: 'arabic' },
    bibliography: { engine: 'bibtex', style: 'plain' }
  },
  technical_report: {
    id: 'technical-report',
    name: 'Technical Report',
    order: ['title','author','abstract','section','bibliography'],
    required: ['title'],
    optional: ['author','abstract','bibliography','subsection'],
    packages: ['amsmath','graphicx','hyperref'],
    numberingStyle: { sections: 'arabic', equations: 'arabic' },
    bibliography: { engine: 'bibtex', style: 'plain' }
  },
  dissertation: {
    id: 'dissertation',
    name: 'Dissertation',
    order: ['title','author','abstract','section','subsection','bibliography'],
    required: ['title','author'],
    optional: ['abstract','bibliography','subsection'],
    packages: ['amsmath','amssymb','graphicx','hyperref'],
    numberingStyle: { sections: 'roman', equations: 'arabic' },
    bibliography: { engine: 'biber', style: 'apa' }
  },
  generic: {
    id: 'generic',
    name: 'Generic',
    order: ['title','section','bibliography'],
    required: ['title'],
    optional: ['author','abstract','bibliography','figure','table'],
    packages: ['graphicx','hyperref'],
    numberingStyle: { sections: 'arabic', equations: 'arabic' },
    bibliography: { engine: 'bibtex', style: 'plain' }
  }
};

/**
 * Recupera um template conhecido por `name` (chave). Lança erro se não
 * for encontrado.
 * @param {string} name
 */
export function getTemplate(name = 'generic') {
  const key = String(name || '').toLowerCase();
  const t = Templates[key];
  if (!t) throw new Error(`Template desconhecido: ${name}`);
  return t;
}

/** Lista os nomes dos templates disponíveis. */
export function listTemplates() {
  return Object.keys(Templates);
}

/**
 * Inspeciona um AST contra um template (alto nível). Retorna um objeto
 * contendo:
 *  - missing: blocos obrigatórios ausentes
 *  - present: contagem por tipo dos blocos de primeiro nível
 *  - orderIssues: lista de tipos em ordem inesperada (alto-nível)
 *  - notes: mensagens explicativas
 *
 * NÃO substitui o `validator` — evita duplicar regras semânticas e faz
 * apenas verificações estruturais relacionadas ao template.
 */
export function inspectASTByTemplate(ast, templateName = 'generic') {
  const template = getTemplate(templateName);
  const blocks = Array.isArray(ast.blocks) ? ast.blocks : (Array.isArray(ast.content) ? ast.content : []);

  const present = {};
  const observed = [];
  for (const b of blocks) {
    present[b.type] = (present[b.type] || 0) + 1;
    observed.push(b.type);
  }

  const missing = (template.required || []).filter(t => !present[t]);

  // Verifica ordem esperada (subsequência) — sinaliza se tipos da ordem
  // do template aparecem fora da sequência observada.
  const expected = template.order || [];
  const orderIssues = [];
  let lastPos = -1;
  for (const exp of expected) {
    const pos = observed.indexOf(exp);
    if (pos === -1) continue; // ausência é reportada em `missing`
    if (pos < lastPos) orderIssues.push(exp);
    lastPos = pos;
  }

  const notes = [];
  if (missing.length) notes.push('Existem blocos obrigatórios ausentes no documento conforme o template.');
  if (orderIssues.length) notes.push('A ordem de blocos observada diverge da ordem esperada pelo template.');

  return { missing, present, orderIssues, notes };
}

/** Retorna os pacotes LaTeX recomendados para o template. */
export function latexPackagesForTemplate(name = 'generic') {
  const t = getTemplate(name);
  return Array.isArray(t.packages) ? Array.from(t.packages) : [];
}

export default {
  Templates,
  getTemplate,
  listTemplates,
  inspectASTByTemplate,
  latexPackagesForTemplate
};
