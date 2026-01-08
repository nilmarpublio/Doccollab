// DocCollab-v0
// AST é a única fonte de verdade.
// Nenhuma lógica fora do modelo semântico é permitida.

// server/server.cjs — small HTTP API to compile and render resources
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
        try { fs.appendFileSync(CLIENT_LOG, JSON.stringify({ ts: new Date().toISOString(), ip: req.socket.remoteAddress, entry: String(e) }) + '\n', 'utf8'); } catch(_){ }
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
// DocCollab-v0
// AST é a única fonte de verdade.
// Nenhuma lógica fora do modelo semântico é permitida.

// server/server.cjs — small HTTP API to compile and render resources
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
        try { fs.appendFileSync(CLIENT_LOG, JSON.stringify({ ts: new Date().toISOString(), ip: req.socket.remoteAddress, entry: String(e) }) + '\n', 'utf8'); } catch(_){ }
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
// DocCollab-v0 — CommonJS server entry
const http = require("http");
const fs = require("fs");
const path = require("path");
const os = require("os");
const { generateLaTeX } = require("./lib/latex-generator.cjs");
const { generateBib } = require("./lib/bib-generator.cjs");
const { compileTex } = require("./lib/compiler.cjs");

const PORT = process.env.PORT || 3000;
const TMP = path.join(__dirname, "tmp");
if (!fs.existsSync(TMP)) fs.mkdirSync(TMP, { recursive: true });
const USERS_FILE = path.join(TMP, "users.json");
const bcrypt = require("bcryptjs");
const LOGS_DIR = path.join(__dirname, "logs");
if (!fs.existsSync(LOGS_DIR)) fs.mkdirSync(LOGS_DIR, { recursive: true });
const CLIENT_LOG = path.join(LOGS_DIR, "client.log");

function readRequestBody(req) {
  return new Promise((resolve, reject) => {
    let buf = "";
    req.on("data", (d) => (buf += d.toString()));
    req.on("end", () => resolve(buf));
    req.on("error", reject);
  });
}

function jsonResponse(res, obj, code = 200) {
  res.writeHead(code, { "Content-Type": "application/json" });
  res.end(JSON.stringify(obj));
}

