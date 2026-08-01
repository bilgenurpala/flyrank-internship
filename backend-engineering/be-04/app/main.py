import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.repository import PostgresRankingRepository
from app.service import RankingService

load_dotenv()

app = FastAPI(title="FlyRank BE-04")

repository = PostgresRankingRepository(os.environ["DATABASE_URL"])
service = RankingService(repository)

class RankingIn(BaseModel):
    keyword: str
    position: int
    url: str

@app.post("/rankings", status_code=201)
def create_ranking(body: RankingIn):
    try:
        return service.track_ranking(body.keyword, body.position, body.url)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@app.get("/rankings")
def list_rankings():
    return service.list_rankings()

@app.get("/rankings/{ranking_id}")
def get_ranking(ranking_id: int):
    row = service.get_ranking(ranking_id)
    if row is None:
        raise HTTPException(status_code=404, detail="not found")
    return row