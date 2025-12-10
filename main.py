from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import organization, admin
from app.database import connect_to_mongo, close_mongo_connection

app = FastAPI(
    title="Organization Management Service",
    description="Multi-tenant organization management API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Event handlers
@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

# Include routers
app.include_router(organization.router, prefix="/org", tags=["Organization"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.get("/")
async def root():
    return {
        "message": "Organization Management Service API",
        "version": "1.0.0",
        "docs": "/docs"
    }