// DocCollab-v0
// AST é a única fonte de verdade.
// Nenhuma lógica fora do modelo semântico é permitida.

const fs = require('fs');
const path = require('path');
const { generateLaTeX } = require('./lib/latex-generator');

const astPath = path.join(__dirname, 'examples', 'simple-ast.json');
const outPath = path.join(__dirname, 'examples', 'generated-by-latex-generator.tex');
const ast = JSON.parse(fs.readFileSync(astPath, 'utf8'));
const tex = generateLaTeX(ast, { packages: ['amsmath','graphicx','hyperref'] });
fs.writeFileSync(outPath, tex, 'utf8');
console.log('Gerado:', outPath);
