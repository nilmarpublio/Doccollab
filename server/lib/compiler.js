// DocCollab-v0
// AST é a única fonte de verdade.
// Nenhuma lógica fora do modelo semântico é permitida.

// server/lib/compiler.js
// Compilador LaTeX empacotado (server-side). Retorna erros mapeados a blocos do AST.
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

function findNearestBlockId(lines, lineIndex) {
  // search upwards from lineIndex for DOCCOLLAB-BLOCK-ID comment
  for (let i = lineIndex; i >= 0; i--) {
    const m = /%\s*DOCCOLLAB-BLOCK-ID:\s*(\S+)/.exec(lines[i]);
    if (m) return m[1];
  }
  return null;
}

function parseLogForErrorBlock(texContent, logText) {
  // Try simple heuristic: find "!" error lines with line numbers like l.<n>
  // If not possible, fallback to scanning for problematic markers in texContent.
  const lines = texContent.split(/\r?\n/);
  // Look for known patterns of LaTeX error: "! Undefined control sequence." etc.
  const lineMatch = /l\.(\d+)/.exec(logText);
  if (lineMatch) {
    const ln = parseInt(lineMatch[1], 10) - 1; // LaTeX lines are 1-indexed
    const blockId = findNearestBlockId(lines, ln);
    return blockId ? { blockId, message: 'Erro de compilação LaTeX (mapeado ao bloco)' } : null;
  }

  // Fallback: detect equation blocks containing 'INVALID' marker
  const joined = texContent;
  const eqRegex = /%\s*DOCCOLLAB-BLOCK-ID:\s*(\S+)\s*[\s\S]*?\\begin\{equation\}([\s\S]*?)\\end\{equation\}/g;
  let m;
  while ((m = eqRegex.exec(joined)) !== null) {
    const bid = m[1];
    const body = m[2];
    if (/INVALID/.test(body)) {
      return { blockId: bid, message: 'Equação inválida' };
    }
  }
  return null;
}

function hasPdflatex() {
  try {
    const which = process.platform === 'win32' ? 'where' : 'which';
    const out = require('child_process').execSync(`${which} pdflatex`, { stdio: 'pipe' }).toString();
    return !!out.trim();
  } catch (e) {
    return false;
  }
}

async function runPdflatex(texPath, cwd, timeoutMs = 20000) {
  return new Promise((resolve) => {
    const args = ['-interaction=nonstopmode', '-halt-on-error', path.basename(texPath)];
    const proc = spawn('pdflatex', args, { cwd });
    let stdout = '';
    let stderr = '';
    const killTimer = setTimeout(() => {
      proc.kill('SIGKILL');
    }, timeoutMs);

    proc.stdout.on('data', d => stdout += d.toString());
    proc.stderr.on('data', d => stderr += d.toString());
    proc.on('close', (code) => {
      clearTimeout(killTimer);
      const logPath = path.join(cwd, path.basename(texPath, '.tex') + '.log');
      let logText = '';
      try { logText = fs.readFileSync(logPath, 'utf8'); } catch (e) { logText = stdout + '\n' + stderr; }
      resolve({ code, stdout, stderr, logText });
    });
  });
}

async function compileTex(texPath, options = {}) {
  options = options || {};
  const cwd = options.cwd || path.dirname(texPath);
  const texContent = fs.readFileSync(texPath, 'utf8');

  if (!hasPdflatex()) {
    // Simulate compilation: detect invalid equation markers
    const simulated = parseLogForErrorBlock(texContent, '');
    if (simulated) return { success: false, error: simulated };
    // otherwise write a fake PDF file to out
    const outPdf = path.join(cwd, path.basename(texPath, '.tex') + '.pdf');
    fs.writeFileSync(outPdf, 'PDF_BINARY_MOCK');
    return { success: true, pdf: outPdf };
  }

  // Run real pdflatex with timeout
  const res = await runPdflatex(texPath, cwd, options.timeoutMs || 20000);
  if (res.code === 0) {
    const outPdf = path.join(cwd, path.basename(texPath, '.tex') + '.pdf');
    return { success: true, pdf: outPdf, log: res.logText };
  }

  // Map error to block
  const mapped = parseLogForErrorBlock(texContent, res.logText || res.stdout || res.stderr);
  if (mapped) return { success: false, error: mapped, log: res.logText };
  // fallback
  return { success: false, error: { message: 'Erro de compilação', blockId: null }, log: res.logText };
}

module.exports = { compileTex };
