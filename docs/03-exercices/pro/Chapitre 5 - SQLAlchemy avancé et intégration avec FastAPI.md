## Exercice 1 — Projet fil rouge : API Catalogue complet

Vous allez construire l'API Catalogue complète en intégrant SQLAlchemy + FastAPI, avec authentification JWT, CRUD persisté et déploiement Docker.

**Fonctionnalités à implémenter :**

- **Utilisateurs** : inscription (`POST /utilisateurs/`), profil (`GET /utilisateurs/moi`)
- **Authentification** : `POST /auth/token`, jeton JWT avec ID utilisateur en base
- **Articles** : CRUD complet, auteur extrait du JWT, pagination, filtre par `publie`
- **Tags** : `POST /tags/`, `GET /tags/`, assignation d'un tag à un article (`PUT /articles/{id}/tags/{tag_id}`)
- **Autorisations** : un utilisateur ne peut modifier/supprimer que ses propres articles (sauf admin)

**Critères de validation :**

- `docker compose up --build` démarre la stack sans erreur
- `alembic upgrade head` applique toutes les migrations
- Les 5 flux suivants fonctionnent de bout en bout via Swagger UI :
  1. Inscription → login → créer un article → lister les articles → voir l'auteur dans la réponse
  2. Ajouter un tag → assigner au article → lister les articles avec leurs tags
  3. Tenter de modifier l'article d'un autre utilisateur → `403`
  4. Tenter de modifier avec un jeton expiré ou invalide → `401`
  5. Supprimer un article avec le compte admin → `204`
- `pytest tests/ -v` : au moins 10 tests passants, couverture `routers/` > 75 %

## Exercice 2 — Corriger le N+1 dans une route existante

Voici une route qui souffre du problème N+1. Corrigez-la.

**Route actuelle (problématique) :**

```python
@router.get("/", response_model=List[ArticleReponse])
def list_articles(db: Session = Depends(get_db)):
    articles = db.execute(select(Article)).scalars().all()
    # Accès à article.auteur et article.tags dans la sérialisation → N+1
    return articles
```

**Travail à réaliser :**

1. Identifiez les deux relations concernées par le N+1 (`auteur` et `tags`)
2. Corrigez la requête avec `joinedload()` pour l'auteur et `selectinload()` pour les tags
3. Activez le logging SQL de SQLAlchemy pour comptabiliser les requêtes avant/après :
   ```python
   engine = create_engine(DATABASE_URL, echo=True)  # Affiche le SQL dans les logs
   ```
4. Comparez le nombre de requêtes SQL pour 10 articles, avant et après la correction

**Critère de validation :**

Avec `echo=True` et 10 articles en base, la route ne doit générer que **2 requêtes SQL** (1 SELECT articles + JOIN auteur, 1 SELECT tags IN).
