from fastapi import FastAPI
from app.models.user import User
from app.db.database import engine
from app.db.database import Base

app = FastAPI(
    title="PlacementIQ API",
    version="1.0.0",
    description="AI-Powered Placement Readiness Platform"
)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
    print("✅ Database Connected")


@app.get("/")
def root():
    return {"message": "Welcome to PlacementIQ API 🚀"}


@app.get("/health")
def health():
    return {"status": "healthy"}