# Documentation Forza.net API v4

**Attention : Cette documentation est issue d’une analyse technique de l’API Forza.net. Elle n’est pas officielle et n’engage pas Microsoft,**

---

## 1. Présentation de l’API

L’API Forza.net v4 permet d’accéder à la galerie d’images d’un utilisateur pour un jeu donné. Elle est accessible via le point d’entrée suivant :

```http
GET https://api.forza.net/api/v4/me/gallery/{game}
```

**Paramètre** :
- `{game}` : identifiant du jeu (exemple : `fh5`, `fm7`, `fh4`)

---


## 2. Authentification

L’accès à l’API requiert un jeton d’authentification (Bearer token).

### Obtention du token

1. Connectez-vous à votre compte sur [forza.net](https://forza.net).
2. Ouvrez les outils de développement de votre navigateur (F12 ou clic droit > Inspecter).
3. Rendez-vous dans l’onglet “Network” (Réseau).
4. Filtrez sur “XHR” ou “Fetch” pour afficher les requêtes API.
5. Repérez une requête vers `https://api.forza.net/api/v4/me/gallery/{game}`.
6. Cliquez sur la requête, puis dans l’onglet “Headers”, cherchez la ligne `Authorization: Bearer ...`.
7. Copiez la valeur du token (après “Bearer ”) : c’est votre jeton d’authentification.

Ce token est à utiliser dans le header HTTP :
`Authorization: Bearer <token>`

**Remarque :** Le token est personnel, temporaire et lié à votre session. Il peut expirer : en cas d’erreur 401, répétez la procédure pour obtenir un nouveau token.

---

## 3. Paramètres de la requête

- `continuationToken` (optionnel) : permet de paginer les résultats (récupération de la page suivante).

---

## 4. Structure de la réponse

Exemple de réponse JSON :

```json
{
  "items": [
    {
      "id": "fc8b4728-3f6a-4758-ffff-47dc1f20f3de",
      "title": "GTR2",
      "author": "forza kantin",
      "createdDate": "2025-10-20T12:34:56Z",
      "imageUrl": "https://t10pgalleryv2.azureedge.net/galleryv2images/fc8...",
      "downloads": 0,
      "game": "fh5"
      // ... autres champs possibles
    }
    // ... autres images
  ],
  "continuationToken": "eyJhbGciOiJUIzI1ErIsInR5cCE6IkpXVCJ9..."
}
```

---

## 5. Description des champs principaux

| Champ              | Description                                              |
|--------------------|---------------------------------------------------------|
| `id`               | Identifiant unique de l’image                            |
| `title`            | Titre de l’image                                         |
| `author`           | Auteur                                                   |
| `createdDate`      | Date de création (format ISO8601)                       |
| `imageUrl`         | URL de l’image (qualité API par défaut : `/2`)           |
| `downloads`        | Nombre de téléchargements                                |
| `game`             | Jeu concerné                                             |
| `continuationToken`| Token pour la page suivante (si présent)                 |

---

## 6. Pagination

- La réponse contient jusqu’à 40 images par page.
- Pour accéder à la page suivante, réutiliser le `continuationToken` fourni dans la réponse précédente.
- Si aucun token n’est retourné, la fin de la galerie est atteinte ou l’accès est limité par le serveur.

---

## 7. Qualité des images

L’URL d’image retournée est généralement en `/2` (haute qualité via l’API). Il est possible de modifier le suffixe pour obtenir d’autres formats :

- `/2` : haute qualité
- `/4` : miniature
- `/6` : qualité Moyenne
**Remarque** : Tous les formats ne sont pas garantis (erreur 404 possible selon l’image).

---

## 8. Limitations et comportements observés

- L’API retourne uniquement les images de la galerie de l’utilisateur authentifié.
- Il n’est pas possible d’ajouter, supprimer ou modifier des images via cette API.
- La pagination est limitée à 40 images par requête 
- Le nombre d’images affichées sur le site peut différer de celui retourné par l’API (cache, backend différent, etc.).
- Aucun filtrage possible par qualité, auteur, date, etc. (uniquement par jeu et pagination).
- Les URLs d’images sont hébergées sur le CDN AzureEdge. Les variantes `/2`, `/4`, `/6` peuvent être testées.

---

## 9. Exemple d’utilisation en Python

```python
import requests

token = "<VOTRE_BEARER_TOKEN>"
game = "fh5"
url = f"https://api.forza.net/api/v4/me/gallery/{game}"
headers = {"Authorization": f"Bearer {token}"}

response = requests.get(url, headers=headers)
data = response.json()
for item in data["items"]:
    print(item["imageUrl"])
```

---

## 10. Points d’attention

- Cette documentation est basée sur une analyse technique : certains comportements peuvent évoluer selon le compte
- Pour obtenir toutes les images affichées sur le site, il peut être nécessaire de recourir à du scraping Web ou à l’analyse des requêtes réseau, l’API ne garantissant pas l’exhaustivité.

