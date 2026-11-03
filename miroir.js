/* Miroir de La Vigie sur GitHub Pages : remplace la base de l'artefact par des fichiers JSON statiques (data/),
   en lecture seule, vue « visiteur » (non propriétaire), sans fonctions IA (« Demander » absent).
   Même interface que la base de l'artefact : collection().where().orderBy().limit().get()/onSnapshot(), doc().get(). */
(function () {
  const cache = {};
  const lire = p => cache[p] ??= fetch("data/" + p, { cache: "no-cache" }).then(r => r.ok ? r.json() : null).catch(() => null);
  const cmp = (a, op, b) => op === "==" ? a == b : op === "!=" ? a != b : op === "<" ? a < b : op === "<=" ? a <= b : op === ">" ? a > b : op === ">=" ? a >= b : op === "in" ? (b || []).includes(a) : true;
  const lectureSeule = () => Promise.reject(new Error("Miroir en lecture seule"));
  function dref(chemin) {
    const id = chemin.split("/").pop();
    const get = () => lire(chemin + ".json").then(v => ({ id, exists: !!v, data: () => v }));
    return { id, get, onSnapshot(ok, err) { get().then(ok, err); return () => {}; }, set: lectureSeule, update: lectureSeule, delete: lectureSeule };
  }
  function q(col, filtres = [], ordre = null, n = 1000) {
    return {
      where: (a, op, b) => q(col, [...filtres, [a, op, b]], ordre, n),
      orderBy: (a, sens = "asc") => q(col, filtres, [a, sens], n),
      limit: k => q(col, filtres, ordre, k),
      doc: id => dref(col + "/" + id),
      add: lectureSeule,
      async get() {
        let l = ((await lire(col + "/_index.json")) || []).filter(x => filtres.every(([a, op, b]) => cmp(x[a], op, b)));
        if (ordre) l.sort((x, y) => (x[ordre[0]] > y[ordre[0]] ? 1 : x[ordre[0]] < y[ordre[0]] ? -1 : 0) * (ordre[1] === "desc" ? -1 : 1));
        l = l.slice(0, n);
        const docs = (await Promise.all(l.map(x => lire(col + "/" + x._id + ".json").then(d => ({ id: x._id, exists: !!d, data: () => d }))))).filter(d => d.exists);
        return { empty: !docs.length, size: docs.length, docs };
      },
      onSnapshot(ok, err) { this.get().then(ok, err); return () => {}; }
    };
  }
  try { if (!localStorage.getItem("vigie-bandeau-vu")) localStorage.setItem("vigie-bandeau-vu", "true"); } catch {} // bandeau « Demander » sans objet ici
  const db = { collection: c => q(c), doc: dref };
  window.claude = { use: nom => Promise.resolve(nom === "db" ? db : nom === "user" ? { isOwner: async () => false } : null) };
})();