const server = http.createServer(async (req, res) => {
  try {
    const publicRoot = path.join(__dirname, "..");
    const urlPath = decodeURIComponent(req.url.split("?")[0]);
    const tryPath = urlPath === "/" ? "/index.html" : urlPath;
    const fsPath = path.normalize(
      path.join(publicRoot, tryPath.replace(/^\//, ""))
    );
    if (
      fsPath.startsWith(publicRoot) &&
      fs.existsSync(fsPath) &&
      req.method === "GET"
    ) {
      const ext = path.extname(fsPath).toLowerCase();
      const mime =
        {
          ".html": "text/html",
          ".css": "text/css",
          ".js": "application/javascript",
          ".json": "application/json",
          ".png": "image/png",
          ".jpg": "image/jpeg",
          ".jpeg": "image/jpeg",
          ".pdf": "application/pdf",
        }[ext] || "application/octet-stream";
      const headers = { "Content-Type": mime };
      if (ext === ".js" || ext === ".html" || ext === ".css") {
        headers["Cache-Control"] = "no-cache, no-store, must-revalidate";
        headers["Pragma"] = "no-cache";
        headers["Expires"] = "0";
      }
      res.writeHead(200, headers);
      fs.createReadStream(fsPath).pipe(res);
      return;
    }

    if (req.method === "GET" && req.url === "/api/health") {
      return jsonResponse(res, { ok: true, version: "0.1" });
    }

    if (req.method === "POST" && req.url === "/api/render-tex") {
      const body = await readRequestBody(req);
      const j = JSON.parse(body || "{}");
      const ast = j.ast || {};
      const tex = generateLaTeX(ast, null);
      return jsonResponse(res, { success: true, tex });
    }

    // Signup endpoint - persists users in server/tmp/users.json (prototype)
    if (req.method === "POST" && req.url === "/api/signup") {
      try {
        const body = await readRequestBody(req);
        const j = JSON.parse(body || "{}");
        const name = (j.name || "").trim();
        const email = (j.email || "").trim().toLowerCase();
        const password = j.password || "";
        if (!email || !password)
          return jsonResponse(
            res,
            { success: false, error: "email and password required" },
            400
          );

        let users = [];
        try {
          users = JSON.parse(fs.readFileSync(USERS_FILE, "utf8") || "[]");
        } catch (_) {
          users = [];
        }
        if (users.find((u) => u.email === email))
          return jsonResponse(
            res,
            { success: false, error: "email_exists" },
            409
          );
        const saltRounds = 10;
        const hash = bcrypt.hashSync(password, saltRounds);
        const user = {
          id: Date.now() + "-" + Math.floor(Math.random() * 1000),
          name,
          email,
          passwordHash: hash,
          createdAt: new Date().toISOString(),
        };
        users.push(user);
        fs.writeFileSync(USERS_FILE, JSON.stringify(users, null, 2), "utf8");
        return jsonResponse(res, { success: true, userId: user.id });
      } catch (e) {
        console.error("signup error", e);
        return jsonResponse(
          res,
          { success: false, error: e.message || String(e) },
          500
        );
      }
    }

    // Login endpoint - checks credentials against users.json
    if (req.method === "POST" && req.url === "/api/login") {
      try {
        const body = await readRequestBody(req);
        const j = JSON.parse(body || "{}");
        const email = (j.email || "").trim().toLowerCase();
        const password = j.password || "";
        if (!email || !password)
          return jsonResponse(
            res,
            { success: false, error: "email and password required" },
            400
          );

        let users = [];
        try {
          users = JSON.parse(fs.readFileSync(USERS_FILE, "utf8") || "[]");
        } catch (_) {
          users = [];
        }
        const user = users.find((u) => u.email === email);
        if (!user)
          return jsonResponse(
            res,
            { success: false, error: "invalid_credentials" },
            401
          );
        const ok = bcrypt.compareSync(password, user.passwordHash || "");
        if (!ok)
          return jsonResponse(
            res,
            { success: false, error: "invalid_credentials" },
            401
          );
        // Simulate session token (do not use in production)
        const token = Buffer.from(user.id + "|" + Date.now()).toString(
          "base64"
        );
        return jsonResponse(res, {
          success: true,
          userId: user.id,
          token,
          name: user.name,
        });
      } catch (e) {
        console.error("login error", e);
        return jsonResponse(
          res,
          { success: false, error: e.message || String(e) },
          500
        );
      }
    }

    if (req.method === "POST" && req.url === "/api/render-bib") {
      const body = await readRequestBody(req);
      const j = JSON.parse(body || "{}");
      const ast = j.ast || {};
      const bib = generateBib(ast);
      return jsonResponse(res, { success: true, bib });
    }

    if (req.method === "POST" && req.url === "/api/compile") {
      try {
        const body = await readRequestBody(req);
        console.log("Received compile request, body length:", body.length);
        const j = JSON.parse(body || "{}");
        console.log("AST blocks count:", j.ast?.blocks?.length || 0);
        const ast = j.ast || {};
        const tex = generateLaTeX(ast, null);
        console.log("Generated LaTeX, length:", tex.length);
        const id = Date.now() + "-" + Math.floor(Math.random() * 1000);
        const texPath = path.join(TMP, `doc-${id}.tex`);
        fs.writeFileSync(texPath, tex, "utf8");
        const resCompile = await compileTex(texPath, {
          cwd: TMP,
          timeoutMs: 20000,
        });
        if (resCompile.success) {
          const pdfPath = resCompile.pdf;
          if (!pdfPath || !fs.existsSync(pdfPath)) {
            return jsonResponse(res, {
              success: false,
              error: { message: "PDF esperado não foi gerado" },
              log: resCompile.log || "",
            });
          }
          const pdfBin = fs.readFileSync(pdfPath);
          const b64 = pdfBin.toString("base64");
          return jsonResponse(res, { success: true, pdfBase64: b64 });
        }
        return jsonResponse(res, {
          success: false,
          error: resCompile.error || { message: "compile failed" },
          log: resCompile.log || "",
        });
      } catch (parseErr) {
        console.error("Compile request error:", parseErr);
        return jsonResponse(
          res,
          {
            success: false,
            error: { message: parseErr.message || String(parseErr) },
          },
          400
        );
      }
    }

    if (req.method === "POST" && req.url === "/api/client-log") {
      try {
        const body = await readRequestBody(req);
        const entry = body && body.length ? body : "{}";
        const ts = new Date().toISOString();
        const ip =
          req.socket && req.socket.remoteAddress
            ? req.socket.remoteAddress
            : "";
        const record = { ts, ip, entry: JSON.parse(entry) };
        fs.appendFileSync(CLIENT_LOG, JSON.stringify(record) + "\n", "utf8");
        return jsonResponse(res, { success: true });
      } catch (e) {
        try {
          fs.appendFileSync(
            CLIENT_LOG,
            JSON.stringify({
              ts: new Date().toISOString(),
              ip: req.socket.remoteAddress,
              entry: String(e),
            }) + "\n",
            "utf8"
          );
        } catch (_) {}
        return jsonResponse(res, {
          success: false,
          error: e.message || String(e),
        });
      }
    }

    res.writeHead(404, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ error: "not found" }));
  } catch (e) {
    console.error("server error", e);
    jsonResponse(res, { error: e.message || String(e) }, 500);
  }
});

server.listen(PORT, () =>
  console.log("DocCollab API listening on http://localhost:" + PORT)
);
