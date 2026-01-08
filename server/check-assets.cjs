// Simple asset checker: encontra imports em assets/js e faz GET para o servidor
const fs = require('fs');
const path = require('path');
const http = require('http');

const ROOT = path.join(__dirname, '..');
const ASSETS = path.join(ROOT, 'assets', 'js');
function walk(dir, files=[]) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const e of entries) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, files);
    else if (e.isFile() && p.endsWith('.js')) files.push(p);
  }
  return files;
}

function extractImports(content){
  const re = /import\s+(?:[^'";]+from\s+)?['"]([^'"]+)['"]/g;
  const out = [];
  let m; while((m = re.exec(content))){ out.push(m[1]); }
  return out;
}

function resolveImport(filePath, imp){
  if(imp.startsWith('http') || imp.startsWith('/')) return imp.startsWith('/')? imp : imp;
  // compute relative to file's directory and map to server path (strip workspace root)
  const dir = path.dirname(filePath);
  const abs = path.normalize(path.join(dir, imp));
  // convert to web path relative to workspace root
  const rel = path.relative(ROOT, abs).split(path.sep).join('/');
  return '/' + rel;
}

function checkUrl(url){
  return new Promise((resolve)=>{
    const opts = { hostname: '127.0.0.1', port: 3000, path: url, method: 'GET' };
    const req = http.request(opts, (res)=>{ resolve({ url, status: res.statusCode }); res.resume(); });
    req.on('error', (e)=> resolve({ url, error: e.message }));
    req.end();
  });
}

(async function(){
  const files = walk(ASSETS);
  const imports = {};
  for(const f of files){
    const c = fs.readFileSync(f,'utf8');
    const imps = extractImports(c);
    for(const i of imps){
      const url = resolveImport(f, i);
      imports[url] = imports[url] || new Set();
      imports[url].add(path.relative(ROOT, f));
    }
  }

  const results = [];
  for(const url of Object.keys(imports)){
    const r = await checkUrl(url);
    results.push({ url, from: Array.from(imports[url]).slice(0,5), status: r.status, error: r.error });
  }

  console.log('Asset check results:');
  for(const r of results){
    console.log(r.status? r.status : 'ERR', r.url, r.error? 'err:'+r.error : '', 'used by', r.from.join(', '));
  }
})();
