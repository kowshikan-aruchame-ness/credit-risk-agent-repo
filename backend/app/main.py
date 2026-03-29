from fastapi import FastAPI
from app.routes import risk

app = FastAPI()

app.include_router(risk.router)

@app.get("/")
def root():
    return {"message": "Backend running with Gemini"}