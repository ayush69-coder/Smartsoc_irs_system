"""
Verdict endpoint for phishing detection
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import VerdictRequest, VerdictResponse, TokenWeight, ExplainData
from app.services.verdict_service import VerdictService
from app.services.url_features import URLFeatureExtractor
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/verdict", response_model=VerdictResponse)
async def get_verdict(request: VerdictRequest):
    """Get phishing verdict for given content"""
    try:
        # Initialize services
        verdict_service = VerdictService()
        url_extractor = URLFeatureExtractor()
        
        # Extract URL features
        url_features = url_extractor.extract_features(request.url)
        
        # Get verdict from service
        verdict = verdict_service.analyze(
            url=request.url,
            text=request.text,
            source=request.source,
            url_features=url_features
        )
        
        logger.info(f"Verdict generated for {request.url}: {verdict['action']} (score: {verdict['score']})")
        
        return VerdictResponse(**verdict)
        
    except Exception as e:
        logger.error(f"Error generating verdict: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate verdict")