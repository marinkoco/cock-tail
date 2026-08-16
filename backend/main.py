from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import categories_router, cocktails_router

app = FastAPI(
    title="Cock-Tail API",
    description="FastAPI REST service providing cocktail categories, recipes, and CRUD operations.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routers
app.include_router(categories_router, prefix="/api/categories")
app.include_router(cocktails_router, prefix="/api/cocktails")


@app.get("/health", tags=["system"], summary="Health check endpoint")
@app.get("/api/health", tags=["system"], summary="Health check endpoint")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/", tags=["system"], summary="API Root")
async def root() -> dict[str, str]:
    return {
        "message": "Welcome to the Cock-Tail API",
        "documentation": "/docs",
        "version": "1.0.0",
    }