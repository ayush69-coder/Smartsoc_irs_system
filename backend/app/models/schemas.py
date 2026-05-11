"""
Pydantic schemas for PhishGuard Pro
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any, Literal
from datetime import datetime
from enum import Enum

class SourceType(str, Enum):
    EMAIL = "email"
    SMS = "sms"
    WEB = "web"

class ActionType(str, Enum):
    ALLOW = "allow"
    WARN = "warn"
    BLOCK = "block"

class VerdictRequest(BaseModel):
    """Request schema for verdict endpoint"""
    url: str = Field(..., description="URL to analyze")
    text: str = Field(..., description="Text content to analyze")
    source: SourceType = Field(..., description="Source type")

class TokenWeight(BaseModel):
    """Token with its importance weight"""
    token: str = Field(..., description="Token text")
    weight: float = Field(..., description="Importance weight (0-1)")

class ExplainData(BaseModel):
    """Explanation data for verdict"""
    tokens: List[TokenWeight] = Field(..., description="Important tokens")
    url_features: Dict[str, Any] = Field(..., description="URL feature analysis")
    visual_cues: Optional[Dict[str, Any]] = Field(None, description="Visual analysis cues")

class VerdictResponse(BaseModel):
    """Response schema for verdict endpoint"""
    score: float = Field(..., ge=0, le=1, description="Phishing score (0-1)")
    action: ActionType = Field(..., description="Recommended action")
    reasons: List[str] = Field(..., description="Reasoning for the verdict")
    explain: ExplainData = Field(..., description="Detailed explanation")

class URLFeaturesRequest(BaseModel):
    """Request schema for URL features endpoint"""
    url: str = Field(..., description="URL to analyze")

class URLFeaturesResponse(BaseModel):
    """Response schema for URL features endpoint"""
    url: str = Field(..., description="Original URL")
    features: Dict[str, Any] = Field(..., description="Extracted features")

class EventData(BaseModel):
    """Event data schema"""
    id: str = Field(..., description="Event ID")
    timestamp: datetime = Field(..., description="Event timestamp")
    source: SourceType = Field(..., description="Source type")
    sender: str = Field(..., description="Sender information")
    subject: str = Field(..., description="Subject or title")
    body: str = Field(..., description="Message body")
    url: str = Field(..., description="Original URL")
    final_url: str = Field(..., description="Final URL after redirects")
    whois: Dict[str, Any] = Field(..., description="WHOIS data")
    ssl_cert: Dict[str, Any] = Field(..., description="SSL certificate data")
    label: str = Field(..., description="Ground truth label")
    verdict: Optional[VerdictResponse] = Field(None, description="AI verdict")

class LiveFeedRequest(BaseModel):
    """Request schema for live feed"""
    limit: int = Field(10, ge=1, le=100, description="Number of events to return")
    offset: int = Field(0, ge=0, description="Offset for pagination")
    source: Optional[SourceType] = Field(None, description="Filter by source type")
    action: Optional[ActionType] = Field(None, description="Filter by action type")
    label: Optional[str] = Field(None, description="Filter by label")
    
    def __init__(self, **data):
        # Handle invalid parameters gracefully
        if 'limit' in data and data['limit'] < 1:
            data['limit'] = 10
        if 'offset' in data and data['offset'] < 0:
            data['offset'] = 0
        super().__init__(**data)

class LiveFeedResponse(BaseModel):
    """Response schema for live feed"""
    events: List[EventData] = Field(..., description="List of events")
    total: int = Field(..., description="Total number of events")
    limit: int = Field(..., description="Limit applied")
    offset: int = Field(..., description="Offset applied")

class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    timestamp: datetime = Field(..., description="Check timestamp")
    version: str = Field(..., description="Application version")
    environment: str = Field(..., description="Environment")

class LoginRequest(BaseModel):
    """Login request schema"""
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")

class LoginResponse(BaseModel):
    """Login response schema"""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")
    user: Dict[str, Any] = Field(..., description="User information")

class PolicyRule(BaseModel):
    """Policy rule schema"""
    id: str = Field(..., description="Rule ID")
    name: str = Field(..., description="Rule name")
    type: str = Field(..., description="Rule type")
    enabled: bool = Field(True, description="Whether rule is enabled")
    config: Dict[str, Any] = Field(..., description="Rule configuration")

class AuditEntry(BaseModel):
    """Audit log entry"""
    id: str = Field(..., description="Entry ID")
    timestamp: datetime = Field(..., description="Entry timestamp")
    actor: str = Field(..., description="Actor (user/role)")
    event_id: str = Field(..., description="Related event ID")
    action: str = Field(..., description="Action performed")
    summary: str = Field(..., description="Action summary")
    details: Dict[str, Any] = Field(..., description="Additional details")