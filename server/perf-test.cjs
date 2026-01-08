// DocCollab-v0
// Simple performance test: validate + generateLaTeX on a large synthetic AST
const fs = require('fs');
const path = require('path');
const { validate } = require('./lib/validator.cjs');
const { generateLaTeX } = require('./lib/latex-generator.cjs');

function hrMs(ns){ return Number(ns) / 1_000_000; }

function buildLargeAST(sample, targetBlocks){
  // clone sample and repeat a paragraph block many times under a section
  const doc = JSON.parse(JSON.stringify(sample));
  // ensure there's a section
  let section = doc.content.find(c=>c.type==='section');
  if(!section){ section = { id:'s_perf', type:'section', title:'Perf Section', content:[] }; doc.content.push(section); }
  // create N paragraph blocks
  const basePara = { id: 'p_perf', type: 'paragraph', text: 'Lorem ipsum dolor sit amet.' };
  for(let i=0;i<targetBlocks;i++){
    const p = JSON.parse(JSON.stringify(basePara)); p.id = 'p_perf_' + i; p.text = `Paragraph ${i} — ` + p.text;
    section.content.push(p);
  }
  return doc;
}

async function run(){
  const sample = JSON.parse(fs.readFileSync(path.join(__dirname,'examples','simple-ast.json'),'utf8'));
  const sizes = [100, 1000, 5000];
  console.log('Perf test starting — validator + generator');
  for(const n of sizes){
    const ast = buildLargeAST(sample, n);
    // validate
    const t0 = process.hrtime.bigint();
    const res = validate(ast);
    const t1 = process.hrtime.bigint();
    const valMs = hrMs(t1 - t0);

    // generate tex
    const g0 = process.hrtime.bigint();
    const tex = generateLaTeX(ast, { packages: ['amsmath','graphicx'] });
    const g1 = process.hrtime.bigint();
    const genMs = hrMs(g1 - g0);

    console.log(`
Size: ${n} paragraphs
  Validation: ${res.errors.length} errors, ${valMs.toFixed(2)} ms
  Generate .tex: ${(tex.length/1024).toFixed(1)} KB, ${genMs.toFixed(2)} ms
`);
  }
  console.log('Perf test completed');
}

run().catch(e=>{ console.error('Perf test failed', e); process.exit(2); });
