const fs = require('fs');
const path = require('path');

const texPath = path.join(__dirname, 'tmp', 'mapped-error.tex');
if (!fs.existsSync(texPath)) { console.error('Missing tex file:', texPath); process.exit(2); }
const content = fs.readFileSync(texPath, 'utf8');

// replicate parseLogForErrorBlock heuristic for INVALID inside equation
const eqRegex = /%\s*DOCCOLLAB-BLOCK-ID:\s*(\S+)\s*[\s\S]*?\\begin\{equation\}([\s\S]*?)\\end\{equation\}/g;
let m; let found = null;
while ((m = eqRegex.exec(content)) !== null) {
  const bid = m[1];
  const body = m[2];
  if (/INVALID/.test(body)) { found = bid; break; }
}

if (found) { console.log('OK: mapped to blockId', found); process.exit(0); }
console.error('FAIL: no mapping found'); process.exit(3);
