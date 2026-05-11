"""
Audit endpoint
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.services.audit_service import AuditService

router = APIRouter()
audit_service = AuditService()

# Initialize with demo data
audit_service.simulate_audit_events()

@router.get("/audit/logs")
async def get_audit_logs(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    action: Optional[str] = Query(None, description="Filter by action type"),
    actor: Optional[str] = Query(None, description="Filter by actor")
):
    """Get audit logs with filtering and pagination"""
    try:
        result = audit_service.get_audit_logs(limit, offset, action, actor)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting audit logs: {str(e)}")

@router.get("/audit/stats")
async def get_audit_stats():
    """Get audit statistics"""
    try:
        stats = audit_service.get_audit_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting audit stats: {str(e)}")

@router.get("/audit/search")
async def search_audit_logs(
    query: str = Query(..., description="Search query"),
    limit: int = Query(50, ge=1, le=200)
):
    """Search audit logs"""
    try:
        results = audit_service.search_audit_logs(query, limit)
        return {
            "query": query,
            "results": results,
            "count": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching audit logs: {str(e)}")

@router.post("/audit/log")
async def log_audit_action(
    action: str,
    actor: str,
    event_id: Optional[str] = None,
    details: Optional[dict] = None,
    severity: str = "info"
):
    """Log an audit action"""
    try:
        audit_id = audit_service.log_action(action, actor, event_id, details, severity)
        return {
            "audit_id": audit_id,
            "status": "logged"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error logging audit action: {str(e)}")