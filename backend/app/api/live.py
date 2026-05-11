"""
Live feed endpoint
"""

from fastapi import APIRouter
from app.models.schemas import LiveFeedRequest, LiveFeedResponse, EventData
import json
import os
from typing import List

router = APIRouter()

def load_demo_events() -> List[dict]:
    """Load demo events from file"""
    events_file = "/workspace/data/demo_campaigns.json"
    if os.path.exists(events_file):
        with open(events_file, 'r') as f:
            data = json.load(f)
            # Handle both array format and object with events key
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and "events" in data:
                return data["events"]
            return []
    return []

@router.post("/live", response_model=LiveFeedResponse)
async def get_live_feed(request: LiveFeedRequest):
    """Get live feed of events"""
    try:
        # Load demo events
        all_events = load_demo_events()
        
        # Apply filters
        filtered_events = all_events
        
        if request.source:
            filtered_events = [e for e in filtered_events if e.get("source") == request.source]
        
        if request.action:
            filtered_events = [e for e in filtered_events if e.get("action") == request.action]
        
        if request.label:
            filtered_events = [e for e in filtered_events if request.label.lower() in e.get("label", "").lower()]
        
        # Apply pagination
        start_idx = request.offset
        end_idx = start_idx + request.limit
        paginated_events = filtered_events[start_idx:end_idx]
        
        # Convert to EventData objects
        events = []
        for event in paginated_events:
            try:
                # Parse timestamp string to datetime
                from datetime import datetime
                timestamp_str = event.get("timestamp", "")
                if timestamp_str:
                    timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                else:
                    timestamp = datetime.now()
                
                events.append(EventData(
                    id=event.get("id", ""),
                    timestamp=timestamp,
                    source=event.get("source", "email"),
                    sender=event.get("sender", ""),
                    subject=event.get("subject", ""),
                    body=event.get("body", ""),
                    url=event.get("url", ""),
                    final_url=event.get("final_url", ""),
                    whois=event.get("whois", {}),
                    ssl_cert=event.get("ssl_cert", {}),
                    label=event.get("label", ""),
                    verdict=None
                ))
            except Exception as e:
                # Skip invalid events
                continue
        
        return LiveFeedResponse(
            events=events,
            total=len(filtered_events),
            limit=request.limit,
            offset=request.offset
        )
        
    except Exception as e:
        # Return empty response on error
        return LiveFeedResponse(
            events=[],
            total=0,
            limit=request.limit,
            offset=request.offset
        )