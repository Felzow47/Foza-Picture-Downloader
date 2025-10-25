# Forza Gallery High-Res Downloader

Ce projet permet d'extraire et de télécharger automatiquement toutes les images haute résolution de la galerie Forza.net, avec déduplication intelligente et logging complet.

## 🚀 Fonctionnalités

- ✅ Téléchargement haute résolution (/2 - meilleure qualité)
- ✅ Déduplication automatique (par hash MD5)
- ✅ Logging complet des téléchargements
- ✅ Support HAR et API Forza.net

## 📋 Prérequis

- Python 3.7+
- Compte Forza.net avec galerie d'images
- Navigateur Chrome (recommandé pour HAR)

## 🛠️ Installation

1. Clonez ce repository :
   ```bash
   git clone https://github.com/Felzow47/Foza-Picture-Downloader.git
   cd Foza-Picture-Downloader
   ```

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

## 📖 Utilisation


#### 1. Capture HAR (Chrome recommandé)

1. Allez sur [forza.net](https://forza.net)
2. Connectez-vous à votre compte
3. Mettez le mode Grid dans la galerie Forza
4. Ouvrez les outils de développement : `F12` ou `Ctrl+Shift+I`
5. Cliquez sur l'onglet **"Network"** (Réseau)
6. Cochez **"Preserve log"** pour garder l'historique
7. Naviguez vers votre galerie de photos et **ouvrez chaque page une à une de la première à la dernière** pour que tous les liens d'images soient chargés dans l'onglet Network
8. Cliquez sur l'icône de téléchargement (petit symbole à côté de "Preserve log") pour exporter le HAR
9. Sauvegardez le fichier dans le même dossier que le script
10. Une fois que vous avez fait tout ça, lancez le script HAR avec cette commande

```bash
python har_image_downloader.py
```

### 📡 Méthode alternative : API directe

Pour les utilisateurs ayant renommé leurs images avec des titres uniques.

```bash
python api_download.py
```

**⚠️ Limitation importante :** L'API ne retourne que 40 images maximum. Si vous avez beaucoup de photos dans votre galerie, l'API ne récupérera pas tout !


## 🎮 Scripts disponibles

| Script | Description | Usage |
|--------|-------------|-------|
| `har_image_downloader.py` | **Recommandé** - Extraction HAR spécialisée | `python har_image_downloader.py` |
| `api_download.py` | API seulement (40 images max) | `python api_download.py` |
| `uploader-privator.py` | Automatisation partage/départage | Utile pour renommer les images en masse |

## ⚠️ Limitations et solutions


### Problème : Limitation de l'API Forza.net

**Cause :** L'API ne retourne qu'une seule image par titre identique (déduplication). Si plusieurs photos ont le même titre (ex : "forza"), seules la plus ancienne sera récupérée.

**Comment récupérer toutes vos images via l'API (Max : 40):**

1. Dans le jeu Forza, sélectionnez chaque photo manquante
2. Choisissez "Ne plus partager" (peut être automatisé avec `uploader-privator.py`)
3. Renommez la photo avec un titre unique (évitez les doublons)
4. Repartagez la photo (peut être automatisé avec `uploader-privator.py`)
5. La photo sera alors disponible via l'API (dans la limite des 40 images maximum)

## 🔧 Dépannage

- **Erreur "HAR file not found"** : Assurez-vous d'avoir exporté le fichier HAR dans le bon dossier et que le fichier HAR n'est ni vide ni corrompu.
- **Aucune image trouvée** : Vérifiez que vous avez bien ouvert toutes les pages de la galerie en mode grille (20 images par page au max) avant d'exporter le HAR. Il n'est pas nécessaire d'ouvrir chaque image individuellement, mais il faut parcourir **toutes les pages une à une** pour que tous les liens d'images soient capturés.
- **Téléchargement lent** : Les images haute résolution peuvent être volumineuses
- **Token manquant** : Normal avec HAR, le script fonctionne sans token

## 📊 Logs et suivi

- `har_downloader.log` : Log détaillé du script HAR
- `downloaded_images.log` : Liste des URLs déjà téléchargées
- `downloaded_images/` : Images téléchargées (HAR)
- `downloads/` : Images téléchargées (API)

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## 📄 Licence

Voir le fichier `LICENSE` pour les détails.