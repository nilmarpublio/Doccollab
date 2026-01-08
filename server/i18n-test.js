import fs from 'fs';
import path from 'path';
import { JSDOM } from 'jsdom';
import { fileURLToPath, pathToFileURL } from 'url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

function loadJson(p){ return JSON.parse(fs.readFileSync(p,'utf8')); }

function compareKeys(objs){
  const locales = Object.keys(objs);
  const keysets = {};
  for(const l of locales) keysets[l] = new Set(Object.keys(objs[l]));
  const report = {};
  for(const l of locales){
    report[l] = { missing: [] };
    for(const other of locales){
      if(other===l) continue;
      for(const k of keysets[other]) if(!keysets[l].has(k)) report[l].missing.push(k);
    }
    // de-dup
    report[l].missing = [...new Set(report[l].missing)];
  }
  return report;
}

async function run(){
  const files = {
    'pt-BR': path.join(root,'assets','i18n','pt-BR.json'),
    'en-US': path.join(root,'assets','i18n','en-US.json'),
    'es-ES': path.join(root,'assets','i18n','es-ES.json')
  };
  const objs = {};
  for(const [k,p] of Object.entries(files)){
    if(!fs.existsSync(p)){ console.error('Missing locale file', p); process.exit(2); }
    objs[k] = loadJson(p);
  }

  const report = compareKeys(objs);
  let problems = false;
  console.log('i18n parity report:');
  for(const l of Object.keys(report)){
    console.log(`- ${l}: missing keys vs others: ${report[l].missing.length}`);
    if(report[l].missing.length) { problems = true; console.log(report[l].missing.join(', ')); }
  }

  // Now test loader and translateDOM using JSDOM and a mocked fetch
  const dom = new JSDOM(`<!doctype html><html><head></head><body><div data-i18n="preview.clear_highlights"></div></body></html>`);
  global.window = dom.window;
  global.document = dom.window.document;
  global.HTMLElement = dom.window.HTMLElement;

  // simple fetch mock that returns the file content when path matches
  global.fetch = async function(url){
    // url may be '/assets/i18n/en-US.json' or absolute
    const name = url.replace(/^.*\/assets\/i18n\//, '');
    const p = path.join(root,'assets','i18n', name);
    if(!fs.existsSync(p)) return { ok:false, status:404 };
    const body = fs.readFileSync(p,'utf8');
    return { ok:true, json: async ()=> JSON.parse(body) };
  };

  // import loader
  const i18nModulePath = pathToFileURL(path.join(root,'assets','js','i18n.js')).href;
  const i18n = await import(i18nModulePath);
  try{
    await i18n.loadLocale('en-US');
    i18n.translateDOM(document);
    const el = document.querySelector('[data-i18n]');
    const txt = el.textContent && el.textContent.trim();
    console.log('Loaded en-US preview.clear_highlights ->', txt);
    if(!txt || txt.length===0){ console.error('Loader failed to set text'); process.exit(3); }
  }catch(e){ console.error('i18n loader failed', e); process.exit(4); }

  if(problems){
    console.log('i18n test completed with parity issues');
    process.exit(1);
  }
  console.log('i18n test OK — parity and loader working');
  process.exit(0);
}

run();
