// DocCollab-v0
// AST é a única fonte de verdade.
// Nenhuma lógica fora do modelo semântico é permitida.

const { validateDocument, attachParents } = require('./validators');

const validDoc = {
  type: 'document',
  metadata: { title: 'Válido', bibliography: ['knuth1984'] },
  content: [
    { type: 'title', text: 'Válido' },
    { type: 'abstract', content: [ { type: 'paragraph', text: 'Resumo.' } ] },
    { type: 'section', title: 'Intro', content: [ { type: 'equation', latex: 'E=mc^2', numbered:true }, { type:'paragraph', text:'Texto' }, { type:'citation', key:'knuth1984' } ] }
  ]
};

const invalidDoc = {
  type: 'document',
  metadata: { title: 'Inválido', bibliography: ['unused2010'] },
  content: [
    { type: 'title', text: 'Inválido' },
    { type: 'section', title: 'Primeira', content: [] },
    { type: 'abstract', content: [ { type: 'paragraph', text: 'Resumo fora de lugar.' } ] },
    { type: 'subsection', title: 'Sem seção pai', content: [] },
    { type: 'equation', latex: 'a+b', numbered:false }
  ]
};

function runSample(doc, name){
  // attach parent pointers to allow ancestor checks
  const docWithParents = attachParents(doc);
  const res = validateDocument(docWithParents);
  console.log('===',name,'===');
  if(res.errors.length===0 && res.warnings.length===0) console.log('Sem erros ou avisos.');
  if(res.errors.length>0){
    console.log('Erros:');
    console.dir(res.errors,{depth:null});
  }
  if(res.warnings.length>0){
    console.log('Avisos:');
    console.dir(res.warnings,{depth:null});
  }
}

runSample(validDoc,'Documento Válido');
console.log('\n');
runSample(invalidDoc,'Documento Inválido');
