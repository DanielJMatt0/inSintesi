from fastapi import FastAPI
from src.database import engine
from src.models import Base
from src.routers import question


# Initialize database
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(title="inSintesi API", version="1.0")

# Include routers
app.include_router(question.router, prefix="/question")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
