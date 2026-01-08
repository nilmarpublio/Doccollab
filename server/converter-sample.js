// DocCollab-v0
// AST é a única fonte de verdade.
// Nenhuma lógica fora do modelo semântico é permitida.

const fs = require('fs');
const path = require('path');
const { convert } = require('./lib/converter');

const inputPath = path.join(__dirname, 'examples', 'simple-ast.json');
const outPath = path.join(__dirname, 'examples', 'out.tex');

const ast = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
const tex = convert(ast);
fs.writeFileSync(outPath, tex, 'utf8');
console.log('Gerado:', outPath);
