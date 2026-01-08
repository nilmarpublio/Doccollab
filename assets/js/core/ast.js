/*
PROMPT COPILOT
Implemente o modelo de dados central do DocCollab-v0.
Este arquivo define o AST oficial, que é a única fonte de verdade do sistema.
Não inclua lógica de UI, validação ou exportação.
Apenas estruturas de dados e funções puras para criação e manipulação segura do AST.
Todo documento deve conter metadata e um array ordenado de blocos.
Use UUID para identificação.
Não permita tipos de blocos fora do enum definido.
*/
// ast.js — helpers mínimos para manipular AST no frontend

export function createEmptyDocument(language = 'pt-BR', documentType = 'generic', template = 'generic') {
	return {
		metadata: {
			id: (typeof crypto !== 'undefined' && crypto.randomUUID) ? crypto.randomUUID() : `id-${Date.now()}-${Math.random().toString(36).slice(2,8)}`,
			language,
			documentType,
			template,
			createdAt: new Date().toISOString(),
			updatedAt: new Date().toISOString()
		},
		blocks: []
	};
}

export const BlockTypes = {
	TITLE: 'title',
	AUTHOR: 'author',
	ABSTRACT: 'abstract',
	SECTION: 'section',
	SUBSECTION: 'subsection',
	PARAGRAPH: 'paragraph',
	EQUATION: 'equation',
	FIGURE: 'figure',
	TABLE: 'table',
	PAGEBREAK: 'pagebreak',
	CITATION: 'citation',
	BIBLIOGRAPHY: 'bibliography'
};

export function createNode(type, props = {}) {
	return Object.assign({ type, id: props.id || `b_${Date.now()}_${Math.random().toString(36).slice(2,8)}` }, props);
}

export function serialize(ast) { return JSON.stringify(ast, null, 2); }

export function parse(json) { return JSON.parse(json); }
