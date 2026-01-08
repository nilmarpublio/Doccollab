import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// usar o validador frontend (ES module)
import { validateAST } from '../assets/js/core/validator.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function loadExample(name){
  const p = path.join(__dirname, 'examples', name);
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

function run(){
  console.log('AST Sanity Test — iniciando');
  const good = loadExample('simple-ast.json');
  const r1 = validateAST(good);
  console.log('Test 1: AST válido — erros encontrados:', r1.errors.length);
  if(r1.errors.length) console.log(JSON.stringify(r1.errors, null, 2));

  // Caso 2: documento sem title
  const bad1 = JSON.parse(JSON.stringify(good));
  // remover título
  bad1.content = bad1.content.filter(c => c.type !== 'title');
  const r2 = validateAST(bad1);
  console.log('Test 2: sem título — erros encontrados:', r2.errors.length);
  console.log(r2.errors.map(e=>e.code).join(', '));

  // Caso 3: subsection fora de section
  const bad2 = JSON.parse(JSON.stringify(good));
  // inserir uma subsection no root
  bad2.content.push({ id: 'ss1', type: 'subsection', title: 'Sub fora' });
  const r3 = validateAST(bad2);
  console.log('Test 3: subsection fora de section — erros encontrados:', r3.errors.length);
  console.log(r3.errors.map(e=>e.code).join(', '));

  // Caso 4: equação fora de section
  const bad3 = JSON.parse(JSON.stringify(good));
  bad3.content.push({ id: 'eq_out', type: 'equation', latex: 'x=1' });
  const r4 = validateAST(bad3);
  console.log('Test 4: equation fora de section — erros encontrados:', r4.errors.length);
  console.log(r4.errors.map(e=>e.code).join(', '));

  console.log('AST Sanity Test — concluído');
}

run();
