"""
Sandbox endpoint
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.sandbox_service import SandboxService

router = APIRouter()
sandbox_service = SandboxService()

class SandboxSubmitRequest(BaseModel):
    url: str
    attachment: Optional[str] = None

class SandboxSubmitResponse(BaseModel):
    submission_id: str
    status: str
    estimated_completion: str
    report_url: str

@router.post("/sandbox/submit", response_model=SandboxSubmitResponse)
async def submit_to_sandbox(request: SandboxSubmitRequest):
    """Submit URL/attachment to sandbox for analysis"""
    try:
        result = sandbox_service.submit_for_analysis(
            url=request.url,
            attachment=request.attachment
        )
        return SandboxSubmitResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting to sandbox: {str(e)}")

@router.get("/sandbox/report/{submission_id}")
async def get_sandbox_report(submission_id: str):
    """Get sandbox analysis report"""
    try:
        report = sandbox_service.get_report(submission_id)
        if "error" in report:
            raise HTTPException(status_code=404, detail=report["error"])
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving report: {str(e)}")