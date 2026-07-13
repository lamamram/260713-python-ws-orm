from fastapi import FastAPI

app = FastAPI(
    title="API Bibiothèque",
    description="Premier projet exo FastAPI — formation Dawan",
    version="0.1.0",
)

@app.get("/")
def read_root():
    """Point d'entrée de l'API — retourne un message de bienvenue."""
    return {"service": app.title, "version": app.version}

@app.get("/livres/{livre_id}")
def get_books(livre_id: int):
    """Retourne un livre fictif identifié par son ID entier."""
    return {"id": livre_id, "titre": f"Livre numéro {livre_id}"}

@app.get("/auteurs/{auteur_id}/livres")
def get_author_books(auteur_id: int):
    """Retourne les livres fictifs identifiés par l' ID entier d'un auteur."""
    return {"auteur_id": auteur_id, "livres": []}