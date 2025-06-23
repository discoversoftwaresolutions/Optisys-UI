from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/stack-options")
def get_stack_options():
    return JSONResponse(content={
        "options": [
            {"name": "SecurePact", "type": "Compliance", "autonomous": True},
            {"name": "StratEx", "type": "Analytics", "autonomous": False},
            {"name": "CarbonIQ", "type": "Performance Optimization", "autonomous": True}
        ]
    })
