from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.api.routes import admin, appointments, auth, patients, psychologists, users
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine
from app.models import Appointment, ClinicalEvolution, ClinicalHistory, User, WhatsAppLog
from app.services.seed_service import seed_demo_data

settings = get_settings()


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        if settings.is_production:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_demo_data()
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH"],
    allow_headers=["Authorization", "Content-Type"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(auth.router, prefix=settings.api_v1_prefix)
app.include_router(admin.router, prefix=settings.api_v1_prefix)
app.include_router(users.router, prefix=settings.api_v1_prefix)
app.include_router(patients.router, prefix=settings.api_v1_prefix)
app.include_router(psychologists.router, prefix=settings.api_v1_prefix)
app.include_router(appointments.router, prefix=settings.api_v1_prefix)
