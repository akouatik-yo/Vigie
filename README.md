# La Vigie — miroir GitHub Pages

Copie **en lecture seule** de La Vigie (revue de presse quotidienne de Yoann), telle que la voit un visiteur, sans les fonctions IA.
Version de test, à usage personnel.

- `index.html` : la page de la Vigie, identique à celle de l'artefact, précédée de `miroir.js`.
- `miroir.js` : remplace la base de l'artefact par les fichiers de `data/` (même interface, lecture seule, vue visiteur, pas de « Demander »).
- `data/` : les documents de la base (éditions des 60 derniers jours, murs, vidéos, présidentielle…), réécrits chaque matin à la fin de la routine de la Vigie (`outils/miroir.py donnees`, depuis la copie de la base que tient le dépôt privé).
- La page est reconstruite à chaque nouvelle version de la Vigie : `python3 outils/miroir.py page chemin/vers/la-vigie.html`.

Rien de privé n'est copié : ni consignes, ni retours, ni réglages de la rédaction.
