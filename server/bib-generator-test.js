// DocCollab-v0
// AST é a única fonte de verdade.
// Nenhuma lógica fora do modelo semântico é permitida.

const fs = require('fs');
const path = require('path');
const { generateBib } = require('./lib/bib-generator');
const ast = JSON.parse(fs.readFileSync(path.join(__dirname,'examples','simple-ast.json'), 'utf8'));
const out = generateBib(ast);
fs.writeFileSync(path.join(__dirname,'examples','out.bib'), out, 'utf8');
console.log('Gerado:', path.join(__dirname,'examples','out.bib'));
