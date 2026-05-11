"""
Review endpoint
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from pydantic import BaseModel
from app.services.review_service import ReviewService

router = APIRouter()
review_service = ReviewService()

# Initialize with demo data
review_service.simulate_auto_review_queue()

class OverrideRequest(BaseModel):
    event_id: str
    action: str
    reason: str
    confidence: float = 0.8

class ReviewAssignmentRequest(BaseModel):
    review_id: str
    analyst_id: str

@router.get("/review/queue")
async def get_review_queue(analyst_role: str = Query("analyst", description="Analyst role: viewer, analyst, admin")):
    """Get the analyst review queue"""
    try:
        queue = review_service.get_review_queue(analyst_role)
        return {
            "review_queue": queue,
            "total_items": len(queue),
            "analyst_role": analyst_role
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting review queue: {str(e)}")

@router.post("/review/assign")
async def assign_review(request: ReviewAssignmentRequest):
    """Assign a review item to an analyst"""
    try:
        result = review_service.assign_review(request.review_id, request.analyst_id)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error assigning review: {str(e)}")

@router.post("/review/override")
async def override_verdict(request: OverrideRequest):
    """Override a verdict decision"""
    try:
        # First add to review queue if not already there
        review_item = review_service.add_to_review_queue(
            event_id=request.event_id,
            reason=f"Manual override: {request.reason}",
            priority="high"
        )
        
        # Assign to analyst
        assignment = review_service.assign_review(review_item['id'], "analyst-001")
        
        # Submit override
        result = review_service.submit_override(
            review_id=review_item['id'],
            analyst_id="analyst-001",
            action=request.action,
            reason=request.reason,
            confidence=request.confidence
        )
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "event_id": request.event_id,
            "action": request.action,
            "reason": request.reason,
            "status": "overridden",
            "override_id": result["override_id"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error overriding verdict: {str(e)}")

@router.get("/review/overrides/{event_id}")
async def get_event_overrides(event_id: str):
    """Get all overrides for a specific event"""
    try:
        overrides = review_service.get_event_overrides(event_id)
        return {
            "event_id": event_id,
            "overrides": overrides,
            "count": len(overrides)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting event overrides: {str(e)}")

@router.get("/review/analyst/{analyst_id}")
async def get_analyst_overrides(analyst_id: str):
    """Get all overrides by a specific analyst"""
    try:
        overrides = review_service.get_analyst_overrides(analyst_id)
        return {
            "analyst_id": analyst_id,
            "overrides": overrides,
            "count": len(overrides)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting analyst overrides: {str(e)}")

@router.get("/review/stats")
async def get_override_stats():
    """Get override statistics"""
    try:
        stats = review_service.get_override_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting override stats: {str(e)}")

@router.get("/review/analytics")
async def get_review_analytics():
    """Get review queue analytics"""
    try:
        analytics = review_service.get_review_analytics()
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting review analytics: {str(e)}")