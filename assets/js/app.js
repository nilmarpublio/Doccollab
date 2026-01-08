import {
  mountEditor,
  getAST,
} from "./editor/editor-controller.js?v=20260102-999";
// sample AST será carregado dinamicamente via fetch (import de JSON direto quebra em alguns browsers)
async function loadSample() {
  try {
    console.debug("Fetching sample AST from server/examples/simple-ast.json");
    const res = await fetch("server/examples/simple-ast.json");
    console.debug("Fetch response:", res.status, res.statusText);
    if (!res.ok) throw new Error("fetch sample failed: " + res.status);
    const data = await res.json();
    console.debug("Sample AST parsed successfully:", data);
    return data;
  } catch (e) {
    console.error("failed to load sample AST", e);
    // fallback AST minimalista mas válido
    return {
      metadata: {
        id: "fallback-doc",
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      },
      blocks: [
        { type: "title", id: "title_1", text: "Novo Documento" },
        { type: "author", id: "author_1", text: "Autor" },
        {
          type: "section",
          id: "sec_1",
          title: "Introdução",
          content: [{ type: "paragraph", id: "p_1", text: "Escreva aqui..." }],
        },
      ],
    };
  }
}
import { mountPreview } from "./editor/preview.js";
import { createToolbar } from "./editor/toolbar.js";
import {
  initAutosave,
  listDocuments,
  getLatestDocument,
} from "./storage/indexeddb.js";
import { generateLaTeX } from "./core/latex-generator.js";
import { loadLocale, translateDOM } from "./i18n.js";

const SUPPORTED_LOCALES = ["pt-BR", "en-US", "es-ES"];

async function chooseLocale() {
  const saved = localStorage.getItem("doccollab:locale");
  const nav = navigator.language || navigator.userLanguage || "pt-BR";
  const candidate =
    saved || SUPPORTED_LOCALES.find((l) => nav.startsWith(l)) || "pt-BR";
  return SUPPORTED_LOCALES.includes(candidate) ? candidate : "pt-BR";
}

async function buildToolbar(root, onLoadDoc, langContainer) {
  const toolbar = document.createElement("div");
  toolbar.className = "toolbar";

  const langSelect = document.createElement("select");
  langSelect.className = "lang-select";
  SUPPORTED_LOCALES.forEach((l) => {
    const o = document.createElement("option");
    o.value = l;
    o.textContent = l;
    langSelect.appendChild(o);
  });
  langSelect.value = await chooseLocale();
  langSelect.addEventListener("change", async () => {
    const newLoc = langSelect.value;
    localStorage.setItem("doccollab:locale", newLoc);
    await loadLocale(newLoc);
    try {
      translateDOM(document);
    } catch (e) {}
  });
  // if caller provided a container for language select, append there (above editor), else put inside toolbar
  if (langContainer && typeof langContainer.appendChild === "function")
    langContainer.appendChild(langSelect);
  else toolbar.appendChild(langSelect);

  const newBtn = document.createElement("button");
  newBtn.dataset.i18n = "action.newDocument";
  newBtn.className = "btn-new";
  newBtn.textContent = "Novo";
  newBtn.addEventListener("click", () => {
    // Generate unique ID for new document
    const newDocId = "doc-" + Date.now();
    // Store flag to create blank document
    sessionStorage.setItem("doccollab:new-blank", newDocId);
    // Reload page
    window.location.href = "app.html";
  });
  // if caller provided langContainer (inside btn_card), append the New button there
  if (langContainer && typeof langContainer.appendChild === "function")
    langContainer.appendChild(newBtn);
  else toolbar.appendChild(newBtn);

  const compileBtn = document.createElement("button");
  compileBtn.className = "btn-compile";
  compileBtn.textContent = "Compilar";
  compileBtn.addEventListener("click", () => {
    try {
      window.dispatchEvent(new Event("request:compile"));
    } catch (e) {}
  });
  // if caller provided langContainer (inside btn_card), append the Compile button there as well
  if (langContainer && typeof langContainer.appendChild === "function")
    langContainer.appendChild(compileBtn);
  else toolbar.appendChild(compileBtn);

  // sample button removed per user request

  const docsSelect = document.createElement("select");
  docsSelect.className = "docs-select";
  if (langContainer && typeof langContainer.appendChild === "function")
    langContainer.appendChild(docsSelect);
  else toolbar.appendChild(docsSelect);

  // NOTE: do not attach a direct load handler here; caller will attach it

  // populate docs
  try {
    const docs = await listDocuments();
    docsSelect.innerHTML = "";
    const emptyOpt = document.createElement("option");
    emptyOpt.value = "";
    emptyOpt.textContent = "--";
    docsSelect.appendChild(emptyOpt);
    for (const d of docs || []) {
      const o = document.createElement("option");
      o.value = d.docId;
      o.textContent = d.title || d.docId;
      docsSelect.appendChild(o);
    }
  } catch (e) {
    console.warn("failed to list docs", e);
  }

  // coloque a toolbar no topo do root para aparecer como barra de navegação
  if (root && typeof root.prepend === "function") root.prepend(toolbar);
  else root.appendChild(toolbar);
  try {
    translateDOM(toolbar);
  } catch (e) {}
  // also translate langContainer if present (we may have appended children there)
  try {
    if (langContainer && typeof langContainer === "object")
      translateDOM(langContainer);
  } catch (e) {}
  return { toolbar, docsSelect, langSelect, newBtn, compileBtn };
}

