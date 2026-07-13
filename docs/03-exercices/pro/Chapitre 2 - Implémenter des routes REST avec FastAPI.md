## Exercice 1 — API CRUD d'une ressource `taches`

Implémentez une API REST complète pour gérer une liste de tâches (to-do list) en mémoire.

**Ressource `Tache` :**

- `id` : entier (généré côté serveur)
- `titre` : chaîne, 3–100 caractères
- `description` : chaîne optionnelle
- `terminee` : booléen, `False` par défaut
- `priorite` : entier de 1 à 5, `3` par défaut
- `date_creation` : datetime (générée côté serveur)

**Routes à implémenter :**

| Méthode | URL | Comportement |
|---------|-----|-------------|
| `GET` | `/taches` | Liste toutes les tâches. Filtre optionnel `?terminee=true/false` |
| `POST` | `/taches` | Crée une tâche, retourne `201` avec l'objet créé |
| `GET` | `/taches/{id}` | Retourne la tâche ou `404` |
| `PATCH` | `/taches/{id}` | Met à jour partiellement, retourne l'objet modifié |
| `DELETE` | `/taches/{id}` | Supprime la tâche, retourne `204` |

**Critères de validation :**

- Schémas Pydantic distincts pour la création, la mise à jour (tous champs optionnels) et la réponse
- `response_model` défini sur toutes les routes
- `GET /taches/abc` retourne `422`, `GET /taches/999` retourne `404`
- La pagination optionnelle `?page=1&taille=5` est implémentée sur `GET /taches`
- Tous les endpoints sont visibles et testables dans Swagger UI

## Exercice 2 — Gestionnaire d'erreurs uniforme

L'objectif est de créer un handler d'exception personnalisé qui uniformise le format de toutes les erreurs de l'API.

**Format d'erreur cible :**

```json
{
  "erreur": "RESSOURCE_INTROUVABLE",
  "message": "La tâche 42 n'existe pas",
  "code": 404,
  "chemin": "/taches/42"
}
```

**Travail à réaliser :**

1. Définissez une exception `TacheIntrouvable(Exception)` avec un attribut `tache_id: int`
2. Enregistrez un handler sur `app` qui retourne le format JSON ci-dessus pour cette exception
3. Modifiez `GET /taches/{id}` et `DELETE /taches/{id}` pour lever `TacheIntrouvable` plutôt que `HTTPException`
4. Vérifiez via Swagger UI que le format de l'erreur est bien celui attendu

**Critère bonus :** surcharger également le handler de `RequestValidationError` (erreurs Pydantic) pour qu'elles utilisent le même format `{"erreur": "VALIDATION_ERROR", ...}`.
