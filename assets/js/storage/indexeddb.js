// DocCollab-v0
// AST é a única fonte de verdade.
// Nenhuma lógica fora do modelo semântico é permitida.

// indexeddb.js — Offline-first storage with versioning per document
const DB_NAME = 'doccollab-v0';
const DB_VERSION = 1;

function openDB(){
  return new Promise((resolve, reject)=>{
    const req = indexedDB.open(DB_NAME, DB_VERSION);
    req.onupgradeneeded = (ev)=>{
      const db = ev.target.result;
      if (!db.objectStoreNames.contains('docs')) db.createObjectStore('docs', { keyPath: 'docId' });
      if (!db.objectStoreNames.contains('versions')){
        const s = db.createObjectStore('versions', { keyPath: 'id', autoIncrement: true });
        s.createIndex('by-doc', 'docId', { unique: false });
        s.createIndex('by-doc-ts', ['docId','ts'], { unique: false });
      }
      if (!db.objectStoreNames.contains('artifacts')){
        const a = db.createObjectStore('artifacts', { keyPath: 'id', autoIncrement: true });
        a.createIndex('by-doc-version', ['docId','versionId'], { unique: false });
      }
    };
    req.onsuccess = ()=> resolve(req.result);
    req.onerror = ()=> reject(req.error);
  });
}

async function saveDocumentVersion(docId, ast){
  const db = await openDB();
  const tx = db.transaction(['versions','docs'],'readwrite');
  const versions = tx.objectStore('versions');
  const docs = tx.objectStore('docs');
  const ts = new Date().toISOString();
  const version = { docId, ts, ast };
  const putReq = versions.add(version);
  return new Promise((resolve, reject)=>{
    putReq.onsuccess = (ev)=>{
      const versionId = ev.target.result;
      // update docs metadata
      docs.get(docId).onsuccess = (g)=>{
        const current = g.target.result || { docId, latestVersionId: versionId, title: (ast.metadata && ast.metadata.title) || (ast.meta && ast.meta.title) || '' };
        current.latestVersionId = versionId;
        current.updated = ts;
        docs.put(current);
      };
      tx.oncomplete = ()=> resolve(versionId);
    };
    putReq.onerror = ()=> reject(putReq.error);
  });
}

async function getLatestDocument(docId){
  const db = await openDB();
  const docs = db.transaction('docs').objectStore('docs');
  return new Promise((resolve,reject)=>{
    const r = docs.get(docId);
    r.onsuccess = ()=>{
      const rec = r.result;
      if(!rec) return resolve(null);
      // fetch version
      const verStore = db.transaction('versions').objectStore('versions');
      const idx = verStore.index('by-doc');
      const req = idx.getAll(IDBKeyRange.only(docId));
      req.onsuccess = ()=>{
        const arr = req.result || [];
        if(arr.length===0) return resolve(null);
        arr.sort((a,b)=> a.ts < b.ts ? 1 : -1);
        resolve(arr[0]);
      };
      req.onerror = ()=> resolve(null);
    };
    r.onerror = ()=> reject(r.error);
  });
}

async function listDocuments(){
  const db = await openDB();
  const store = db.transaction('docs').objectStore('docs');
  return new Promise((resolve,reject)=>{
    const out = [];
    store.openCursor().onsuccess = (ev)=>{
      const cur = ev.target.result; if(!cur) return resolve(out); out.push(cur.value); cur.continue();
    };
    store.openCursor().onerror = (e)=> reject(e.target.error);
  });
}

async function getVersions(docId){
  const db = await openDB();
  const verStore = db.transaction('versions').objectStore('versions');
  const idx = verStore.index('by-doc');
  return new Promise((resolve,reject)=>{
    const req = idx.getAll(IDBKeyRange.only(docId));
    req.onsuccess = ()=> resolve((req.result||[]).sort((a,b)=> a.ts < b.ts ? 1 : -1));
    req.onerror = ()=> reject(req.error);
  });
}

async function saveArtifact(docId, versionId, type, content){
  const db = await openDB();
  const store = db.transaction('artifacts','readwrite').objectStore('artifacts');
  const item = { docId, versionId, type, content, ts: new Date().toISOString() };
  return new Promise((resolve,reject)=>{
    const r = store.add(item);
    r.onsuccess = ()=> resolve(r.result);
    r.onerror = ()=> reject(r.error);
  });
}

async function getArtifacts(docId, versionId){
  const db = await openDB();
  const store = db.transaction('artifacts').objectStore('artifacts');
  const idx = store.index('by-doc-version');
  return new Promise((resolve,reject)=>{
    const req = idx.getAll([docId, versionId]);
    req.onsuccess = ()=> resolve(req.result || []);
    req.onerror = ()=> reject(req.error);
  });
}

async function getVersionById(versionId){
  const db = await openDB();
  const store = db.transaction('versions').objectStore('versions');
  return new Promise((resolve,reject)=>{
    const r = store.get(versionId);
    r.onsuccess = ()=> resolve(r.result || null);
    r.onerror = ()=> reject(r.error);
  });
}

/**
 * Exclui um documento e todas as suas versões e artefatos.
 * Retorna true se algum registro foi removido.
 */
async function deleteDocument(docId){
  const db = await openDB();
  const tx = db.transaction(['docs','versions','artifacts'],'readwrite');
  const docs = tx.objectStore('docs');
  const vers = tx.objectStore('versions');
  const arts = tx.objectStore('artifacts');

  // remove doc metadata
  const delDocReq = docs.delete(docId);

  // remove versions by cursor
  const idx = vers.index('by-doc');
  const range = IDBKeyRange.only(docId);
  const versReq = idx.openCursor(range);
  versReq.onsuccess = (ev)=>{
    const cur = ev.target.result;
    if(!cur) return;
    vers.delete(cur.primaryKey);
    cur.continue();
  };

  // remove artifacts by cursor
  const aIdx = arts.index('by-doc-version');
  const aReq = aIdx.openCursor(IDBKeyRange.bound([docId, -Infinity], [docId, Infinity]));
  aReq.onsuccess = (ev)=>{
    const cur = ev.target.result;
    if(!cur) return;
    arts.delete(cur.primaryKey);
    cur.continue();
  };

  return new Promise((resolve,reject)=>{
    tx.oncomplete = ()=> resolve(true);
    tx.onerror = ()=> reject(tx.error);
  });
}

// Autosave helper: listens to window 'ast:changed' events and saves versions debounced
export function initAutosave(getAST, opts = {}){
  const docId = opts.docId || 'local-doc';
  const delay = opts.delay || 1200;
  let timer = null;
  window.addEventListener('ast:changed', ()=>{
    if(timer) clearTimeout(timer);
    timer = setTimeout(async ()=>{
      try{
        const ast = (typeof getAST === 'function') ? getAST() : getAST;
        if(!ast) return;
        const vid = await saveDocumentVersion(docId, ast);
        console.debug('IndexedDB: saved version', vid, 'docId', docId);
        // optionally save a .tex artifact for quick offline preview (client generator)
        if (opts.generateTex && window.generateLaTeX) {
          try{
            const tex = window.generateLaTeX(ast, opts.template || null);
            await saveArtifact(docId, vid, 'tex', tex);
          }catch(e){ /* ignore */ }
        }
      }catch(e){ console.warn('autosave failed', e); }
    }, delay);
  });
}

export { openDB, saveDocumentVersion, getLatestDocument, listDocuments, getVersions, getVersionById, saveArtifact, getArtifacts, deleteDocument };
