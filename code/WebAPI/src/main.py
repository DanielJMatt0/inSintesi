from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import question, auth, team, user, answer, analyze
from src.db.session import init_db
from src.sanitizer.sanitizer import SanitizerMiddleware

app = FastAPI(title="inSintesi API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SanitizerMiddleware)

# Routers
app.include_router(question.router, prefix="/question", tags=["question"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(team.router, prefix="/team", tags=["team"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(answer.router, prefix="/answer", tags=["answer"])
app.include_router(analyze.router, prefix="/analyze", tags=["analyze"])

if __name__ == "__main__":
    import uvicorn
    init_db()
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
