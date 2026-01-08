// DocCollab-v0
// AST é a única fonte de verdade.
// Nenhuma lógica fora do modelo semântico é permitida.

const path = require('path');
const fs = require('fs');
const { compileTex } = require('./lib/compiler');

(async ()=>{
  const texPath = path.join(__dirname, 'examples', 'generated-by-latex-generator.tex');
  console.log('Using', texPath);
  const res = await compileTex(texPath, { timeoutMs: 10000 });
  console.log('Result:', res);
})();
