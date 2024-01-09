from fastapi import APIRouter

from app.api.v1.endpoints import auth, profile

api_router_v1 = APIRouter()


api_router_v1.include_router(
    auth.router,
    prefix="/v1/auth",
    tags=["Auth"])

api_router_v1.include_router(
    profile.router,
    prefix="/v1/profile",
    tags=["Profile"])
