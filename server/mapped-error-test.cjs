const fs = require('fs');
const path = require('path');
const { compileTex } = require('./lib/compiler.cjs');

// Create a temporary tex with a marked block containing INVALID to trigger mapping
const tex = `\\documentclass{article}
\\begin{document}
% DOCCOLLAB-BLOCK-ID: test_eq
\\begin{equation}
INVALID_MARKER_INVALID
\\end{equation}
\\end{document}
`;
const tmpDir = path.join(__dirname, 'tmp');
if (!fs.existsSync(tmpDir)) fs.mkdirSync(tmpDir);
const texPath = path.join(tmpDir, 'mapped-error.tex');
fs.writeFileSync(texPath, tex, 'utf8');

(async ()=>{
  console.log('Running mapped-error test on', texPath);
  const res = await compileTex(texPath, { cwd: tmpDir, timeoutMs: 5000 });
  console.log('Compile result:', res);
  if(res && res.success===false && res.error && res.error.blockId){
    console.log('Mapped blockId:', res.error.blockId);
    process.exit(0);
  } else {
    console.error('Mapping failed or no error returned');
    process.exit(2);
  }
})();
