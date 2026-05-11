"""
Review Service - Handles analyst review queue and overrides
"""
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class ReviewStatus(Enum):
    PENDING = "pending"
    IN_REVIEW = "in_review"
    RESOLVED = "resolved"
    ESCALATED = "escalated"


class OverrideAction(Enum):
    FALSE_POSITIVE = "false_positive"
    CONFIRMED_PHISHING = "confirmed_phishing"
    ESCALATE = "escalate"
    IGNORE = "ignore"


class ReviewService:
    def __init__(self):
        self.review_queue = []
        self.overrides = {}
        self.analyst_roles = {
            'viewer': ['read'],
            'analyst': ['read', 'review', 'override'],
            'admin': ['read', 'review', 'override', 'manage']
        }

    def add_to_review_queue(self, event_id: str, reason: str, priority: str = "medium") -> Dict[str, Any]:
        """Add an event to the analyst review queue"""
        review_item = {
            'id': f"review_{int(time.time())}_{len(self.review_queue)}",
            'event_id': event_id,
            'reason': reason,
            'priority': priority,
            'status': ReviewStatus.PENDING.value,
            'created_at': datetime.now().isoformat(),
            'assigned_to': None,
            'reviewed_at': None,
            'resolution': None
        }
        
        self.review_queue.append(review_item)
        return review_item

    def get_review_queue(self, analyst_role: str = "analyst") -> List[Dict[str, Any]]:
        """Get review queue for analyst"""
        if analyst_role not in self.analyst_roles:
            return []
        
        # Filter based on role permissions
        if analyst_role == 'viewer':
            return [item for item in self.review_queue if item['status'] == ReviewStatus.RESOLVED.value]
        else:
            return self.review_queue

    def assign_review(self, review_id: str, analyst_id: str) -> Dict[str, Any]:
        """Assign a review item to an analyst"""
        review_item = next((item for item in self.review_queue if item['id'] == review_id), None)
        
        if not review_item:
            return {"error": "Review item not found"}
        
        if review_item['status'] != ReviewStatus.PENDING.value:
            return {"error": "Review item is not pending"}
        
        review_item['assigned_to'] = analyst_id
        review_item['status'] = ReviewStatus.IN_REVIEW.value
        
        return {
            "review_id": review_id,
            "assigned_to": analyst_id,
            "status": "assigned"
        }

    def submit_override(self, review_id: str, analyst_id: str, action: str, 
                       reason: str, confidence: float = 0.8) -> Dict[str, Any]:
        """Submit an analyst override decision"""
        review_item = next((item for item in self.review_queue if item['id'] == review_id), None)
        
        if not review_item:
            return {"error": "Review item not found"}
        
        if review_item['assigned_to'] != analyst_id:
            return {"error": "Not assigned to this analyst"}
        
        if review_item['status'] != ReviewStatus.IN_REVIEW.value:
            return {"error": "Review item is not in review"}
        
        # Validate action
        try:
            OverrideAction(action)
        except ValueError:
            return {"error": f"Invalid action: {action}"}
        
        # Create override record
        override_id = f"override_{int(time.time())}_{len(self.overrides)}"
        override = {
            'id': override_id,
            'review_id': review_id,
            'event_id': review_item['event_id'],
            'analyst_id': analyst_id,
            'action': action,
            'reason': reason,
            'confidence': confidence,
            'created_at': datetime.now().isoformat(),
            'status': 'applied'
        }
        
        self.overrides[override_id] = override
        
        # Update review item
        review_item['status'] = ReviewStatus.RESOLVED.value
        review_item['reviewed_at'] = datetime.now().isoformat()
        review_item['resolution'] = {
            'action': action,
            'reason': reason,
            'confidence': confidence,
            'analyst_id': analyst_id
        }
        
        return {
            "override_id": override_id,
            "review_id": review_id,
            "action": action,
            "status": "applied"
        }

    def get_event_overrides(self, event_id: str) -> List[Dict[str, Any]]:
        """Get all overrides for a specific event"""
        return [override for override in self.overrides.values() 
                if override['event_id'] == event_id]

    def get_analyst_overrides(self, analyst_id: str) -> List[Dict[str, Any]]:
        """Get all overrides by a specific analyst"""
        return [override for override in self.overrides.values() 
                if override['analyst_id'] == analyst_id]

    def get_override_stats(self) -> Dict[str, Any]:
        """Get override statistics"""
        total_overrides = len(self.overrides)
        action_counts = {}
        
        for override in self.overrides.values():
            action = override['action']
            action_counts[action] = action_counts.get(action, 0) + 1
        
        return {
            "total_overrides": total_overrides,
            "action_breakdown": action_counts,
            "recent_overrides": list(self.overrides.values())[-10:]  # Last 10 overrides
        }

    def simulate_auto_review_queue(self) -> None:
        """Simulate adding items to review queue for demo purposes"""
        # Add some demo review items
        demo_items = [
            {
                'event_id': 'demo-001',
                'reason': 'High confidence phishing detection - manual review required',
                'priority': 'high'
            },
            {
                'event_id': 'demo-002', 
                'reason': 'Unusual URL pattern detected',
                'priority': 'medium'
            },
            {
                'event_id': 'demo-003',
                'reason': 'User reported as false positive',
                'priority': 'high'
            },
            {
                'event_id': 'demo-004',
                'reason': 'Low confidence score - needs verification',
                'priority': 'low'
            },
            {
                'event_id': 'demo-005',
                'reason': 'Suspicious attachment detected',
                'priority': 'high'
            }
        ]
        
        for item in demo_items:
            self.add_to_review_queue(
                event_id=item['event_id'],
                reason=item['reason'],
                priority=item['priority']
            )

    def get_review_analytics(self) -> Dict[str, Any]:
        """Get review queue analytics"""
        total_items = len(self.review_queue)
        pending_items = len([item for item in self.review_queue 
                           if item['status'] == ReviewStatus.PENDING.value])
        in_review_items = len([item for item in self.review_queue 
                             if item['status'] == ReviewStatus.IN_REVIEW.value])
        resolved_items = len([item for item in self.review_queue 
                            if item['status'] == ReviewStatus.RESOLVED.value])
        
        priority_breakdown = {}
        for item in self.review_queue:
            priority = item['priority']
            priority_breakdown[priority] = priority_breakdown.get(priority, 0) + 1
        
        return {
            "total_items": total_items,
            "pending_items": pending_items,
            "in_review_items": in_review_items,
            "resolved_items": resolved_items,
            "priority_breakdown": priority_breakdown,
            "average_resolution_time": self._calculate_avg_resolution_time()
        }

    def _calculate_avg_resolution_time(self) -> Optional[float]:
        """Calculate average resolution time in minutes"""
        resolved_items = [item for item in self.review_queue 
                         if item['status'] == ReviewStatus.RESOLVED.value and item['reviewed_at']]
        
        if not resolved_items:
            return None
        
        total_minutes = 0
        for item in resolved_items:
            created_at = datetime.fromisoformat(item['created_at'])
            reviewed_at = datetime.fromisoformat(item['reviewed_at'])
            resolution_time = (reviewed_at - created_at).total_seconds() / 60
            total_minutes += resolution_time
        
        return round(total_minutes / len(resolved_items), 2)