window.addEventListener("DOMContentLoaded", async () => {
  // helper to send logs to server (sendBeacon preferred, fallback to fetch keepalive)
  const sendClientLog = (obj) => {
    try {
      const payload = JSON.stringify(
        Object.assign(
          {
            ts: new Date().toISOString(),
            ua: (typeof navigator !== "undefined" && navigator.userAgent) || "",
            href: (typeof location !== "undefined" && location.href) || "",
          },
          obj
        )
      );
      if (typeof navigator !== "undefined" && navigator.sendBeacon) {
        try {
          navigator.sendBeacon("/api/client-log", payload);
          return true;
        } catch (e) {}
      }
      // fallback: fire-and-forget fetch with keepalive
      try {
        if (typeof fetch !== "undefined")
          fetch("/api/client-log", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: payload,
            keepalive: true,
          }).catch(() => {});
      } catch (e) {}
    } catch (e) {}
  };
  // buffered client-side logs: keep last N entries and send on beforeunload
  const CLIENT_LOG_BUFFER_LIMIT = 50;
  const clientLogBuffer = [];
  const pushToBuffer = (entry) => {
    try {
      clientLogBuffer.push(
        Object.assign({ ts: new Date().toISOString() }, entry)
      );
      while (clientLogBuffer.length > CLIENT_LOG_BUFFER_LIMIT)
        clientLogBuffer.shift();
    } catch (e) {}
  };
  // wrap console.error to capture messages
  try {
    const _origConsoleError = console.error.bind(console);
    console.error = function (...args) {
      try {
        pushToBuffer({
          level: "error",
          message: args
            .map((a) => (typeof a === "object" ? JSON.stringify(a) : String(a)))
            .join(" "),
          stack: (args[0] && args[0].stack) || null,
        });
      } catch (e) {}
      try {
        _origConsoleError(...args);
      } catch (e) {}
    };
  } catch (e) {}
  // beforeunload: flush buffered logs via sendBeacon (or synchronous fetch fallback)
  try {
    window.addEventListener("beforeunload", (ev) => {
      try {
        if (clientLogBuffer.length === 0) return;
        const payload = JSON.stringify({
          level: "batch",
          event: "buffered-logs",
          logs: clientLogBuffer,
          ts: new Date().toISOString(),
          ua: (typeof navigator !== "undefined" && navigator.userAgent) || "",
        });
        if (typeof navigator !== "undefined" && navigator.sendBeacon) {
          try {
            navigator.sendBeacon("/api/client-log", payload);
          } catch (e) {}
        } else if (typeof fetch !== "undefined") {
          try {
            navigator && navigator.sendBeacon
              ? null
              : fetch("/api/client-log", {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: payload,
                  keepalive: true,
                });
          } catch (e) {}
        }
      } catch (e) {}
    });
  } catch (e) {}
  try {
    // client-side error reporting back to server to help debug mount failures
    console.debug("Setting up error handlers and client logging");
    try {
      window.addEventListener("error", (ev) => {
        console.error(
          "window.error captured:",
          ev.message,
          ev.filename,
          ev.lineno
        );
        try {
          sendClientLog({
            level: "error",
            message: ev.message,
            filename: ev.filename,
            lineno: ev.lineno,
            colno: ev.colno,
            stack: ev.error && ev.error.stack,
          });
        } catch (e) {}
      });
      window.addEventListener("unhandledrejection", (ev) => {
        console.error("unhandledrejection captured:", ev.reason);
        try {
          sendClientLog({
            level: "error",
            message: String(ev.reason),
            stack: ev.reason && ev.reason.stack,
          });
        } catch (e) {}
      });

      // send initial startup ping to help catch immediate failures
      try {
        sendClientLog({ level: "info", event: "client-start" });
      } catch (e) {}
    } catch (e) {
      console.error("Error handler setup failed", e);
    }
    // initialize locale and translate static DOM
    console.debug("Initializing i18n");
    const locale = await chooseLocale();
    try {
      await loadLocale(locale);
      translateDOM(document);
    } catch (e) {
      console.warn("i18n init failed", e);
    }

    console.debug("Finding #app root");
    const root = document.getElementById("app");
    if (!root) throw new Error("Missing #app root element");
    console.debug("#app found, clearing and setting up shell");
    // limpar texto de placeholder (ex: "Carregando editor...") antes de montar UI
    root.innerHTML = "";
    // aplicar layout shell (editor + preview lado a lado)
    root.classList.add("app-shell");

    // build sidebar and editor containers
    const sidebarDiv = document.createElement("div");
    sidebarDiv.className = "sidebar";
    root.appendChild(sidebarDiv);
    // create an editor column that stacks a small btn card above the editor
    const editorColumn = document.createElement("div");
    editorColumn.className = "editor-column";
    const editorDiv = document.createElement("div");
    editorDiv.className = "editor";
    // new card wrapper for the editor
    const cardDiv = document.createElement("div");
    cardDiv.className = "editor-card";
    cardDiv.appendChild(editorDiv);
    // button card to sit above the editor card (thin horizontal bar)
    const btnDiv = document.createElement("div");
    btnDiv.className = "btn-card";
    btnDiv.textContent = "";
    // create lang-container inside btn-card so select lives there
    const langContainer = document.createElement("div");
    langContainer.className = "lang-container";
    btnDiv.appendChild(langContainer);
    editorColumn.appendChild(btnDiv);
    editorColumn.appendChild(cardDiv);
    root.appendChild(editorColumn);

    // mount formatting toolbar (doc-toolbar) into sidebar (moved outside editor)
    console.debug("Mounting formatting toolbar into sidebar");
    try {
      const fmt = createToolbar();
      sidebarDiv.appendChild(fmt);
      console.debug("Formatting toolbar mounted");
    } catch (e) {
      console.error("mount formatting toolbar failed", e);
      sendClientLog({
        level: "error",
        event: "toolbar-mount-failed",
        message: e && e.message,
        stack: e && e.stack,
      });
    }

    // Check if creating blank document
    let editorMountedViaNew = false;
    try {
      const newBlankId = sessionStorage.getItem("doccollab:new-blank");
      if (newBlankId) {
        console.debug("Creating new blank document:", newBlankId);
        sessionStorage.removeItem("doccollab:new-blank");
        const blankAst = {
          metadata: {
            id: newBlankId,
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
          },
          blocks: [
            { type: "title", id: "title_" + Date.now(), text: "" },
            { type: "author", id: "author_" + Date.now(), text: "" },
            { type: "abstract", id: "abstract_" + Date.now(), text: "" },
            {
              type: "section",
              id: "sec_" + Date.now(),
              title: "Nova Seção",
              content: [{ type: "paragraph", id: "p_" + Date.now(), text: "" }],
            },
          ],
        };
        mountEditor(editorDiv, blankAst);
        initAutosave(getAST, {
          docId: newBlankId,
          generateTex: true,
          template: null,
        });
        editorMountedViaNew = true;
        console.debug("Blank document mounted");
      } else {
        const params = new URLSearchParams(window.location.search);
        if (params.get("new") === "1") {
          console.debug("Detected ?new=1 — loading sample and mounting editor");
          const ast = await loadSample();
          console.debug("Sample AST loaded:", ast);
          mountEditor(editorDiv, ast);
          console.debug("Editor mounted successfully via ?new=1");
          initAutosave(getAST, {
            docId: "local-doc",
            generateTex: true,
            template: null,
          });
          editorMountedViaNew = true;
        }
      }
    } catch (e) {
      console.error("Failed to mount editor", e);
      sendClientLog({
        level: "error",
        event: "mount-new-failed",
        message: e && e.message,
        stack: e && e.stack,
      });
    }

    // build toolbar inside the sidebar so it appears vertical outside the editor
    console.debug(
      "buildToolbar: calling with langContainer present?",
      !!langContainer,
      langContainer
    );
    // define onLoadDoc handler so we can call it with a loading state
    async function onLoadDoc(opts) {
      console.debug("onLoadDoc called with opts:", opts);
      try {
        if (opts.source === "storage" && opts.docId) {
          try {
            const ver = await getLatestDocument(opts.docId);
            const ast = ver && ver.ast ? ver.ast : await loadSample();
            console.debug("Mounting editor with loaded doc:", opts.docId);
            mountEditor(editorDiv, ast);
            initAutosave(getAST, {
              docId: opts.docId,
              generateTex: true,
              template: null,
            });
          } catch (e) {
            console.warn("load doc failed", e);
            mountEditor(editorDiv, await loadSample());
            initAutosave(getAST, { docId: "local-doc", generateTex: true });
          }
        } else {
          // new document
          console.debug("Creating new blank document");
          const newAst = opts.blank
            ? {
                metadata: {
                  id: "doc-" + Date.now(),
                  createdAt: new Date().toISOString(),
                  updatedAt: new Date().toISOString(),
                },
                blocks: [
                  { type: "title", id: "title_" + Date.now(), text: "" },
                  { type: "author", id: "author_" + Date.now(), text: "" },
                  {
                    type: "section",
                    id: "sec_" + Date.now(),
                    title: "Nova Seção",
                    content: [
                      { type: "paragraph", id: "p_" + Date.now(), text: "" },
                    ],
                  },
                ],
              }
            : await loadSample();
          console.debug("New AST:", newAst);
          mountEditor(editorDiv, newAst);
          console.debug("Editor mounted with new document");
          initAutosave(getAST, {
            docId: "doc-" + Date.now(),
            generateTex: true,
            template: null,
          });
          console.debug("Autosave initialized");
        }
        try {
          translateDOM(document);
        } catch (e) {}
      } catch (err) {
        console.error("onLoadDoc error:", err);
        console.error(
          "Erro ao carregar documento:",
          err && (err.message || err)
        );
      }
    }

    const { docsSelect, langSelect, newBtn, compileBtn } = await buildToolbar(
      sidebarDiv,
      onLoadDoc
    );
    // attach safer change handler now that editorDiv is in scope
    try {
      docsSelect.addEventListener("change", async () => {
        const docId = docsSelect.value;
        if (!docId) return;
        try {
          // show minimal loading indicator inside editor area
          try {
            editorDiv.innerHTML =
              '<div class="loading">Carregando editor...</div>';
          } catch (e) {}
          await onLoadDoc({ source: "storage", docId });
        } catch (e) {
          console.error("Open doc failed", e);
          try {
            mountEditor(editorDiv, await loadSample());
            initAutosave(getAST, { docId: "local-doc", generateTex: true });
          } catch (ee) {}
        }
      });
    } catch (e) {
      console.warn("failed to attach docsSelect handler", e);
    }
    console.debug("buildToolbar returned:", {
      docsSelect: !!docsSelect,
      langSelect: !!langSelect,
      newBtn: !!newBtn,
      compileBtn: !!compileBtn,
    });
    // fallback: if langContainer has no children, append the returned controls into it
    try {
      console.debug(
        "langContainer children before fallback:",
        langContainer && langContainer.children
          ? langContainer.children.length
          : "no-langContainer",
        langContainer && langContainer.innerHTML
      );
      if (langContainer && langContainer.children.length === 0) {
        console.debug(
          "langContainer empty — applying fallback append of controls into langContainer"
        );
        if (langSelect) langContainer.appendChild(langSelect);
        if (newBtn) langContainer.appendChild(newBtn);
        if (compileBtn) langContainer.appendChild(compileBtn);
        console.debug(
          "langContainer children after fallback:",
          langContainer.children.length,
          langContainer.innerHTML
        );
      }
    } catch (e) {
      console.error("langContainer fallback error", e);
    }
    // Ensure any leftover toolbar controls are moved into langContainer (defensive)
    try {
      const loadBtnEl = document.querySelector(".btn-load");
      const docsSelectEl = docsSelect || document.querySelector(".docs-select");
      const moveIf = (el) => {
        if (el && langContainer && !langContainer.contains(el))
          langContainer.appendChild(el);
      };
      moveIf(loadBtnEl);
      moveIf(docsSelectEl);
      console.debug(
        "post-move langContainer children:",
        langContainer.children.length,
        langContainer.innerHTML
      );
    } catch (e) {
      console.error("post-move error", e);
    }
    // preview container will be appended below after initial mount
    // mount default: try to load first saved doc or fallback to sample (skip if already mounted via ?new=1)
    if (!editorMountedViaNew) {
      console.debug(
        "Mounting default editor (no ?new=1 detected or previous mount failed)"
      );
      try {
        const docs = await listDocuments();
        if (docs && docs.length) {
          console.debug("Found saved documents:", docs.length);
          const first = docs[0];
          const ver = await getLatestDocument(first.docId);
          const ast = ver && ver.ast ? ver.ast : await loadSample();
          console.debug("Loading first doc:", first.docId);
          mountEditor(editorDiv, ast);
          initAutosave(getAST, {
            docId: first.docId,
            generateTex: true,
            template: null,
          });
          // pre-select in UI
          const sel = document.querySelector(".docs-select");
          if (sel) sel.value = first.docId;
          console.debug("Default editor mounted from saved doc");
        } else {
          console.debug("No saved docs — mounting with sample AST");
          mountEditor(editorDiv, await loadSample());
          initAutosave(getAST, {
            docId: "local-doc",
            generateTex: true,
            template: null,
          });
          console.debug("Default editor mounted with sample");
        }
      } catch (e) {
        console.error("initial load failed", e);
        sendClientLog({
          level: "error",
          event: "mount-default-failed",
          message: e && e.message,
          stack: e && e.stack,
        });
        try {
          console.debug("Attempting fallback mount");
          mountEditor(editorDiv, await loadSample());
          initAutosave(getAST, { docId: "local-doc", generateTex: true });
          console.debug("Fallback mount succeeded");
        } catch (fallbackErr) {
          console.error("Fallback mount also failed", fallbackErr);
          sendClientLog({
            level: "fatal",
            event: "mount-fallback-failed",
            message: fallbackErr && fallbackErr.message,
            stack: fallbackErr && fallbackErr.stack,
          });
        }
      }
    } else {
      console.debug(
        "Skipping default mount — editor already mounted via ?new=1"
      );
    }

    // mount preview panel to the right of editor
    console.debug("Mounting preview panel");
    const previewDiv = document.createElement("div");
    previewDiv.className = "preview";
    root.appendChild(previewDiv);
    const previewApi = mountPreview(previewDiv, () => getAST());
    console.debug("Preview panel mounted");
    // add ad slots inside the preview container (PDF area)
    try {
      const previewAds = document.createElement("div");
      previewAds.className = "ad-slots preview-ad-slots";
      previewAds.style.cssText =
        "display:flex;gap:8px;padding:8px;box-sizing:border-box;justify-content:center;align-items:center;margin-top:8px;";
      for (let i = 0; i < 4; i++) {
        const slot = document.createElement("div");
        slot.className = "ad-slot preview-ad-slot";
        slot.dataset.adIndex = "pdf-" + (i + 1);
        slot.style.cssText =
          "flex:1;max-width:320px;height:90px;background:rgba(250,250,250,0.9);border:1px solid rgba(0,0,0,0.06);box-shadow:0 1px 0 rgba(0,0,0,0.02) inset;display:flex;align-items:center;justify-content:center;color:#555;font-size:13px;padding:6px;";
        slot.textContent = "Slot PDF " + (i + 1);
        previewAds.appendChild(slot);
      }
      previewDiv.appendChild(previewAds);
    } catch (e) {
      console.error("preview ad slots setup failed", e);
    }
    // Reserve ad slots inside the main editor column (keeps them in the document flow)
    try {
      const adsContainer = document.createElement("div");
      adsContainer.className = "ad-slots";
      adsContainer.style.cssText =
        "position:static;left:0;right:0;height:110px;display:flex;gap:8px;padding:10px;box-sizing:border-box;background:transparent;z-index:9998;justify-content:center;align-items:center;";
      for (let i = 0; i < 4; i++) {
        const slot = document.createElement("div");
        slot.className = "ad-slot";
        slot.dataset.adIndex = i + 1;
        slot.style.cssText =
          "flex:1;max-width:320px;height:90px;background:rgba(250,250,250,0.9);border:1px solid rgba(0,0,0,0.06);box-shadow:0 1px 0 rgba(0,0,0,0.02) inset;display:flex;align-items:center;justify-content:center;color:#555;font-size:13px;padding:6px;";
        slot.textContent = "Slot de anúncio " + (i + 1);
        adsContainer.appendChild(slot);
      }
      // append into editorColumn so ads are inside the main container and part of the layout
      try {
        editorColumn.appendChild(adsContainer);
      } catch (e) {
        root.appendChild(adsContainer);
      }
    } catch (e) {
      console.error("ad slots setup failed", e);
    }
    // tente atualizar o preview imediatamente após montagem
    try {
      if (previewApi && typeof previewApi.fetchCompile === "function")
        setTimeout(() => previewApi.fetchCompile(false), 300);
    } catch (e) {
      console.error("Preview initial compile failed", e);
    }
    // hook para botão 'Compilar' que foi criado no toolbar
    try {
      window.addEventListener("request:compile", () => {
        try {
          if (previewApi && typeof previewApi.fetchCompile === "function")
            previewApi.fetchCompile(true);
        } catch (e) {
          console.error("Compile request failed", e);
        }
      });
    } catch (e) {
      console.error("Compile hook setup failed", e);
    }

    // Global keyboard shortcut mappings for editor actions
    (function setupGlobalShortcuts() {
      function isTypingInField() {
        const ae = document.activeElement;
        if (!ae) return false;
        const tag = (ae.tagName || "").toLowerCase();
        if (tag === "input" || tag === "textarea") return true;
        if (ae.isContentEditable) return true;
        return false;
      }

      window.addEventListener("keydown", (e) => {
        try {
          // Ignore if typing in input/textarea or contentEditable
          if (isTypingInField()) return;

          const mod = e.ctrlKey || e.metaKey;
          // Formatting
          if (mod && !e.altKey && !e.shiftKey && e.key.toLowerCase() === "b") {
            e.preventDefault();
            window.dispatchEvent(
              new CustomEvent("toolbar:format", { detail: { cmd: "bold" } })
            );
            return;
          }
          if (mod && !e.altKey && !e.shiftKey && e.key.toLowerCase() === "i") {
            e.preventDefault();
            window.dispatchEvent(
              new CustomEvent("toolbar:format", { detail: { cmd: "italic" } })
            );
            return;
          }
          if (mod && !e.altKey && !e.shiftKey && e.key.toLowerCase() === "k") {
            e.preventDefault();
            window.dispatchEvent(
              new CustomEvent("toolbar:format", { detail: { cmd: "code" } })
            );
            return;
          }
          if (mod && e.shiftKey && !e.altKey && e.key.toLowerCase() === "k") {
            e.preventDefault();
            window.dispatchEvent(
              new CustomEvent("toolbar:insert", {
                detail: { type: "equation" },
              })
            );
            return;
          }

          // Delete / remove block (Ctrl+Delete handled by toolbar.js but map here too)
          if ((e.key === "Delete" || e.key === "Del") && mod) {
            e.preventDefault();
            window.dispatchEvent(new CustomEvent("toolbar:delete"));
            return;
          }

          // Move block
          if (mod && e.shiftKey && e.key === "ArrowUp") {
            e.preventDefault();
            window.dispatchEvent(
              new CustomEvent("toolbar:move", { detail: { dir: "up" } })
            );
            return;
          }
          if (mod && e.shiftKey && e.key === "ArrowDown") {
            e.preventDefault();
            window.dispatchEvent(
              new CustomEvent("toolbar:move", { detail: { dir: "down" } })
            );
            return;
          }

          // Compile
          if (mod && !e.shiftKey && !e.altKey && e.key === "Enter") {
            e.preventDefault();
            window.dispatchEvent(new Event("request:compile"));
            return;
          }

          // Insertions (Ctrl/Cmd + Alt + ...)
          if (mod && e.altKey && !e.shiftKey) {
            const k = e.key.toLowerCase();
            switch (k) {
              case "1":
                e.preventDefault();
                window.dispatchEvent(
                  new CustomEvent("toolbar:insert", {
                    detail: { type: "section" },
                  })
                );
                return;
              case "2":
                e.preventDefault();
                window.dispatchEvent(
                  new CustomEvent("toolbar:insert", {
                    detail: { type: "subsection" },
                  })
                );
                return;
              case "p":
                e.preventDefault();
                window.dispatchEvent(
                  new CustomEvent("toolbar:insert", {
                    detail: { type: "paragraph" },
                  })
                );
                return;
              case "e":
                e.preventDefault();
                window.dispatchEvent(
                  new CustomEvent("toolbar:insert", {
                    detail: { type: "equation" },
                  })
                );
                return;
              case "f":
                e.preventDefault();
                window.dispatchEvent(
                  new CustomEvent("toolbar:insert", {
                    detail: { type: "figure" },
                  })
                );
                return;
              case "t":
                e.preventDefault();
                window.dispatchEvent(
                  new CustomEvent("toolbar:insert", {
                    detail: { type: "table" },
                  })
                );
                return;
              case "q":
                e.preventDefault();
                window.dispatchEvent(
                  new CustomEvent("toolbar:insert", {
                    detail: { type: "pagebreak" },
                  })
                );
                return;
              case "c":
                e.preventDefault();
                window.dispatchEvent(
                  new CustomEvent("toolbar:insert", {
                    detail: { type: "citation" },
                  })
                );
                return;
              case "b":
                e.preventDefault();
                window.dispatchEvent(
                  new CustomEvent("toolbar:insert", {
                    detail: { type: "bibliography" },
                  })
                );
                return;
              default:
                break;
            }
          }
        } catch (err) {
          console.error("shortcut handler error", err);
        }
      });
    })();

    // expose generator for other modules (autosave may use window.generateLaTeX)
    try {
      window.generateLaTeX = generateLaTeX;
    } catch (e) {}
  } catch (e) {
    try {
      console.error("Error initializing app:", e);
    } catch (ee) {}
    try {
      sendClientLog({
        level: "fatal",
        event: "init-failed",
        message: e && e.message,
        stack: e && e.stack,
      });
    } catch (ee) {}
    try {
      const root = document.getElementById("app");
      if (root) {
        root.innerHTML = "";
        const msg = document.createElement("div");
        msg.className = "editor-load-error";
        try {
          msg.textContent =
            window && window.t
              ? window.t("editor.loading_error")
              : "Erro ao carregar o editor. Veja o console.";
        } catch (te) {
          msg.textContent = "Erro ao carregar o editor. Veja o console.";
        }
        root.appendChild(msg);
      }
    } catch (ee) {}
  }
});
