from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import risk

app = FastAPI()

origins = [
    "https://8080-bbcadfdbafceeafecfefbafaafdfbdaacdcac.premiumproject.examly.io"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(risk.router)

@app.get("/")
def root():
    return {"message": "Backend running with Gemini"}