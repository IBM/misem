from cmath import inf
from turtle import distance
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from src.apply_seems import SeemsResponse

from src.apply_seems import getScore


app = FastAPI()


class SeemsRequest(BaseModel):
    ref_text: str
    inf_text: str
    distance_threshold: Optional[float] = 0.9


@app.post("/seems/score", response_model=SeemsResponse)
async def requestScore(request: SeemsRequest) -> SeemsResponse:
    return getScore(request.ref_text, request.inf_text, request.distance_threshold)
