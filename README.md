# Forza Gallery High-Res Downloader

Ce projet permet d'extraire et de télécharger automatiquement toutes les images haute résolution de la galerie Forza.net, 


### Téléchargement direct via API 


   ```
   python api_download.py
   ```
8. Les images seront téléchargées dans le dossier `downloads/`.



## Fichiers importants

- `api_download.py` : script Python pour télécharger directement via l'API Forza.
- `downloads/` : dossier où les images sont enregistrées
- `uploader-privator.py` : script d'automatisation permettant d'enchaîner les actions "partager" et "ne plus partager" sur vos photos dans le jeu. Il simule les touches du clavier pour faciliter le retrait et le repartage de vos photos, ce qui est utile pour appliquer rapidement la solution de renommage et de partage sur un grand nombre d'images. Utilisez ce script pour automatiser la manipulation des photos et gagner du temps si vous avez beaucoup de photos à traiter.

## Limitation sur les titres d’images et solution pratique

Si l’API ne retourne pas toutes les photos visibles sur le site, vérifiez en jeu si plusieurs images portent le même titre (ex le titre par défaut des photos : "forza"). L’API Forza.net ne retourne qu’une seule image par titre identique : les doublons sont ignorés par l'api.

**Solution** :
1. Dans le jeu Forza, sélectionnez la photo manquante.
2. Choisissez l’option "Ne plus partager" (peut être automatisé avec `uploader-privator.py`).
3. Renommez la photo en lui attribuant un titre unique (évitez les titres par défaut des photo ou ceux déjà utilisés)
4. Repartagez la photo (peut être automatisé avec `uploader-privator.py`).
5. La photo sera alors immédiatement disponible via l’API et téléchargeable par le script.


## Licence
MIT
