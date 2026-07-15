from fastapi import FastAPI
from routers import articles, auteurs

app = FastAPI(
    title="API Catalogue",
    description="Premier projet FastAPI — formation Dawan",
    version="0.1.0",
)

@app.get("/")
def read_root():
    """Point d'entrée de l'API — retourne un message de bienvenue."""
    return {"message": f"Bienvenue sur {app.title} ! version {app.version}"}

app.include_router(articles.router)
app.include_router(auteurs.router)