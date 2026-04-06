# server/app.py — OpenEnv entry point (redirects to your actual app)
from app.main import app 

__all__ = ["app"]