from fastapi import FastAPI

app = FastAPI(
    title="API Catalogue",
    description="Premier projet FastAPI — formation Dawan",
    version="0.1.0",
)

## 1. contrairement à Django, les routes ne sont que des décorateurs sur des fonctions Python. 
## 2. Il n'y a pas de notion de "views" ou de "controllers" séparés.
## 3. le nom de la fonction n'a pas d'importance, 
## 4. c'est le décorateur qui définit la route et la méthode HTTP associée.
@app.get("/")
def read_root():
    """Point d'entrée de l'API — retourne un message de bienvenue."""
    return {"message": "Bienvenue sur l'API Catalogue"}