# Documentation Forza.net API v4

**Attention : Cette documentation est issue d’une analyse technique de l’API Forza.net. Elle n’est pas officielle et n’engage pas Microsoft.**

---

## 1. Présentation de l’API

L’API Forza.net v4 permet d’accéder à la galerie d’images d’un utilisateur pour un jeu donné. Elle est accessible via le point d’entrée suivant :

```http
GET https://api.forza.net/api/v4/me/gallery/{game}
```

**Paramètre** :
- `{game}` : identifiant du jeu (exemple : `fh5`, `fm7`, `fh4`).

---


## 2. Authentification

L’accès à l’API requiert un jeton d’authentification (Bearer token).

### Obtention du token

1. Connectez-vous à votre compte sur [forza.net](https://forza.net).
2. Ouvrez les outils de développement de votre navigateur (F12 ou clic droit > Inspecter).
3. Rendez-vous dans l’onglet "Network" (Réseau).
4. Filtrez sur "XHR" ou "Fetch" pour afficher les requêtes API.
5. Repérez une requête vers `https://api.forza.net/api/v4/me/gallery/{game}`.
6. Cliquez sur la requête, puis dans l’onglet "Headers", recherchez la ligne `Authorization: Bearer ...`.
7. Copiez la valeur du token (après "Bearer ") : il s’agit de votre jeton d’authentification.

Ce token est à utiliser dans le header HTTP :
`Authorization: Bearer <token>`

**Remarque :** Le token est personnel, temporaire et lié à votre session. Il peut expirer : en cas d’erreur 401, répétez la procédure pour obtenir un nouveau token.

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
## 6 Limitation sur les titres d’images et solution pratique


Si l’API ne retourne pas toutes les photos visibles sur le site, il est probable que plusieurs images partagent le même titre (par exemple : "forza"). L’API Forza.net ne retourne qu’une seule image par titre identique : les doublons sont ignorés dans la réponse.

**Procédure pour rendre une photo accessible via l’API** :
1. Dans le jeu Forza, sélectionnez la photo manquante.
2. Choisissez l’option "Ne plus partager".
3. Renommez la photo en lui attribuant un titre unique (évitez les titres par défaut des photo ou ceux déjà utilisés).
4. Repartagez la photo.
5. La photo sera alors immédiatement disponible via l’API et téléchargeable par le script.

Ce comportement a été systématiquement vérifié : toute photo possédant un titre unique apparaît instantanément dans les résultats de l’API après partage dans un jeu forza.



### 6.1 Explication technique détaillée sur la limitation des titres d’images


**Comportement serveur observé :**
Lorsque l’API `/api/v4/me/gallery/{game}` est interrogée, le backend Forza.net applique une déduplication stricte sur le champ `title` des images. Pour chaque titre, seule la première occurrence (généralement la plus ancienne) est incluse dans la réponse JSON. Les autres images portant le même titre sont ignorées et ne sont pas exposées par l’API, même si elles restent visibles dans la galerie du site web.

**Conséquence :**
Si plusieurs photos possèdent le même titre (par exemple le titre par défaut "forza"), l’API ne retournera qu’une seule d’entre elles. Les doublons sont invisibles pour tout script utilisant l’API, ce qui explique la différence entre le nombre d’images affichées sur le site et celui récupéré par l’API.

**Justification technique :**
Cette déduplication semble être une optimisation côté serveur visant à limiter la taille des réponses et à éviter les doublons dans la galerie API. Ce comportement n’est pas documenté officiellement (il n’existe pas de documentation publique sur l’API Forza.net), mais il a été confirmé par analyse et par des tests sur plusieurs comptes et photos non exposées par l’API.

---

## 7. Qualité des images

L’URL d’image retournée est généralement en `/2` (haute qualité via l’API). Il est possible de modifier le suffixe pour obtenir d’autres formats :

- `/2` : haute qualité
- `/4` : miniature
- `/6` : qualité Moyenne
**Remarque :** Tous les formats ne sont pas garantis (une erreur 404 est possible selon l’image).

---


## 8. Limitations et comportements observés

- L’API retourne uniquement les images de la galerie de l’utilisateur authentifié, mais applique une déduplication stricte sur le champ `title` : si plusieurs images possèdent le même titre, seule la première (généralement la plus ancienne) est exposée par l’API, les autres sont ignorées.
- Il n’est pas possible d’ajouter, supprimer ou modifier des images via cette API.
- Le nombre d’images affichées sur le site peut différer de celui retourné par l’API : le site affiche toutes les images, même celles avec des titres en doublon, alors que l’API ne retourne qu’une seule image par titre. Cela explique pourquoi certaines photos ancienne ou en doublon n’apparaissent pas dans le script utilisant l’API.
- Aucun filtrage n’est possible par qualité, auteur, date, etc. (uniquement par jeu).
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

- Cette documentation est basée sur une analyse technique : certains comportements peuvent évoluer selon le compte ou le contexte d’utilisation.
- Pour obtenir toutes les images affichées sur le site, il peut être nécessaire de recourir au scraping web ou à l’analyse des requêtes réseau (HAR). L’API ne garantit pas l’exhaustivité dans le cas de titres en doublon ou de synchronisation incomplète.

