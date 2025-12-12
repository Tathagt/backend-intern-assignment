from fastapi import APIRouter, HTTPException, status, Depends
from app.models import OrganizationCreate, OrganizationUpdate, OrganizationResponse
from app.database import get_database
from app.auth import auth_handler, get_current_user, TokenData
from datetime import datetime
import re

router = APIRouter()

def sanitize_collection_name(org_name: str) -> str:
    sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', org_name.lower())
    return f"org_{sanitized}"

@router.post("/create", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(org_data: OrganizationCreate):
    db = get_database()
    
    
    existing_org = await db.organizations.find_one({"organization_name": org_data.organization_name})
    if existing_org:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization already exists"
        )
    
    
    existing_admin = await db.admins.find_one({"email": org_data.email})
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin email already registered"
        )
    
    
    collection_name = sanitize_collection_name(org_data.organization_name)
    
    
    hashed_password = auth_handler.get_password_hash(org_data.password)
    
    
    admin_doc = {
        "email": org_data.email,
        "password": hashed_password,
        "organization_name": org_data.organization_name,
        "created_at": datetime.utcnow()
    }
    admin_result = await db.admins.insert_one(admin_doc)
    
    
    org_doc = {
        "organization_name": org_data.organization_name,
        "collection_name": collection_name,
        "admin_id": str(admin_result.inserted_id),
        "admin_email": org_data.email,
        "created_at": datetime.utcnow()
    }
    await db.organizations.insert_one(org_doc)
    
    
    await db.create_collection(collection_name)
    
    
    await db[collection_name].insert_one({
        "initialized": True,
        "created_at": datetime.utcnow(),
        "organization": org_data.organization_name
    })
    
    return OrganizationResponse(
        organization_name=org_data.organization_name,
        collection_name=collection_name,
        admin_email=org_data.email,
        created_at=org_doc["created_at"]
    )

@router.get("/get", response_model=OrganizationResponse)
async def get_organization(organization_name: str):
    """Get organization details by name"""
    db = get_database()
    
    org = await db.organizations.find_one({"organization_name": organization_name})
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    return OrganizationResponse(
        organization_name=org["organization_name"],
        collection_name=org["collection_name"],
        admin_email=org["admin_email"],
        created_at=org["created_at"]
    )

@router.put("/update", response_model=OrganizationResponse)
async def update_organization(
    org_data: OrganizationUpdate,
    current_user: TokenData = Depends(get_current_user)
):
    """Update organization details"""
    db = get_database()
    
    
    org = await db.organizations.find_one({"organization_name": org_data.organization_name})
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    
    admin = await db.admins.find_one({"email": current_user.email})
    if not admin or admin["organization_name"] != org_data.organization_name:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this organization"
        )
    
    
    update_data = {}
    if org_data.email:
        update_data["email"] = org_data.email
        await db.organizations.update_one(
            {"organization_name": org_data.organization_name},
            {"$set": {"admin_email": org_data.email}}
        )
    
    if org_data.password:
        update_data["password"] = auth_handler.get_password_hash(org_data.password)
    
    if update_data:
        await db.admins.update_one(
            {"email": current_user.email},
            {"$set": update_data}
        )
    
    
    updated_org = await db.organizations.find_one({"organization_name": org_data.organization_name})
    
    return OrganizationResponse(
        organization_name=updated_org["organization_name"],
        collection_name=updated_org["collection_name"],
        admin_email=updated_org["admin_email"],
        created_at=updated_org["created_at"]
    )

@router.delete("/delete", status_code=status.HTTP_200_OK)
async def delete_organization(
    organization_name: str,
    current_user: TokenData = Depends(get_current_user)
):
    """Delete organization and its collection"""
    db = get_database()
    
    
    org = await db.organizations.find_one({"organization_name": organization_name})
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    
    admin = await db.admins.find_one({"email": current_user.email})
    if not admin or admin["organization_name"] != organization_name:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this organization"
        )
    
    
    await db.drop_collection(org["collection_name"])
    
    
    await db.organizations.delete_one({"organization_name": organization_name})
    
    
    await db.admins.delete_one({"email": current_user.email})
    
    return {
        "message": f"Organization '{organization_name}' deleted successfully",
        "deleted_collection": org["collection_name"]
    }
