# Chapitre 4 — Quiz : SQLAlchemy — Modélisation et requêtes

1. Que signifie le terme **impedance objet-relationnel** dans le contexte des ORMs ?
   - A) La lenteur des requêtes SQL sur de grands volumes de données
   - B) Le décalage entre le paradigme objet (classes, attributs) et le paradigme relationnel (tables, colonnes)
   - C) L'incompatibilité entre SQLAlchemy et les bases NoSQL
   - D) La difficulté d'écrire du SQL portable entre PostgreSQL et MySQL

2. Quelle est la différence entre `SQLAlchemy Core` et `SQLAlchemy ORM` ?
   - A) Core est pour PostgreSQL, ORM est pour SQLite
   - B) Core fournit un SQL Expression Language proche du SQL ; ORM ajoute le mapping objet-relationnel avec des classes Python
   - C) Core est la version 1.x, ORM est la version 2.x
   - D) Core est synchrone, ORM est asynchrone

3. Pourquoi ajouter `connect_args={"check_same_thread": False}` lors de la création d'un Engine SQLite ?
   - A) Pour activer le mode WAL de SQLite
   - B) Pour autoriser plusieurs threads à partager la même connexion SQLite, nécessaire avec FastAPI
   - C) Pour désactiver la vérification de type des colonnes
   - D) Pour activer les index automatiques

4. Que se passe-t-il si on accède à l'attribut `auteur` d'un article **après** que la Session est fermée ?
   - A) SQLAlchemy ouvre automatiquement une nouvelle session
   - B) L'attribut retourne `None`
   - C) SQLAlchemy lève une `DetachedInstanceError`
   - D) L'attribut retourne la valeur en cache de la session précédente

5. Dans un modèle SQLAlchemy, quelle est la différence entre `default=True` et `server_default="true"` ?
   - A) Aucune différence — les deux produisent le même résultat
   - B) `default` est évalué côté Python ; `server_default` est évalué par la base de données
   - C) `default` ne fonctionne qu'avec SQLite ; `server_default` avec PostgreSQL
   - D) `server_default` est plus performant car il utilise le cache de la base

6. Pour modéliser une relation n-à-n entre `Article` et `Tag` dans SQLAlchemy, qu'est-ce qui est requis ?
   - A) Deux `ForeignKey` dans le modèle `Article`
   - B) Un modèle intermédiaire `ArticleTag` avec deux colonnes PK
   - C) Une table d'association définie avec `Table()` et référencée via `secondary` dans `relationship()`
   - D) Un champ `tags: JSON` dans `Article` contenant les IDs des tags

7. Quelle méthode SQLAlchemy recharge les attributs générés par la base (id auto-incrémenté, valeurs `server_default`) dans l'objet Python après un `commit()` ?
   - A) `db.sync(objet)`
   - B) `db.reload(objet)`
   - C) `db.refresh(objet)`
   - D) `objet.reload(db)`

8. Dans la syntaxe SQLAlchemy 2.0, quelle est la façon correcte de récupérer tous les articles publiés ?
   - A) `session.query(Article).filter_by(publie=True).all()`
   - B) `session.execute(select(Article).where(Article.publie == True)).scalars().all()`
   - C) `Article.objects.filter(publie=True)`
   - D) `session.find(Article, publie=True)`

9. Quel outil SQLAlchemy est utilisé pour gérer les migrations de schéma de base de données (ajout de colonnes, modification de contraintes) ?
   - A) `Base.metadata.migrate()`
   - B) `sqlalchemy-migrate`
   - C) `Alembic`
   - D) `Flask-Migrate`

10. Que fait `model_dump(exclude_none=True)` d'un modèle Pydantic dans le contexte d'un PATCH SQLAlchemy ?
    - A) Supprime les colonnes None de la table SQL
    - B) Retourne uniquement les champs fournis (non-None) pour ne mettre à jour que les attributs envoyés par le client
    - C) Vérifie que les valeurs None ne violent pas les contraintes NOT NULL
    - D) Convertit le modèle Pydantic en objet SQLAlchemy directement

## Corrections

1. **B) Le décalage entre le paradigme objet et le paradigme relationnel** — L'impedance objet-relationnel désigne la difficulté de faire correspondre les objets Python (héritage, méthodes, composition) avec les tables SQL (lignes, colonnes, jointures) (section "Le problème de l'impedance objet-relationnel").
2. **B) Core fournit un SQL Expression Language proche du SQL ; ORM ajoute le mapping objet-relationnel** — Core manipule des tables et des colonnes ; ORM ajoute la correspondance classes/tables et le cycle de vie des objets (section "SQLAlchemy Core vs SQLAlchemy ORM").
3. **B) Pour autoriser plusieurs threads à partager la même connexion SQLite** — SQLite interdit par défaut de partager une connexion entre threads. FastAPI utilise plusieurs threads, d'où la nécessité de ce paramètre (section "Engine — connexion à la base de données").
4. **C) SQLAlchemy lève une `DetachedInstanceError`** — Une fois la session fermée, les objets sont "detached" et ne peuvent plus charger leurs relations lazy. Le schéma du cycle de vie illustre cet état (section "Cycle de vie d'un objet SQLAlchemy dans la Session").
5. **B) `default` est évalué côté Python ; `server_default` est évalué par la base de données** — `default` est appliqué par SQLAlchemy avant l'INSERT ; `server_default` est une valeur DEFAULT SQL interprétée par le moteur de base de données (section "Attributs clés de mapped_column").
6. **C) Une table d'association définie avec `Table()` et référencée via `secondary`** — La relation n-à-n nécessite une table pivot. `secondary=articles_tags` dans `relationship()` indique à SQLAlchemy d'utiliser cette table pour les jointures (section "Relation n-à-n").
7. **C) `db.refresh(objet)`** — `db.refresh()` relit l'objet depuis la base de données pour synchroniser les champs générés côté serveur (section "Créer des enregistrements").
8. **B) `session.execute(select(Article).where(Article.publie == True)).scalars().all()`** — C'est la syntaxe ORM 2.0. La syntaxe `session.query()` est la 1.x (legacy, toujours supportée) (section "Lire des enregistrements").
9. **C) Alembic** — Alembic est l'outil de migration officiel de SQLAlchemy. `Base.metadata.create_all()` ne gère pas les migrations — il ne peut que créer les tables si elles n'existent pas (section "Migrations avec Alembic").
10. **B) Retourne uniquement les champs fournis pour ne mettre à jour que les attributs envoyés** — `exclude_none=True` filtre les champs `None`, ce qui permet un PATCH partiel : seuls les attributs fournis par le client sont propagés à `db.update()` (section "Modifier des enregistrements").
