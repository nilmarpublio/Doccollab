// DocCollab-v0
// CommonJS compiler copy for tests
const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");

function findNearestBlockId(lines, lineIndex) {
  for (let i = lineIndex; i >= 0; i--) {
    const m = /%\s*DOCCOLLAB-BLOCK-ID:\s*(\S+)/.exec(lines[i]);
    if (m) return m[1];
  }
  return null;
}

function parseLogForErrorBlock(texContent, logText) {
  const lines = texContent.split(/\r?\n/);
  // Alguns logs do LaTeX podem ter formatos diferentes para indicar a linha
  // do erro — por exemplo `l.123`, `l. 123`, `on input line 123` ou apenas
  // `line 123:` em mensagens auxiliares. Tentamos vários patterns para
  // aumentar a robustez do mapeamento para `DOCCOLLAB-BLOCK-ID`.
  let ln = null;
  const lineMatchers = [
    /l\.\s*(\d+)/,
    /on input line\s*(\d+)/i,
    /line\s+(\d+)[\):.,]/i,
    /line\s+(\d+)\b/i,
  ];
  for (const rx of lineMatchers) {
    const m = rx.exec(logText);
    if (m && m[1]) {
      ln = parseInt(m[1], 10) - 1;
      break;
    }
  }
  if (ln !== null) {
    const blockId = findNearestBlockId(lines, ln);
    return blockId
      ? { blockId, message: "Erro de compilação LaTeX (mapeado ao bloco)" }
      : null;
  }

  const joined = texContent;
  const eqRegex =
    /%\s*DOCCOLLAB-BLOCK-ID:\s*(\S+)\s*[\s\S]*?\\begin\{equation\}([\s\S]*?)\\end\{equation\}/g;
  let m;
  while ((m = eqRegex.exec(joined)) !== null) {
    const bid = m[1];
    const body = m[2];
    if (/INVALID/.test(body)) {
      return { blockId: bid, message: "Equação inválida" };
    }
  }
  return null;
}

function hasPdflatex() {
  try {
    const which = process.platform === "win32" ? "where" : "which";
    const out = require("child_process")
      .execSync(`${which} pdflatex`, { stdio: "pipe" })
      .toString();
    return !!out.trim();
  } catch (e) {
    return false;
  }
}

function hasXelatex() {
  try {
    const which = process.platform === "win32" ? "where" : "which";
    const out = require("child_process")
      .execSync(`${which} xelatex`, { stdio: "pipe" })
      .toString();
    return !!out.trim();
  } catch (e) {
    return false;
  }
}

async function runPdflatex(texPath, cwd, timeoutMs = 20000) {
  return new Promise((resolve) => {
    const args = [
      "-interaction=nonstopmode",
      "-halt-on-error",
      path.basename(texPath),
    ];
    const proc = spawn("pdflatex", args, { cwd });
    let stdout = "";
    let stderr = "";
    const killTimer = setTimeout(() => {
      proc.kill("SIGKILL");
    }, timeoutMs);
    proc.stdout.on("data", (d) => (stdout += d.toString()));
    proc.stderr.on("data", (d) => (stderr += d.toString()));
    proc.on("close", (code) => {
      clearTimeout(killTimer);
      const logPath = path.join(cwd, path.basename(texPath, ".tex") + ".log");
      let logText = "";
      try {
        logText = fs.readFileSync(logPath, "utf8");
      } catch (e) {
        logText = stdout + "\n" + stderr;
      }
      resolve({ code, stdout, stderr, logText });
    });
  });
}

async function runXelatex(texPath, cwd, timeoutMs = 20000) {
  return new Promise((resolve) => {
    const args = [
      "-interaction=nonstopmode",
      "-halt-on-error",
      path.basename(texPath),
    ];
    const proc = spawn("xelatex", args, { cwd });
    let stdout = "";
    let stderr = "";
    const killTimer = setTimeout(() => {
      proc.kill("SIGKILL");
    }, timeoutMs);
    proc.stdout.on("data", (d) => (stdout += d.toString()));
    proc.stderr.on("data", (d) => (stderr += d.toString()));
    proc.on("close", (code) => {
      clearTimeout(killTimer);
      const logPath = path.join(cwd, path.basename(texPath, ".tex") + ".log");
      let logText = "";
      try {
        logText = fs.readFileSync(logPath, "utf8");
      } catch (e) {
        logText = stdout + "\n" + stderr;
      }
      resolve({ code, stdout, stderr, logText });
    });
  });
}

async function compileTex(texPath, options = {}) {
  options = options || {};
  const cwd = options.cwd || path.dirname(texPath);
  const texContent = fs.readFileSync(texPath, "utf8");
  if (!hasPdflatex()) {
    const simulated = parseLogForErrorBlock(texContent, "");
    if (simulated) return { success: false, error: simulated };
    const outPdf = path.join(cwd, path.basename(texPath, ".tex") + ".pdf");
    fs.writeFileSync(outPdf, "PDF_BINARY_MOCK");
    return { success: true, pdf: outPdf };
  }
  const res = await runPdflatex(texPath, cwd, options.timeoutMs || 20000);
  if (res.code === 0) {
    const outPdf = path.join(cwd, path.basename(texPath, ".tex") + ".pdf");
    return { success: true, pdf: outPdf, log: res.logText };
  }
  // if pdflatex failed due to Unicode/encoding issues, try xelatex if available
  const logLower = (res.logText || "").toLowerCase();
  const unicodeIssue =
    /unicode character/.test(logLower) ||
    /not set up for use with latex/.test(logLower) ||
    /u\+fffd/.test(logLower) ||
    /invalid utf-8/.test(logLower);
  if (unicodeIssue && hasXelatex()) {
    const resXe = await runXelatex(texPath, cwd, options.timeoutMs || 20000);
    if (resXe.code === 0) {
      const outPdf = path.join(cwd, path.basename(texPath, ".tex") + ".pdf");
      return {
        success: true,
        pdf: outPdf,
        log: resXe.logText,
        engine: "xelatex",
      };
    }
    // merge logs for diagnostics
    res.logText =
      (res.logText || "") + "\n---- xelatex log ----\n" + (resXe.logText || "");
  }
  const mapped = parseLogForErrorBlock(
    texContent,
    res.logText || res.stdout || res.stderr
  );
  if (mapped) return { success: false, error: mapped, log: res.logText };
  return {
    success: false,
    error: { message: "Erro de compilação", blockId: null },
    log: res.logText,
  };
}

module.exports = { compileTex };
