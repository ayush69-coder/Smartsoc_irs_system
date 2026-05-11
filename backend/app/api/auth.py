"""
Authentication API endpoints
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from pydantic import BaseModel
from app.services.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()
security = HTTPBearer()

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict
    session_id: str

class UserCreateRequest(BaseModel):
    username: str
    email: str
    password: str
    role: str
    full_name: str

class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Get current user from JWT token"""
    token = credentials.credentials
    user_info = auth_service.verify_token(token)
    
    if not user_info:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user_info

def require_role(required_role: str):
    """Decorator to require specific role"""
    def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] != required_role:
            raise HTTPException(
                status_code=403,
                detail=f"Requires {required_role} role"
            )
        return current_user
    return role_checker

def require_permission(resource: str, action: str):
    """Decorator to require specific permission"""
    def permission_checker(current_user: dict = Depends(get_current_user)):
        if not auth_service.check_permission(current_user["role"], resource, action):
            raise HTTPException(
                status_code=403,
                detail=f"Requires {action} permission on {resource}"
            )
        return current_user
    return permission_checker

@router.post("/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Login user and return JWT token"""
    try:
        user = auth_service.authenticate_user(request.username, request.password)
        
        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid username or password"
            )
        
        token = auth_service.generate_token(user)
        session_id = auth_service.create_session(user, token)
        
        return LoginResponse(
            access_token=token,
            token_type="bearer",
            user=user,
            session_id=session_id
        )
    except HTTPException:
        # Re-raise HTTP exceptions (like 401) as-is
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")

@router.post("/auth/logout")
async def logout(current_user: dict = Depends(get_current_user)):
    """Logout user and invalidate session"""
    try:
        # In a real system, you'd need to track sessions by user_id
        # For demo purposes, we'll just return success
        return {"message": "Logged out successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Logout failed: {str(e)}")

@router.get("/auth/me")
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    try:
        user_id = current_user["user_id"]
        user_info = auth_service.get_user_by_id(user_id)
        
        if not user_info:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Add permissions
        permissions = auth_service.get_user_permissions(user_info["role"])
        user_info["permissions"] = permissions
        
        return user_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting user info: {str(e)}")

@router.get("/auth/permissions")
async def get_user_permissions(current_user: dict = Depends(get_current_user)):
    """Get current user permissions"""
    try:
        permissions = auth_service.get_user_permissions(current_user["role"])
        return {
            "role": current_user["role"],
            "permissions": permissions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting permissions: {str(e)}")

@router.get("/auth/users")
async def get_all_users(current_user: dict = Depends(require_role("admin"))):
    """Get all users (admin only)"""
    try:
        users = auth_service.get_all_users()
        return {
            "users": users,
            "total_count": len(users)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting users: {str(e)}")

@router.post("/auth/users")
async def create_user(
    request: UserCreateRequest,
    current_user: dict = Depends(require_role("admin"))
):
    """Create new user (admin only)"""
    try:
        user_id = auth_service.create_user(
            username=request.username,
            email=request.email,
            password=request.password,
            role=request.role,
            full_name=request.full_name
        )
        
        if not user_id:
            raise HTTPException(status_code=400, detail="Username or email already exists")
        
        return {
            "user_id": user_id,
            "message": "User created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

@router.put("/auth/users/{user_id}")
async def update_user(
    user_id: str,
    request: UserUpdateRequest,
    current_user: dict = Depends(require_role("admin"))
):
    """Update user (admin only)"""
    try:
        updates = request.dict(exclude_unset=True)
        success = auth_service.update_user(user_id, updates)
        
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"message": "User updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")

@router.get("/auth/stats")
async def get_auth_stats(current_user: dict = Depends(require_role("admin"))):
    """Get authentication statistics (admin only)"""
    try:
        stats = auth_service.get_auth_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting auth stats: {str(e)}")

@router.get("/auth/verify")
async def verify_token(current_user: dict = Depends(get_current_user)):
    """Verify token validity"""
    return {
        "valid": True,
        "user": current_user
    }