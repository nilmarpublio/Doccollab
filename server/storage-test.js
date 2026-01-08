import { fileURLToPath, pathToFileURL } from 'url';
import path from 'path';
import fs from 'fs';

// polyfill IndexedDB in Node
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const FDBFactory = require('fake-indexeddb');
const FDBKeyRange = require('fake-indexeddb/lib/FDBKeyRange');
global.indexedDB = FDBFactory.indexedDB || FDBFactory;
global.IDBKeyRange = FDBKeyRange;

// minimal window emulation for autosave
global.window = global;
global.window.addEventListener = global.addEventListener ? global.addEventListener.bind(global) : (n,f)=>{};

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const assetsPath = path.join(__dirname, '..', 'assets', 'js', 'storage', 'indexeddb.js');
const storageModule = await import(pathToFileURL(assetsPath).href);

const { saveDocumentVersion, getLatestDocument, listDocuments, getVersions, saveArtifact, getArtifacts, getVersionById, deleteDocument } = storageModule;

async function run(){
  console.log('Storage test starting');
  const docId = 'test-doc';
  const ast1 = { metadata:{title:'v1'}, content: [ { type:'title', text:'T' } ] };
  const v1 = await saveDocumentVersion(docId, ast1);
  console.log('Saved version id', v1);
  const latest = await getLatestDocument(docId);
  console.log('Latest version docId', latest.docId, 'ts', latest.ts);

  const docs = await listDocuments();
  console.log('List documents count', docs.length);

  const versions = await getVersions(docId);
  console.log('Versions for doc', versions.length);

  // save artifact
  const aid = await saveArtifact(docId, v1, 'tex', 'content-tex');
  console.log('Saved artifact id', aid);
  const arts = await getArtifacts(docId, v1);
  console.log('Artifacts count', arts.length);

  const byId = await getVersionById(v1);
  console.log('Get version by id ok', !!byId);

  // delete document
  const deleted = await deleteDocument(docId);
  console.log('Delete document result', deleted);

  const docsAfter = await listDocuments();
  console.log('Docs after delete', docsAfter.length);

  console.log('Storage test completed');
}

run().catch(e=>{ console.error('Storage test failed', e); process.exit(2); });
