from fastapi import APIRouter, HTTPException, status
from app.models import AdminLogin, Token
from app.database import get_database
from app.auth import auth_handler
from datetime import timedelta
from app.config import settings

router = APIRouter()

@router.post("/login", response_model=Token)
async def admin_login(credentials: AdminLogin):
    """Admin login endpoint"""
    db = get_database()
    
    # Find admin by email
    admin = await db.admins.find_one({"email": credentials.email})
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not auth_handler.verify_password(credentials.password, admin["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Get organization details
    org = await db.organizations.find_one({"organization_name": admin["organization_name"]})
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_handler.create_access_token(
        data={
            "sub": credentials.email,
            "organization_id": str(org["_id"]) if org else None,
            "organization_name": admin["organization_name"]
        },
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")