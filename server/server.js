// DocCollab-v0
// AST é a única fonte de verdade.
// Nenhuma lógica fora do modelo semântico é permitida.

// server/server.js — small HTTP API to compile and render resources
const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');
// prefer CommonJS copies (.cjs) for compatibility with package.json "type": "module"
const { generateLaTeX } = require('./lib/latex-generator.cjs');
const { generateBib } = require('./lib/bib-generator.cjs');
const { compileTex } = require('./lib/compiler.cjs');

const PORT = process.env.PORT || 3000;
const TMP = path.join(__dirname, 'tmp');
if (!fs.existsSync(TMP)) fs.mkdirSync(TMP, { recursive: true });
const LOGS_DIR = path.join(__dirname, 'logs');
if (!fs.existsSync(LOGS_DIR)) fs.mkdirSync(LOGS_DIR, { recursive: true });
const CLIENT_LOG = path.join(LOGS_DIR, 'client.log');

function readRequestBody(req) {
  return new Promise((resolve, reject) => {
    let buf = '';
    req.on('data', d => buf += d.toString());
    req.on('end', () => resolve(buf));
    req.on('error', reject);
  });
}

function jsonResponse(res, obj, code=200) {
  res.writeHead(code, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(obj));
}

const server = http.createServer(async (req, res) => {
  try {
    // quick static file server for preview (serve workspace files)
    const publicRoot = path.join(__dirname, '..');
    const urlPath = decodeURIComponent(req.url.split('?')[0]);
    const tryPath = urlPath === '/' ? '/index.html' : urlPath;
    const fsPath = path.normalize(path.join(publicRoot, tryPath.replace(/^\//, '')));
    if (fsPath.startsWith(publicRoot) && fs.existsSync(fsPath) && req.method === 'GET') {
      const ext = path.extname(fsPath).toLowerCase();
      const mime = ({'.html':'text/html','.css':'text/css','.js':'application/javascript','.json':'application/json','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.pdf':'application/pdf'}[ext]) || 'application/octet-stream';
      res.writeHead(200, { 'Content-Type': mime });
      fs.createReadStream(fsPath).pipe(res);
      return;
    }

    if (req.method === 'GET' && req.url === '/api/health') {
      return jsonResponse(res, { ok: true, version: '0.1' });
    }

    if (req.method === 'POST' && req.url === '/api/render-tex') {
      const body = await readRequestBody(req);
      const j = JSON.parse(body || '{}');
      const ast = j.ast || {};
      const tex = generateLaTeX(ast, null);
      return jsonResponse(res, { success: true, tex });
    }

    if (req.method === 'POST' && req.url === '/api/render-bib') {
      const body = await readRequestBody(req);
      const j = JSON.parse(body || '{}');
      const ast = j.ast || {};
      const bib = generateBib(ast);
      return jsonResponse(res, { success: true, bib });
    }

    if (req.method === 'POST' && req.url === '/api/client-log') {
      // Accept small JSON log entries from the client and persist them.
      try {
        const body = await readRequestBody(req);
        const entry = body && body.length ? body : '{}';
        const ts = new Date().toISOString();
        const ip = req.socket && req.socket.remoteAddress ? req.socket.remoteAddress : '';
        const record = { ts, ip, entry: JSON.parse(entry) };
        fs.appendFileSync(CLIENT_LOG, JSON.stringify(record) + '\n', 'utf8');
        return jsonResponse(res, { success: true });
      } catch (e) {
        // best-effort: if body isn't valid JSON, still append raw text
        try { fs.appendFileSync(CLIENT_LOG, JSON.stringify({ ts: new Date().toISOString(), ip: req.socket.remoteAddress, entry: String(e) }) + '\n', 'utf8'); } catch(_){}
        return jsonResponse(res, { success: false, error: e.message || String(e) });
      }
    }

    if (req.method === 'POST' && req.url === '/api/compile') {
      const body = await readRequestBody(req);
      const j = JSON.parse(body || '{}');
      const ast = j.ast || {};
      const tex = generateLaTeX(ast, null);
      const id = Date.now() + '-' + Math.floor(Math.random()*1000);
      const texPath = path.join(TMP, `doc-${id}.tex`);
      fs.writeFileSync(texPath, tex, 'utf8');
      const resCompile = await compileTex(texPath, { cwd: TMP, timeoutMs: 20000 });
      if (resCompile.success) {
        const pdfPath = resCompile.pdf;
        const pdfBin = fs.readFileSync(pdfPath);
        const b64 = pdfBin.toString('base64');
        return jsonResponse(res, { success: true, pdfBase64: b64 });
      }
      return jsonResponse(res, { success: false, error: resCompile.error || { message: 'compile failed' }, log: resCompile.log || '' });
    }

    // unknown
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'not found' }));
  } catch (e) {
    console.error('server error', e);
    jsonResponse(res, { error: e.message || String(e) }, 500);
  }
});

server.listen(PORT, () => console.log('DocCollab API listening on http://localhost:' + PORT));
