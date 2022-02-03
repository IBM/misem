from cmath import inf
from fastapi import FastAPI
from pydantic import BaseModel

from src.apply_seems import getScore


app = FastAPI()


class SeemsRequest(BaseModel):
    ref_text: str
    inf_text: str


@app.post("/seems/score")
async def requestScore(request: SeemsRequest):
    print(request.ref_text)
    return getScore(request.ref_text, request.inf_text)
