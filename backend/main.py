"""
PhishGuard Pro - Main FastAPI Application
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from fastapi import Query
import time
import os
import json
from datetime import datetime
from verdict_service import VerdictService
from url_features import URLFeatureExtractor
from render_service import RenderService
from graph_service import GraphService

# Import API routers
from app.api import demo, sandbox, auth, live, policies, url_features, graph, model, audit

# Create FastAPI app
app = FastAPI(
    title="PhishGuard Pro API",
    description="AI-Powered Phishing Detection & Response Platform",
    version="v1-dev",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(demo.router, prefix="/api")
app.include_router(sandbox.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(live.router, prefix="/api")
app.include_router(policies.router, prefix="/api")
app.include_router(url_features.router, prefix="/api")
app.include_router(graph.router, prefix="/api")
app.include_router(model.router, prefix="/api")
app.include_router(audit.router, prefix="/api")

# Track startup time
startup_time = time.time()

# Initialize services
verdict_service = VerdictService()
url_extractor = URLFeatureExtractor()
render_service = RenderService()
graph_service = GraphService()

# Pydantic models
class VerdictRequest(BaseModel):
    url: str
    text: str
    source: str

class VerdictResponse(BaseModel):
    score: float
    action: str
    reasons: List[str]
    explain: Dict[str, Any]

class URLFeaturesRequest(BaseModel):
    url: str

class URLFeaturesResponse(BaseModel):
    url: str
    features: Dict[str, Any]

class LiveEvent(BaseModel):
    id: str
    timestamp: str
    source: str
    sender: str
    subject: str
    body: str
    url: str
    final_url: str
    label: str
    score: Optional[float] = None
    action: Optional[str] = None

class LiveResponse(BaseModel):
    events: List[LiveEvent]
    total: int
    limit: int
    offset: int

class LiveRequest(BaseModel):
    pass  # Empty request body

class RenderRequest(BaseModel):
    url: str

class RenderResponse(BaseModel):
    screenshot: str
    dom: Dict[str, Any]
    title: str
    status: str
    visual_analysis: Dict[str, Any]

class GraphQueryResponse(BaseModel):
    domain: str
    neighbors: List[Dict[str, Any]]
    cluster_score: float
    node_info: Optional[Dict[str, Any]] = None

class ModelStatusResponse(BaseModel):
    models: List[Dict[str, Any]]
    ensemble: Dict[str, Any]
    performance: Dict[str, Any]

class PolicyEvaluateRequest(BaseModel):
    event: Dict[str, Any]

class PolicyEvaluateResponse(BaseModel):
    policy_hits: List[Dict[str, Any]]
    final_action: str
    reason: str

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    uptime = time.time() - startup_time
    return {
        "status": "ok",
        "uptime": round(uptime, 2),
        "version": "v1-dev",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/verdict", response_model=VerdictResponse)
async def get_verdict(request: VerdictRequest):
    """Get phishing verdict for given inputs"""
    try:
        verdict = verdict_service.get_verdict(
            url=request.url,
            text=request.text,
            source=request.source
        )
        return VerdictResponse(**verdict)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing verdict: {str(e)}")

@app.post("/api/url/features", response_model=URLFeaturesResponse)
async def get_url_features(request: URLFeaturesRequest):
    """Extract features from URL"""
    try:
        features = url_extractor.extract_features(request.url)
        return URLFeaturesResponse(url=request.url, features=features)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting URL features: {str(e)}")

@app.post("/api/live", response_model=LiveResponse)
async def get_live_events(
    request: LiveRequest,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    domain: Optional[str] = Query(None),
    label: Optional[str] = Query(None)
):
    """Get live events with pagination and filtering"""
    try:
        # Load demo campaigns
        campaigns = verdict_service.demo_campaigns
        
        # Apply filters
        filtered_events = []
        for campaign in campaigns:
            # Domain filter
            if domain and domain not in campaign.get('final_url', ''):
                continue
            
            # Label filter
            if label and campaign.get('label') != label:
                continue
            
            # Get verdict for this campaign
            verdict = verdict_service.get_verdict(
                url=campaign['url'],
                text=campaign['body'],
                source=campaign['source']
            )
            
            # Create live event
            event = LiveEvent(
                id=campaign['id'],
                timestamp=campaign['timestamp'],
                source=campaign['source'],
                sender=campaign['sender'],
                subject=campaign['subject'],
                body=campaign['body'],
                url=campaign['url'],
                final_url=campaign['final_url'],
                label=campaign['label'],
                score=verdict['score'],
                action=verdict['action']
            )
            filtered_events.append(event)
        
        # Sort by timestamp (newest first)
        filtered_events.sort(key=lambda x: x.timestamp, reverse=True)
        
        # Apply pagination
        total = len(filtered_events)
        events = filtered_events[offset:offset + limit]
        
        return LiveResponse(
            events=events,
            total=total,
            limit=limit,
            offset=offset
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading live events: {str(e)}")

@app.post("/api/render", response_model=RenderResponse)
async def render_page(request: RenderRequest):
    """Render page and return screenshot + DOM"""
    try:
        render_result = render_service.render_page(request.url)
        return RenderResponse(**render_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error rendering page: {str(e)}")

@app.get("/api/graph/query", response_model=GraphQueryResponse)
async def query_graph(domain: str = Query(..., description="Domain to query")):
    """Query domain graph for neighbors and cluster info"""
    try:
        result = graph_service.query_domain(domain)
        return GraphQueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying graph: {str(e)}")

@app.get("/api/model/status", response_model=ModelStatusResponse)
async def get_model_status():
    """Get model status and metadata"""
    try:
        with open('/workspace/data/models/metadata.json', 'r') as f:
            metadata = json.load(f)
        return ModelStatusResponse(**metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading model metadata: {str(e)}")

@app.post("/api/policies/evaluate", response_model=PolicyEvaluateResponse)
async def evaluate_policies(request: PolicyEvaluateRequest):
    """Evaluate policies against an event"""
    try:
        event = request.event
        
        # Mock policy evaluation for demo
        policy_hits = []
        final_action = "allow"
        reason = "No policies matched"
        
        # Check score threshold policy
        if event.get('score', 0) > 0.8:
            policy_hits.append({
                "policy_id": "high_score_block",
                "policy_name": "High Score Block",
                "action": "block",
                "reason": f"Score {event.get('score', 0):.2f} exceeds threshold 0.8"
            })
            final_action = "block"
            reason = "High risk score detected"
        
        # Check domain blocklist
        url = event.get('url', '') or event.get('final_url', '')
        if any(domain in url for domain in ['fake-bank', 'fake-microsoft', 'scam', 'phishing']):
            policy_hits.append({
                "policy_id": "domain_blocklist",
                "policy_name": "Known Phishing Domains",
                "action": "block",
                "reason": "Domain matches blocklist"
            })
            final_action = "block"
            reason = "Domain in blocklist"
        
        # Check sender whitelist
        sender = event.get('sender', '')
        if any(trusted in sender for trusted in ['@google.com', '@microsoft.com', '@apple.com']):
            policy_hits.append({
                "policy_id": "sender_whitelist",
                "policy_name": "Trusted Senders",
                "action": "allow",
                "reason": "Sender in whitelist"
            })
            if final_action == "allow":
                final_action = "allow"
                reason = "Trusted sender"
        
        return PolicyEvaluateResponse(
            policy_hits=policy_hits,
            final_action=final_action,
            reason=reason
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error evaluating policies: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)