/*
PROMPT COPILOT
Implemente uma fábrica de blocos semânticos.
Cada função deve criar um bloco válido conforme o AST oficial.
Não renderizar HTML.
Não validar regras globais (isso é papel do validator).
Cada bloco deve conter um ID único e apenas campos compatíveis com seu tipo.
Evite valores opcionais implícitos — seja explícito.
*/
// block-factory.js — cria instâncias de blocos
import { createNode, BlockTypes } from '../core/ast.js';

export function createBlock(type, props = {}) {
	if (!Object.values(BlockTypes).includes(type)) {
		throw new Error('Invalid block type: ' + type);
	}
	// only include known properties per type; caller should be explicit
	return createNode(type, props);
}

export function title(text) { return createBlock(BlockTypes.TITLE, { text: text || '' }); }
export function paragraph(text) { return createBlock(BlockTypes.PARAGRAPH, { text: text || '' }); }
export function section(titleText, children = []) { return createBlock(BlockTypes.SECTION, { title: titleText || '', content: Array.isArray(children) ? children : [] }); }

