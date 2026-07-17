# Programme Dawan — Python Avancé : FastAPI + ORM

> Document interne — non publié dans le HTML généré.
> Référence : PYT101931-F | Durée : 5 jours | Source : https://www.dawan.fr/formations/python/python-avance/python-avance-fastapi-orm

## Informations générales

- **Titre** : Python Avancé : FastAPI + ORM
- **Référence Dawan** : PYT101931-F
- **Durée** : 5 jours
- **Public** : Développeurs Python
- **Sanction** : Attestation de fin de formation mentionnant le résultat des acquis

## Prérequis

Avoir suivi le stage "Python : Initiation + Approfondissement" ou notions équivalentes.

## Objectifs

Construire une API en Python avec FastAPI et implémenter une couche d'accès aux données avec un ORM (SQLAlchemy).

## Programme officiel (extrait du site dawan.fr)

### Découvrir FastAPI

- Présentation des Web Services (WS) : fonctionnement, intérêt, interopérabilité
- Architecture orientée services (SOA) vs microservices : composantes, technologies
- FastAPI : présentation, cas d'usage, architecture
- FastAPI vs autres frameworks (Flask, Django)
- Design et documentation : OpenApi Specification (Swagger)
- Outils de test de services web : Postman
- Atelier : Installation de l'environnement de développement (VS Code + Interpréteur Python) — Création d'un projet FastAPI (structure, point d'entrée, dépendances)

### Implémenter et interroger des services web REST

- Architecture REST : composantes, méthodes d'appel (GET, POST, PUT, DELETE)
- Définition de routes
- Gestion des paramètres de la requête
- Validation des entrées : typing, pydantic
- Types de réponses, format (json, xml, texte, binaire)
- Gestion des erreurs
- Traitements asynchrones
- Déploiement d'un service RESTful
- Interrogation de web services

### Manipuler des bases de données en programmation objet (ORM)

- Principe des ORM (Pattern DAO)
- Bibliothèques d'ORM Python : SQLObject, SQLAlchemy, Peewee, PonyORM, Django

### Découverte d'un ORM (SQLAlchemy)

- Choix d'un ORM
- Découvrir les concepts de base des ORMs
- Mapping : modèles, colonnes, métadonnées de tables
- Gérer son schéma de données
- Concept de migrations de schéma
- Gestion des relations entre tables : n à 1, 1 à 1, n à n
- Optimisations (syndrome des n+1 requêtes, etc.)
- Atelier : Découverte de l'ORM

### Écrire des requêtes avec un ORM

- Sélections de base, filtres
- Jointures en SQL et jointures en objet
- Fonctions d'agrégation, scalaires et de fenêtrage
- Désérialisation lazy/eager
- Atelier : Développer une couche modèle efficacement

## Correspondance programme ↔ chapitres

| Sujet programme officiel | Chapitre de ce support |
|--------------------------|----------------------|
| Découvrir FastAPI | Chapitre 1 |
| REST : routes, paramètres, Pydantic | Chapitre 2 |
| Gestion des erreurs, async, déploiement | Chapitre 3 |
| ORM, SQLAlchemy, mapping, relations, migrations | Chapitre 4 |
| Requêtes ORM, lazy/eager, intégration FastAPI | Chapitre 5 |

## Choix pédagogique — ORM retenu

Le programme Dawan mentionne plusieurs ORMs Python (SQLObject, SQLAlchemy, Peewee, PonyORM, Django). Ce support utilise exclusivement **SQLAlchemy 2.0** car :

- C'est l'ORM le plus utilisé dans l'écosystème Python (hors Django)
- Il s'intègre nativement avec FastAPI via `Depends(get_db)`
- Il dispose d'un support async de première classe
- Alembic (migrations) est développé par la même équipe
