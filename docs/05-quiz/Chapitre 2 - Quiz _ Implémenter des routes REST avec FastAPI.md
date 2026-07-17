# Chapitre 2 — Quiz : Implémenter des routes REST avec FastAPI

1. Selon les conventions REST, quelle URL est correcte pour créer un nouvel article ?
   - A) `POST /createArticle`
   - B) `GET /articles/new`
   - C) `POST /articles`
   - D) `PUT /articles/create`

2. Dans FastAPI, comment déclarer un paramètre de requête optionnel `categorie` de type chaîne, sans valeur par défaut imposée ?
   - A) `categorie: str`
   - B) `categorie: Optional[str] = None`
   - C) `categorie: str = Query(required=False)`
   - D) `categorie: str | None`

3. Quelle méthode de modèle Pydantic v2 retourne un dictionnaire en excluant les champs dont la valeur est `None` ?
   - A) `model.dict(skip_none=True)`
   - B) `model.model_dump(exclude_none=True)`
   - C) `model.to_dict(omit_null=True)`
   - D) `model.json(exclude_unset=True)`

4. Dans un décorateur `@router.post("/", status_code=201)`, quel est l'effet du paramètre `status_code=201` ?
   - A) Il valide que le corps de réponse contient un champ `id`
   - B) Il force FastAPI à retourner le code HTTP 201 en cas de succès au lieu de 200
   - C) Il indique le code HTTP attendu dans la requête du client
   - D) Il déclenche une `HTTPException` si la création échoue

5. Que retourne FastAPI quand on lève `raise HTTPException(status_code=404, detail="Introuvable")` ?
   - A) Une page HTML d'erreur 404
   - B) Une réponse JSON `{"detail": "Introuvable"}` avec le code 404
   - C) Une exception Python non interceptée visible dans les logs
   - D) Un corps vide avec le code 404

6. Dans le contexte de FastAPI, quand est-il **correct** d'utiliser `async def` pour un gestionnaire ?
   - A) Toujours — les gestionnaires doivent systématiquement être asynchrones
   - B) Jamais — FastAPI gère l'asynchrone en interne
   - C) Quand le gestionnaire effectue des opérations I/O-bound avec un équivalent async disponible (ex. httpx, SQLAlchemy async)
   - D) Uniquement pour les routes `GET`

7. Quel paramètre du décorateur de route indique à FastAPI quel modèle Pydantic utiliser pour sérialiser et **filtrer** la réponse ?
   - A) `schema_model`
   - B) `output_schema`
   - C) `response_model`
   - D) `return_type`

8. Quelle est la différence entre `PUT /articles/42` et `PATCH /articles/42` en REST ?
   - A) `PUT` est plus rapide car il n'envoie que les champs modifiés
   - B) `PUT` remplace complètement la ressource ; `PATCH` la modifie partiellement
   - C) `PUT` est idempotent, `PATCH` ne l'est pas
   - D) Il n'y a pas de différence sémantique, c'est une convention arbitraire

9. Que fait `APIRouter(prefix="/articles", tags=["Articles"])` dans FastAPI ?
   - A) Crée un sous-domaine `articles.` pour les routes
   - B) Préfixe toutes les routes du routeur avec `/articles` et les groupe sous l'onglet "Articles" dans Swagger UI
   - C) Restreint les routes aux seuls utilisateurs avec le tag "Articles"
   - D) Génère automatiquement les quatre routes CRUD

10. Dans `asyncio.gather(tache1, tache2, tache3)`, comment les trois tâches sont-elles exécutées ?
    - A) Séquentiellement, dans l'ordre déclaré
    - B) En parallèle, la durée totale étant celle de la plus lente
    - C) En parallèle, la durée totale étant la somme des trois
    - D) Dans un thread pool séparé de la boucle d'événements

## Corrections

1. **C) `POST /articles`** — En REST, l'URL désigne la ressource (un nom), la méthode HTTP désigne l'action. `POST /articles` crée un article. Les URLs avec verbes (`/createArticle`) violent les conventions REST (section "Ressources et URLs — la convention REST").
2. **B) `categorie: Optional[str] = None`** — `Optional[str]` est équivalent à `str | None` ; la valeur par défaut `None` rend le paramètre facultatif. Sans valeur par défaut, un paramètre de type primitif serait **obligatoire** dans la query string (section "Paramètres de requête").
3. **B) `model.model_dump(exclude_none=True)`** — `model_dump()` remplace `dict()` en Pydantic v2. `exclude_none=True` exclut les champs dont la valeur est `None`, ce qui est le mécanisme clé du `PATCH` partiel (section "CRUD complet").
4. **B) Il force FastAPI à retourner le code HTTP 201 en cas de succès au lieu de 200** — Par défaut FastAPI retourne 200. `status_code=201` indique que la création réussie doit retourner 201 Created (section "Réponses HTTP — codes, en-têtes et formats").
5. **B) Une réponse JSON `{"detail": "Introuvable"}` avec le code 404** — `HTTPException` est interceptée par FastAPI qui construit une `JSONResponse` avec le `status_code` et le champ `detail` fournis (section "HTTPException").
6. **C) Quand le gestionnaire effectue des opérations I/O-bound avec un équivalent async disponible** — `async def` est utile pour les I/O-bound (httpx, SQLAlchemy async). Pour les calculs CPU-bound, `def` synchrone dans un thread pool est souvent plus adapté (section "Traitements asynchrones avec async/await").
7. **C) `response_model`** — `response_model` définit le modèle Pydantic utilisé pour sérialiser et filtrer la sortie, garantissant que les champs non présents dans le modèle ne sont jamais exposés (section "response_model — filtrer la sortie").
8. **B) `PUT` remplace complètement la ressource ; `PATCH` la modifie partiellement** — `PUT` est idempotent et remplace toute la ressource ; `PATCH` ne met à jour que les champs fournis (section "Architecture REST et organisation du code").
9. **B) Préfixe toutes les routes du routeur avec `/articles` et les groupe sous l'onglet "Articles" dans Swagger UI** — `prefix` évite la répétition dans chaque décorateur ; `tags` organise les routes dans la documentation (section "Organiser le code avec APIRouter").
10. **B) En parallèle, la durée totale étant celle de la plus lente** — `asyncio.gather()` lance toutes les coroutines en parallèle et attend que toutes soient terminées. La durée totale est le maximum des durées individuelles (section "Paralléliser des appels asynchrones").
