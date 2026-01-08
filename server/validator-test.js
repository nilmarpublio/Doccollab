// DocCollab-v0
// AST é a única fonte de verdade.
// Nenhuma lógica fora do modelo semântico é permitida.

const { validate } = require('./lib/validator');

const validAst = {
  metadata: { id: 'v1' },
  content: [
    { type: 'title', text: 'Título' },
    { type: 'abstract', text: 'Resumo' },
    { type: 'section', title: 'Intro', content: [ { type: 'paragraph', text: 'P' }, { type: 'equation', latex: 'E=mc^2' } ] },
    { type: 'bibliography', entries: [ { id: 'ref1', text: 'X' } ] },
    { type: 'paragraph', type: 'citation', ref: 'ref1' }
  ]
};

const invalidAst = {
  metadata: { id: 'i1' },
  content: [
    { type: 'abstract', text: 'Resumo depois' },
    { type: 'title', text: 'Titulo1' },
    { type: 'title', text: 'Titulo2' },
    { type: 'subsection', title: 'Sub sem section' },
    { type: 'equation', latex: 'x=1' },
    { type: 'bibliography', entries: [ { id: 'r1', text: 'A' } ] }
  ]
};

console.log('Valid AST ->', validate(validAst));
console.log('Invalid AST ->', validate(invalidAst));
