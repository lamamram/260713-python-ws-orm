from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse, JSONResponse
from routers import taches

app = FastAPI(
    title="API Taches",
    description="Premier projet FastAPI — formation Dawan",
    version="0.1.0",
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    # message = "Validation errors:"
    # for error in exc.errors():
    #     message += f"\nField: {error['loc']}, Error: {error['msg']}"
    # return PlainTextResponse(message, status_code=400)
    
    errors = []
    for error in exc.errors():
        errors.append({
            "erreur": error["type"],
            "message": error["msg"],
            "fields": error["loc"],
            "input": error["input"]
        })
    return JSONResponse(
        status_code=400,
        content=errors
    )

app.include_router(taches.router)