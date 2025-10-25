"""
Main FastAPI application for Juicebox AI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from app.core.config import settings
from app.models.schemas import HealthCheckResponse
from app.api.routes import search, candidates

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(search.router, prefix=settings.API_V1_STR)
app.include_router(candidates.router, prefix=settings.API_V1_STR)


@app.get("/", response_model=HealthCheckResponse)
async def root():
    """Root endpoint - health check"""
    return HealthCheckResponse(
        status="healthy",
        version=settings.VERSION,
        timestamp=datetime.now()
    )


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint"""
    return HealthCheckResponse(
        status="healthy",
        version=settings.VERSION,
        timestamp=datetime.now()
    )


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print(f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   🚀 {settings.PROJECT_NAME} - Backend API Started        ║
    ║                                                           ║
    ║   Version: {settings.VERSION}                                   ║
    ║   Docs: http://{settings.HOST}:{settings.PORT}/docs                    ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    print("\n👋 Shutting down Juicebox AI Backend...")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
