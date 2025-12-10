from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class OrganizationCreate(BaseModel):
    organization_name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

class OrganizationUpdate(BaseModel):
    organization_name: str = Field(..., min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)

class OrganizationResponse(BaseModel):
    organization_name: str
    collection_name: str
    admin_email: str
    created_at: datetime
    
class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    organization_id: Optional[str] = None