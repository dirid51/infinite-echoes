from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.server.api import routes
from src.server.db.session import engine, Base
from src.server.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure DB tables exist (dev mode only)
    # In prod, use Alembic strictly.
    if settings.DEBUG_MODE:
        async with engine.begin() as conn:
            # Note: This won't enable pgvector extension automatically; 
            # that must be done via migration or manual SQL.
            await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: Clean up resources if needed
    await engine.dispose()

app = FastAPI(
    title="Infinite Echoes RPG Backend",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(routes.router)

@app.get("/health")
async def health_check():
    return {"status": "active", "mode": "lazy_simulation"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.server.main:app", host="0.0.0.0", port=8000, reload=True)