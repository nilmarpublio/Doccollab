// DocCollab-v0 - VERSÃO COM CITATION - 2026-01-02-001
// AST é a única fonte de verdade.
// Nenhuma lógica fora do modelo semântico é permitida.

// PROMPT COPILOT
// Implemente as regras de convivência entre blocos no editor.
// Este arquivo define quais blocos podem ser criados em cada contexto.
// Exemplo: Subsection só pode ser criada dentro de Section.
// As regras devem ser declarativas, não espalhadas pelo código.
// Não renderizar UI.
// Não modificar o AST diretamente.

import { BlockTypes } from '../core/ast.js';

/**
 * Regras declarativas de quais tipos de blocos são permitidos em cada
 * contexto/parentType. A chave `root` representa o documento (nível raiz).
 *
 * Esta estrutura é consultada pelo editor antes de permitir a criação
 * de um novo bloco. Ela não realiza alterações no AST — apenas responde
 * se a operação é permitida.
 */
export const RULES = {
  // Nível raiz do documento
  root: [
    BlockTypes.PREAMBLE || 'preamble',
    BlockTypes.TITLE || 'title',
    BlockTypes.ABSTRACT || 'abstract',
    BlockTypes.SECTION || 'section',
    BlockTypes.BIBLIOGRAPHY || 'bibliography'
  ].filter(Boolean),

  // Dentro de uma Section podemos criar subseções e blocos de conteúdo
  [BlockTypes.SECTION || 'section']: [
    BlockTypes.SUBSECTION || 'subsection',
    BlockTypes.PARAGRAPH || 'paragraph',
    BlockTypes.FIGURE || 'figure',
    BlockTypes.TABLE || 'table',
    BlockTypes.EQUATION || 'equation',
    BlockTypes.PAGEBREAK || 'pagebreak',
    BlockTypes.CITATION || 'citation',
    BlockTypes.LIST || 'list'
  ].filter(Boolean),

  // Dentro de uma Subsection apenas conteúdo (não novas Sections)
  [BlockTypes.SUBSECTION || 'subsection']: [
    BlockTypes.PARAGRAPH || 'paragraph',
    BlockTypes.FIGURE || 'figure',
    BlockTypes.TABLE || 'table',
    BlockTypes.EQUATION || 'equation',
    BlockTypes.PAGEBREAK || 'pagebreak',
    BlockTypes.CITATION || 'citation',
    BlockTypes.LIST || 'list'
  ].filter(Boolean),

  // Figuras, equações e parágrafos não aceitam filhos por padrão
  [BlockTypes.FIGURE || 'figure']: [],
  [BlockTypes.EQUATION || 'equation']: [],
  [BlockTypes.PARAGRAPH || 'paragraph']: [],

  // Bibliografia só pode existir no root ou no final do documento; aqui
  // permitimos que a bibliografia exista no root, mas não que receba
  // filhos editáveis via inserção direta.
  [BlockTypes.BIBLIOGRAPHY || 'bibliography']: []
};

/**
 * Retorna os tipos de blocos permitidos como filhos de `parentType`.
 * Se `parentType` for falsy (null/undefined), considera-se o nível `root`.
 *
 * @param {string|undefined|null} parentType
 * @returns {string[]} lista de tipos permitidos (pode ser vazia)
 */
export function allowedChildTypes(parentType) {
  const key = parentType || 'root';
  // Se RULES não tiver a chave, retorna array vazio para indicar que
  // não é permitido inserir filhos nesse contexto.
  return RULES[key] ? Array.from(RULES[key]) : [];
}

/**
 * Verifica se é permitido criar `childType` dentro do contexto `parentType`.
 * Não modifica o AST — apenas consulta as regras.
 *
 * @param {string} childType
 * @param {string|undefined|null} parentType
 * @returns {boolean}
 */
export function canCreate(childType, parentType) {
  const allowed = allowedChildTypes(parentType);
  return allowed.includes(childType);
}

/**
 * Úteis para depuração/integração: retorna um mapa simplificado das regras.
 * Não necessário para a validação, mas expõe as regras para outros módulos
 * que queiram apresentar mensagens ou gerar menus dinâmicos.
 */
export function getRules() {
  return RULES;
}

export default {
  RULES,
  allowedChildTypes,
  canCreate,
  getRules
};
