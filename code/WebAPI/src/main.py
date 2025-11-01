from fastapi import FastAPI
from src.routers import question,auth,team,user,answer
from src.db.session import init_db


# Create FastAPI app
app = FastAPI(title="inSintesi API", version="1.0")

# Include routers
app.include_router(question.router, prefix="/question", tags=["question"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(team.router, prefix="/team", tags=["team"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(answer.router, prefix="/answer", tags=["answer"])

if __name__ == "__main__":
    import uvicorn
    init_db()
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
