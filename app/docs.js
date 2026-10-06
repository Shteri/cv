// Receipt files (a readable image or the PDF) kept on this device in IndexedDB: localStorage is too small for them.
// A signed-in driver's files are also uploaded to the private receipts bucket (cloud.js), and then this copy is a cache.
// Plain script: exposes window.TipulitDocs.
(function (global) {
  const DB = "tipulit-docs", STORE = "docs";
  let dbp = null;
  const open = () => dbp || (dbp = new Promise((res, rej) => {
    const r = indexedDB.open(DB, 1);
    r.onupgradeneeded = () => r.result.createObjectStore(STORE);
    r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error);
  }));
  const tx = async (mode, fn) => { const db = await open(); return new Promise((res, rej) => { const t = db.transaction(STORE, mode), q = fn(t.objectStore(STORE)); t.oncomplete = () => res(q && q.result); t.onerror = () => rej(t.error); }); };
  const put = (id, blob) => tx("readwrite", s => s.put(blob, id)).catch(() => null);
  const get = id => tx("readonly", s => s.get(id)).catch(() => null);
  const del = id => tx("readwrite", s => s.delete(id)).catch(() => null);
  global.TipulitDocs = { put, get, del };
})(typeof window !== "undefined" ? window : globalThis);
