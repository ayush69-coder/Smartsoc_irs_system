"""
URL features extraction endpoint
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import URLFeaturesRequest, URLFeaturesResponse
from app.services.url_features import URLFeatureExtractor
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/url/features")
async def get_url_features(request: URLFeaturesRequest):
    """Extract features from URL"""
    try:
        extractor = URLFeatureExtractor()
        features = extractor.extract_features(request.url)
        
        logger.info(f"URL features extracted for {request.url}")
        
        # Return features at top level for backward compatibility
        response = {
            "url": request.url,
            "features": features
        }
        
        # Also include features at top level for tests
        response.update(features)
        
        return response
        
    except Exception as e:
        logger.error(f"Error extracting URL features: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to extract URL features")