// bibmanager.js — Gerenciador de entradas BibTeX no cliente
export class BibManager {
  constructor(ast) {
    this.ast = ast || { metadata: {}, blocks: [] };
    // ensure bibliography block exists
    this._ensureBibBlock();
  }

  _ensureBibBlock() {
    const b = (this.ast.blocks || []).find(x => x.type === 'bibliography');
    if (!b) {
      const nb = { id: `bib_${Date.now()}`, type: 'bibliography', entries: [] };
      this.ast.blocks = this.ast.blocks || [];
      this.ast.blocks.push(nb);
      this.bibBlock = nb;
    } else this.bibBlock = b;
  }

  getEntries() { return this.bibBlock.entries || []; }

  _generateKey(base) {
    const existing = new Set(this.getEntries().map(e => e.id || e.key));
    let key = base.replace(/[^a-zA-Z0-9_:-]/g, '_');
    let i = 1;
    while (existing.has(key)) { key = `${base}_${i++}`; }
    return key;
  }

  addEntry({ key, id, author, title, year, journal, type = 'article', extra = {} }){
    const entries = this.getEntries();
    const base = key || (author ? (author.split(',')[0]||author).split(' ')[0] : 'ref');
    const finalKey = this._generateKey(base);
    const entry = Object.assign({ id: finalKey, key: finalKey, author, title, year, journal, type }, extra);
    entries.push(entry);
    this.bibBlock.entries = entries;
    return entry;
  }

  removeEntry(keyOrId) {
    const entries = this.getEntries();
    const idx = entries.findIndex(e => e.id === keyOrId || e.key === keyOrId);
    if (idx >= 0) entries.splice(idx, 1);
    return idx >= 0;
  }

  exportBib() {
    const e = this.getEntries();
    const lines = e.map(it => {
      const k = it.id || it.key;
      const fields = Object.entries(it).filter(([f]) => !['id','key','type'].includes(f)).map(([f,v]) => `  ${f} = {${String(v).replace(/\n/g,' ')}}`).join(',\n');
      return `@${it.type || 'article'}{${k},\n${fields}\n}`;
    });
    return lines.join('\n\n');
  }
}

export default BibManager;
