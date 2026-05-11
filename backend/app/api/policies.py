"""
Policies endpoint
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import os

router = APIRouter()

# Policy models
class PolicyRule(BaseModel):
    id: str
    name: str
    type: str
    condition: str
    action: str
    enabled: bool = True

class PolicyEvaluationRequest(BaseModel):
    url: str
    text: str
    source: str
    score: float

class PolicyEvaluationResponse(BaseModel):
    action: str
    reason: str
    matched_policies: List[str]

# Load policies from file or use demo data
def load_policies():
    policies_file = "/workspace/data/policies.json"
    if os.path.exists(policies_file):
        with open(policies_file, 'r') as f:
            return json.load(f)
    else:
        # Demo policies
        return {
            "policies": [
                {
                    "id": "policy-001",
                    "name": "High Score Block",
                    "type": "score_threshold",
                    "condition": "score > 0.8",
                    "action": "block",
                    "enabled": True
                },
                {
                    "id": "policy-002", 
                    "name": "Suspicious Domain Block",
                    "type": "domain_blocklist",
                    "condition": "domain in ['fake-bank.com', 'phishing-site.net']",
                    "action": "block",
                    "enabled": True
                },
                {
                    "id": "policy-003",
                    "name": "Medium Score Warn",
                    "type": "score_threshold", 
                    "condition": "score > 0.5 and score <= 0.8",
                    "action": "warn",
                    "enabled": True
                }
            ]
        }

@router.get("/policies")
async def get_policies():
    """Get all policies"""
    policies_data = load_policies()
    return policies_data

@router.post("/policies/evaluate")
async def evaluate_policy(request: PolicyEvaluationRequest):
    """Evaluate policies against a request"""
    policies_data = load_policies()
    policies = policies_data.get("policies", [])
    
    matched_policies = []
    action = "allow"  # Default action
    reason = "No policies matched"
    
    for policy in policies:
        if not policy.get("enabled", True):
            continue
            
        try:
            # Simple policy evaluation logic
            if policy["type"] == "score_threshold":
                if policy["condition"] == "score > 0.8" and request.score > 0.8:
                    matched_policies.append(policy["id"])
                    action = policy["action"]
                    reason = f"Matched policy: {policy['name']}"
                elif policy["condition"] == "score > 0.5 and score <= 0.8" and 0.5 < request.score <= 0.8:
                    matched_policies.append(policy["id"])
                    action = policy["action"]
                    reason = f"Matched policy: {policy['name']}"
            elif policy["type"] == "domain_blocklist":
                # Extract domain from URL
                domain = request.url.split('/')[2] if '://' in request.url else request.url
                if domain in ['fake-bank.com', 'phishing-site.net']:
                    matched_policies.append(policy["id"])
                    action = policy["action"]
                    reason = f"Matched policy: {policy['name']}"
        except Exception as e:
            continue
    
    return PolicyEvaluationResponse(
        action=action,
        reason=reason,
        matched_policies=matched_policies
    )

@router.get("/policies/stats")
async def get_policy_stats():
    """Get policy statistics"""
    policies_data = load_policies()
    policies = policies_data.get("policies", [])
    
    return {
        "total_policies": len(policies),
        "enabled_policies": len([p for p in policies if p.get("enabled", True)]),
        "disabled_policies": len([p for p in policies if not p.get("enabled", True)]),
        "policy_types": {
            "score_threshold": len([p for p in policies if p.get("type") == "score_threshold"]),
            "domain_blocklist": len([p for p in policies if p.get("type") == "domain_blocklist"]),
            "sender_whitelist": len([p for p in policies if p.get("type") == "sender_whitelist"])
        }
    }