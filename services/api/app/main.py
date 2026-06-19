from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import router
from app.core.config import settings
from app.db.session import Base, engine

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.API_PREFIX)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": settings.APP_NAME}


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


@app.exception_handler(404)
async def not_found(request, exc):
    if request.url.path.startswith("/api/"):
        return JSONResponse(status_code=404, content={"detail": "Not Found"})
    return JSONResponse(status_code=404, content={"detail": "Not Found"})
