from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os
from typing import Optional

security = HTTPBearer()

SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "your-supabase-jwt-secret")

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verify Supabase JWT token"""
    try:
        token = credentials.credentials
        # Decode without verification for now (in production, verify with Supabase public key)
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(payload: dict = Depends(verify_token)) -> dict:
    """Get current user from token"""
    return {
        "id": payload.get("sub"),
        "email": payload.get("email"),
        "role": payload.get("role", "user")
    }

def optional_auth(request: Request) -> Optional[dict]:
    """Optional authentication for endpoints that work with or without auth"""
    try:
        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, options={"verify_signature": False})
        return {
            "id": payload.get("sub"),
            "email": payload.get("email"),
            "role": payload.get("role", "user")
        }
    except:
        return None