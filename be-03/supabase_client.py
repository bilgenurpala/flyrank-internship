from supabase import Client, create_client

from config import Settings


def build_supabase_client(settings: Settings) -> Client:
    return create_client(settings.supabase_url, settings.supabase_key)
