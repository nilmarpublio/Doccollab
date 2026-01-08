// DocCollab-v0
// AST é a única fonte de verdade.
// Nenhuma lógica fora do modelo semântico é permitida.

const http = require('http');
const fs = require('fs');
const path = require('path');
const data = JSON.parse(fs.readFileSync(path.join(__dirname,'examples','simple-ast.json'),'utf8'));
const body = JSON.stringify({ ast: data });
const opts = { hostname: 'localhost', port: 3000, path: '/api/compile', method: 'POST', headers: { 'Content-Type':'application/json', 'Content-Length': Buffer.byteLength(body) } };
const req = http.request(opts, (res) => {
  let out = '';
  res.setEncoding('utf8');
  res.on('data', d => out += d);
  res.on('end', ()=>{
    try{ const j = JSON.parse(out); console.log('API response:', j.success ? 'success' : 'failure'); if(j.success) console.log('PDF base64 length:', (j.pdfBase64||'').length); else console.log('error', j.error);
    } catch(e){ console.log('Invalid JSON', out); }
  });
});
req.on('error', e => console.error('request error', e));
req.write(body); req.end();
