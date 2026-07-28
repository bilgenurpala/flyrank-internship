from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request, Response
from fastapi.responses import JSONResponse
from supabase import AuthApiError

from config import load_settings
from supabase_client import build_supabase_client


class AuthenticationError(Exception):
    def __init__(self, message: str):
        self.message = message


async def read_credentials(request: Request):
    try:
        body = await request.json()
    except ValueError:
        return None
    if not isinstance(body, dict):
        return None
    email = body.get("email")
    password = body.get("password")
    if not isinstance(email, str) or not email.strip():
        return None
    if not isinstance(password, str) or not password:
        return None
    return {"email": email.strip(), "password": password}


def user_to_dict(user):
    return {
        "id": str(user.id),
        "email": user.email,
        "created_at": str(user.created_at),
    }


def extract_bearer_token(request: Request):
    authorization = request.headers.get("Authorization", "")
    scheme, separator, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not separator or not token.strip():
        return None
    return token.strip()


def get_current_user(request: Request):
    token = extract_bearer_token(request)
    if token is None:
        raise AuthenticationError("Access token required")
    try:
        response = request.app.state.supabase.auth.get_user(token)
    except AuthApiError as error:
        raise AuthenticationError("Invalid or expired token") from error
    return response.user


def create_app(supabase_client=None):
    @asynccontextmanager
    async def lifespan(application: FastAPI):
        settings = load_settings()
        application.state.supabase = supabase_client or build_supabase_client(settings)
        yield

    application = FastAPI(title="FlyRank BE-03", lifespan=lifespan)

    @application.exception_handler(AuthenticationError)
    async def authentication_error_handler(request: Request, error: AuthenticationError):
        return JSONResponse(status_code=401, content={"error": error.message})

    @application.get("/health")
    def health_check():
        return {"status": "ok", "service": "connected to Supabase"}

    @application.post("/auth/signup", status_code=201)
    async def signup(request: Request):
        credentials = await read_credentials(request)
        if credentials is None:
            return JSONResponse(
                status_code=400,
                content={"error": "Email and password are required"},
            )
        try:
            response = request.app.state.supabase.auth.sign_up(credentials)
        except AuthApiError as error:
            return JSONResponse(
                status_code=400,
                content={"error": str(error)},
            )
        return {"user": user_to_dict(response.user)}

    @application.post("/auth/login")
    async def login(request: Request):
        credentials = await read_credentials(request)
        if credentials is None:
            return JSONResponse(
                status_code=400,
                content={"error": "Email and password are required"},
            )
        try:
            response = request.app.state.supabase.auth.sign_in_with_password(
                credentials
            )
        except AuthApiError:
            return JSONResponse(
                status_code=401,
                content={"error": "Invalid login credentials"},
            )
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
        }

    @application.get("/public/info")
    def public_info():
        return {"message": "Welcome stranger! This info is public."}

    @application.get("/protected/profile")
    def protected_profile(user=Depends(get_current_user)):
        return {"user": user_to_dict(user)}

    @application.get("/protected/dashboard")
    def protected_dashboard(user=Depends(get_current_user)):
        return {
            "message": "Welcome to your protected dashboard",
            "user_id": str(user.id),
        }

    @application.post("/auth/logout", status_code=204)
    def logout(request: Request, user=Depends(get_current_user)):
        try:
            request.app.state.supabase.auth.sign_out()
        except AuthApiError as error:
            raise AuthenticationError("Invalid or expired token") from error
        return Response(status_code=204)

    return application


app = create_app()
