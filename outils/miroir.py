#!/usr/bin/env python3
"""Miroir de La Vigie sur GitHub Pages.

  python3 outils/miroir.py besoins EXPORT          -> documents complémentaires à lire (vignettes, images)
  python3 outils/miroir.py donnees EXPORT          -> reconstruit data/ depuis EXPORT (<collection>/<id>.json)
  python3 outils/miroir.py page LA-VIGIE.HTML      -> reconstruit index.html (page de l'artefact + miroir.js)

EXPORT est le dossier rempli par l'outil ArtifactData (out_dir) : un fichier JSON par document.
Seules les collections lisibles par un visiteur sont copiées (jamais consignes, retours, config/prompt,
config/collecteur, config/mode)."""
import json, os, shutil, sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUS = {"consignes", "retours"}
DOCS_EXCLUS = {"config/prompt", "config/collecteur", "config/mode"}
CHAMPS_INDEX = ("date", "mois", "traite")


def docs(export):
    for col in sorted(os.listdir(export)):
        d = os.path.join(export, col)
        if not os.path.isdir(d) or col in EXCLUS:
            continue
        for f in sorted(os.listdir(d)):
            if f.endswith(".json") and f"{col}/{f[:-5]}" not in DOCS_EXCLUS:
                yield col, f[:-5], os.path.join(d, f)


def besoins(export):
    eds = sorted(os.listdir(os.path.join(export, "editions")))
    if not eds:
        return
    print("vignettes date ==", eds[-1][:-5])
    for f in eds:
        e = json.load(open(os.path.join(export, "editions", f)))
        for cle in ("image_jour", "caricature"):
            doc = (e.get(cle) or {}).get("doc")
            if doc:
                print("document", doc)


def donnees(export):
    sortie = os.path.join(RACINE, "data")
    shutil.rmtree(sortie, ignore_errors=True)
    index = {}
    for col, did, chemin in docs(export):
        d = json.load(open(chemin))
        os.makedirs(os.path.join(sortie, col), exist_ok=True)
        json.dump(d, open(os.path.join(sortie, col, did + ".json"), "w"), ensure_ascii=False, separators=(",", ":"))
        index.setdefault(col, []).append({"_id": did, **{k: d[k] for k in CHAMPS_INDEX if isinstance(d, dict) and k in d}})
    for col, l in index.items():
        json.dump(l, open(os.path.join(sortie, col, "_index.json"), "w"), ensure_ascii=False)
    print(f"data/ : {sum(len(l) for l in index.values())} documents, {len(index)} collections")


def page(source):
    html = open(source, encoding="utf-8").read()
    tete = ('<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<meta name="robots" content="noindex">\n<script src="miroir.js"></script>\n')
    open(os.path.join(RACINE, "index.html"), "w", encoding="utf-8").write(tete + html)
    print("index.html reconstruit depuis", source)


if __name__ == "__main__":
    cmd, arg = sys.argv[1], sys.argv[2]
    {"besoins": besoins, "donnees": donnees, "page": page}[cmd](arg)
