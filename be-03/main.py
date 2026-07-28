from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import load_settings
from supabase_client import build_supabase_client


def create_app(supabase_client=None):
    @asynccontextmanager
    async def lifespan(application: FastAPI):
        settings = load_settings()
        application.state.supabase = supabase_client or build_supabase_client(settings)
        yield

    application = FastAPI(title="FlyRank BE-03", lifespan=lifespan)

    @application.get("/health")
    def health_check():
        return {"status": "ok", "service": "connected to Supabase"}

    return application


app = create_app()
