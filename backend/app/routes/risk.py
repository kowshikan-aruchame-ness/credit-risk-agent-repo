from fastapi import APIRouter
from app.services.risk_service import run_risk_analysis

router = APIRouter()

@router.post("/analyze")
async def analyze(data: dict):
    company = data.get("name")
    result = run_risk_analysis(company)
    return result