"""
Authentication Service - Handles JWT auth and RBAC for demo
"""
import json
import jwt
import bcrypt
import time
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum


class UserRole(Enum):
    VIEWER = "viewer"
    ANALYST = "analyst"
    ADMIN = "admin"


class AuthService:
    def __init__(self):
        self.users = {}
        self.sessions = {}
        self.jwt_secret = "phishguard_demo_secret_2024"  # In production, use env var
        self.jwt_algorithm = "HS256"
        self.token_expiry_hours = 24
        
        # Initialize demo users
        self._initialize_demo_users()

    def _initialize_demo_users(self):
        """Initialize demo users with hashed passwords"""
        demo_users = [
            {
                "id": "user_001",
                "username": "viewer",
                "email": "viewer@phishguard.com",
                "password": "viewer123",
                "role": UserRole.VIEWER.value,
                "full_name": "Demo Viewer",
                "created_at": "2024-01-01T00:00:00Z"
            },
            {
                "id": "user_002", 
                "username": "analyst",
                "email": "analyst@phishguard.com",
                "password": "analyst123",
                "role": UserRole.ANALYST.value,
                "full_name": "Demo Analyst",
                "created_at": "2024-01-01T00:00:00Z"
            },
            {
                "id": "user_003",
                "username": "admin",
                "email": "admin@phishguard.com", 
                "password": "admin123",
                "role": UserRole.ADMIN.value,
                "full_name": "Demo Admin",
                "created_at": "2024-01-01T00:00:00Z"
            }
        ]
        
        for user in demo_users:
            hashed_password = self._hash_password(user["password"])
            self.users[user["id"]] = {
                "id": user["id"],
                "username": user["username"],
                "email": user["email"],
                "password_hash": hashed_password,
                "role": user["role"],
                "full_name": user["full_name"],
                "created_at": user["created_at"],
                "last_login": None,
                "is_active": True
            }

    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate user with username/password"""
        # Find user by username or email
        user = None
        for user_id, user_data in self.users.items():
            if (user_data["username"] == username or 
                user_data["email"] == username):
                user = user_data
                break
        
        if not user or not user["is_active"]:
            return None
        
        if not self._verify_password(password, user["password_hash"]):
            return None
        
        # Update last login
        user["last_login"] = datetime.now().isoformat()
        
        return {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"],
            "full_name": user["full_name"],
            "last_login": user["last_login"]
        }

    def generate_token(self, user: Dict[str, Any]) -> str:
        """Generate JWT token for user"""
        payload = {
            "user_id": user["id"],
            "username": user["username"],
            "role": user["role"],
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=self.token_expiry_hours)
        }
        
        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token and return user info"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            user_id = payload.get("user_id")
            
            if user_id not in self.users:
                return None
            
            user = self.users[user_id]
            if not user["is_active"]:
                return None
            
            return {
                "user_id": user_id,
                "username": payload.get("username"),
                "role": payload.get("role"),
                "exp": payload.get("exp")
            }
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def create_session(self, user: Dict[str, Any], token: str) -> str:
        """Create user session"""
        session_id = f"session_{int(time.time())}_{len(self.sessions)}"
        self.sessions[session_id] = {
            "user_id": user["id"],
            "username": user["username"],
            "role": user["role"],
            "token": token,
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "ip_address": "127.0.0.1",  # In production, get from request
            "user_agent": "PhishGuard Demo Client"
        }
        return session_id

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session by ID"""
        return self.sessions.get(session_id)

    def invalidate_session(self, session_id: str) -> bool:
        """Invalidate user session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False

    def check_permission(self, user_role: str, resource: str, action: str) -> bool:
        """Check if user role has permission for resource/action"""
        permissions = {
            UserRole.VIEWER.value: {
                "dashboard": ["read"],
                "live_feed": ["read"],
                "domain_graph": ["read"],
                "audit": ["read"],
                "settings": ["read"]
            },
            UserRole.ANALYST.value: {
                "dashboard": ["read"],
                "live_feed": ["read", "update"],
                "domain_graph": ["read"],
                "policies": ["read", "test"],
                "review": ["read", "assign", "override"],
                "sandbox": ["read", "submit"],
                "audit": ["read"],
                "settings": ["read"]
            },
            UserRole.ADMIN.value: {
                "dashboard": ["read"],
                "live_feed": ["read", "update", "delete"],
                "domain_graph": ["read"],
                "policies": ["read", "create", "update", "delete", "test"],
                "review": ["read", "assign", "override", "manage"],
                "sandbox": ["read", "submit", "manage"],
                "demo": ["read", "trigger", "manage"],
                "audit": ["read", "search"],
                "settings": ["read", "update"],
                "users": ["read", "create", "update", "delete"]
            }
        }
        
        role_permissions = permissions.get(user_role, {})
        resource_permissions = role_permissions.get(resource, [])
        
        return action in resource_permissions

    def get_user_permissions(self, user_role: str) -> Dict[str, List[str]]:
        """Get all permissions for a user role"""
        permissions = {
            UserRole.VIEWER.value: {
                "dashboard": ["read"],
                "live_feed": ["read"],
                "domain_graph": ["read"],
                "audit": ["read"],
                "settings": ["read"]
            },
            UserRole.ANALYST.value: {
                "dashboard": ["read"],
                "live_feed": ["read", "update"],
                "domain_graph": ["read"],
                "policies": ["read", "test"],
                "review": ["read", "assign", "override"],
                "sandbox": ["read", "submit"],
                "audit": ["read"],
                "settings": ["read"]
            },
            UserRole.ADMIN.value: {
                "dashboard": ["read"],
                "live_feed": ["read", "update", "delete"],
                "domain_graph": ["read"],
                "policies": ["read", "create", "update", "delete", "test"],
                "review": ["read", "assign", "override", "manage"],
                "sandbox": ["read", "submit", "manage"],
                "demo": ["read", "trigger", "manage"],
                "audit": ["read", "search"],
                "settings": ["read", "update"],
                "users": ["read", "create", "update", "delete"]
            }
        }
        
        return permissions.get(user_role, {})

    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        user = self.users.get(user_id)
        if not user:
            return None
        
        return {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "role": user["role"],
            "full_name": user["full_name"],
            "created_at": user["created_at"],
            "last_login": user["last_login"],
            "is_active": user["is_active"]
        }

    def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users (admin only)"""
        return [self.get_user_by_id(user_id) for user_id in self.users.keys()]

    def update_user(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """Update user (admin only)"""
        if user_id not in self.users:
            return False
        
        user = self.users[user_id]
        allowed_fields = ["full_name", "email", "is_active"]
        
        for field, value in updates.items():
            if field in allowed_fields:
                user[field] = value
        
        return True

    def create_user(self, username: str, email: str, password: str, 
                   role: str, full_name: str) -> Optional[str]:
        """Create new user (admin only)"""
        # Check if username or email already exists
        for user in self.users.values():
            if user["username"] == username or user["email"] == email:
                return None
        
        user_id = f"user_{int(time.time())}_{len(self.users)}"
        hashed_password = self._hash_password(password)
        
        self.users[user_id] = {
            "id": user_id,
            "username": username,
            "email": email,
            "password_hash": hashed_password,
            "role": role,
            "full_name": full_name,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "is_active": True
        }
        
        return user_id

    def get_auth_stats(self) -> Dict[str, Any]:
        """Get authentication statistics"""
        total_users = len(self.users)
        active_sessions = len(self.sessions)
        
        role_counts = {}
        for user in self.users.values():
            role = user["role"]
            role_counts[role] = role_counts.get(role, 0) + 1
        
        return {
            "total_users": total_users,
            "active_sessions": active_sessions,
            "role_breakdown": role_counts,
            "recent_logins": [
                user for user in self.users.values() 
                if user["last_login"] and 
                (datetime.now() - datetime.fromisoformat(user["last_login"])).days < 7
            ]
        }