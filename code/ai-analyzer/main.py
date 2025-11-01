from fastapi import FastAPI
from routes.analyze import router as analyze_router

app = FastAPI(title="inSintesi API", version="1.0.0")
app.include_router(analyze_router)
