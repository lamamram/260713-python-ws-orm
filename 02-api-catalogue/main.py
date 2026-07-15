from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from routers import articles, auteurs
from exceptions import RessourceNonTrouveException

app = FastAPI(
    title="API Catalogue",
    description="Premier projet FastAPI — formation Dawan",
    version="0.1.0",
)

@app.exception_handler(RessourceNonTrouveException)
async def resource_not_found_handler(
    request: Request, 
    exc: RessourceNonTrouveException
):
    return JSONResponse(
        status_code=404,
        content={
            "erreur": f"{exc.resource_type.upper()}_NOT_FOUND",
            "message": f"La ressource {exc.resource_type}: {exc.id} n'existe pas",
            "code": 404,
        },
    )

@app.get("/")
def read_root():
    """Point d'entrée de l'API — retourne un message de bienvenue."""
    return {"message": f"Bienvenue sur {app.title} ! version {app.version}"}

app.include_router(articles.router)
app.include_router(auteurs.router)