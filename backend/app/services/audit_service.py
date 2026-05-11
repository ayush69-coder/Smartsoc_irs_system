"""
Audit Service - Handles audit logging with PII masking
"""
import json
import re
import hashlib
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class AuditAction(Enum):
    VERDICT_CREATED = "verdict_created"
    VERDICT_OVERRIDDEN = "verdict_overridden"
    POLICY_CREATED = "policy_created"
    POLICY_UPDATED = "policy_updated"
    POLICY_DELETED = "policy_deleted"
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    REVIEW_ASSIGNED = "review_assigned"
    REVIEW_RESOLVED = "review_resolved"
    SANDBOX_SUBMITTED = "sandbox_submitted"
    CAMPAIGN_TRIGGERED = "campaign_triggered"
    SETTINGS_UPDATED = "settings_updated"


class AuditService:
    def __init__(self):
        self.audit_logs = []
        self.pii_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',
            'ssn': r'\b\d{3}-?\d{2}-?\d{4}\b',
            'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            'ip_address': r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        }
        self.salt = "phishguard_audit_salt_2024"

    def log_action(self, action: str, actor: str, event_id: Optional[str] = None, 
                   details: Optional[Dict[str, Any]] = None, severity: str = "info") -> str:
        """Log an audit action with PII masking"""
        audit_id = f"audit_{int(time.time())}_{len(self.audit_logs)}"
        
        # Mask PII in details
        masked_details = self._mask_pii(details or {})
        
        audit_entry = {
            'id': audit_id,
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'actor': actor,
            'event_id': event_id,
            'details': masked_details,
            'severity': severity,
            'ip_address': self._get_hashed_ip(actor),  # Hash IP for privacy
            'session_id': self._generate_session_id(actor)
        }
        
        self.audit_logs.append(audit_entry)
        
        # In a real system, this would be written to a secure audit database
        self._write_to_audit_file(audit_entry)
        
        return audit_id

    def _mask_pii(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Mask PII in data dictionary"""
        if not isinstance(data, dict):
            return data
        
        masked_data = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                masked_data[key] = self._mask_string_pii(value)
            elif isinstance(value, dict):
                masked_data[key] = self._mask_pii(value)
            elif isinstance(value, list):
                masked_data[key] = [self._mask_pii(item) if isinstance(item, dict) 
                                  else self._mask_string_pii(item) if isinstance(item, str) 
                                  else item for item in value]
            else:
                masked_data[key] = value
        
        return masked_data

    def _mask_string_pii(self, text: str) -> str:
        """Mask PII in a string"""
        if not isinstance(text, str):
            return text
        
        masked_text = text
        
        # Mask email addresses
        masked_text = re.sub(
            self.pii_patterns['email'], 
            lambda m: self._mask_email(m.group(0)), 
            masked_text
        )
        
        # Mask phone numbers
        masked_text = re.sub(
            self.pii_patterns['phone'], 
            lambda m: self._mask_phone(m.group(0)), 
            masked_text
        )
        
        # Mask SSNs
        masked_text = re.sub(
            self.pii_patterns['ssn'], 
            lambda m: self._mask_ssn(m.group(0)), 
            masked_text
        )
        
        # Mask credit card numbers
        masked_text = re.sub(
            self.pii_patterns['credit_card'], 
            lambda m: self._mask_credit_card(m.group(0)), 
            masked_text
        )
        
        # Mask IP addresses (but keep local IPs for debugging)
        masked_text = re.sub(
            self.pii_patterns['ip_address'], 
            lambda m: self._mask_ip_address(m.group(0)), 
            masked_text
        )
        
        return masked_text

    def _mask_email(self, email: str) -> str:
        """Mask email address: j***@d***.com"""
        if '@' not in email:
            return email
        
        local, domain = email.split('@', 1)
        if len(local) <= 2:
            masked_local = local[0] + '*' * (len(local) - 1)
        else:
            masked_local = local[0] + '*' * (len(local) - 2) + local[-1]
        
        domain_parts = domain.split('.')
        if len(domain_parts) >= 2:
            masked_domain = domain_parts[0][0] + '*' * (len(domain_parts[0]) - 1) + '.' + '.'.join(domain_parts[1:])
        else:
            masked_domain = domain
        
        return f"{masked_local}@{masked_domain}"

    def _mask_phone(self, phone: str) -> str:
        """Mask phone number: (555) ***-****"""
        digits = re.sub(r'[^\d]', '', phone)
        if len(digits) == 10:
            return f"({digits[:3]}) ***-{digits[-4:]}"
        elif len(digits) == 11 and digits[0] == '1':
            return f"+1 ({digits[1:4]}) ***-{digits[-4:]}"
        else:
            return "***-***-****"

    def _mask_ssn(self, ssn: str) -> str:
        """Mask SSN: ***-**-1234"""
        digits = re.sub(r'[^\d]', '', ssn)
        if len(digits) == 9:
            return f"***-**-{digits[-4:]}"
        else:
            return "***-**-****"

    def _mask_credit_card(self, card: str) -> str:
        """Mask credit card: ****-****-****-1234"""
        digits = re.sub(r'[^\d]', '', card)
        if len(digits) >= 4:
            return f"****-****-****-{digits[-4:]}"
        else:
            return "****-****-****-****"

    def _mask_ip_address(self, ip: str) -> str:
        """Mask IP address: 192.168.***.***"""
        parts = ip.split('.')
        if len(parts) == 4:
            # Keep first two octets for network identification, mask last two
            return f"{parts[0]}.{parts[1]}.***.***"
        else:
            return "***.***.***.***"

    def _get_hashed_ip(self, actor: str) -> str:
        """Get hashed IP address for privacy"""
        # In a real system, this would get the actual IP from the request
        # For demo purposes, we'll generate a consistent hash
        return hashlib.sha256(f"{actor}_{self.salt}".encode()).hexdigest()[:16]

    def _generate_session_id(self, actor: str) -> str:
        """Generate session ID for tracking"""
        return hashlib.sha256(f"{actor}_{int(time.time())}_{self.salt}".encode()).hexdigest()[:12]

    def _write_to_audit_file(self, audit_entry: Dict[str, Any]) -> None:
        """Write audit entry to file (in production, this would go to a secure database)"""
        try:
            with open('/workspace/data/audit.json', 'a') as f:
                f.write(json.dumps(audit_entry) + '\n')
        except Exception as e:
            print(f"Error writing audit log: {e}")

    def get_audit_logs(self, limit: int = 100, offset: int = 0, 
                      action: Optional[str] = None, actor: Optional[str] = None) -> Dict[str, Any]:
        """Get audit logs with filtering"""
        filtered_logs = self.audit_logs
        
        if action:
            filtered_logs = [log for log in filtered_logs if log['action'] == action]
        
        if actor:
            filtered_logs = [log for log in filtered_logs if log['actor'] == actor]
        
        # Sort by timestamp (newest first)
        filtered_logs.sort(key=lambda x: x['timestamp'], reverse=True)
        
        # Apply pagination
        total_count = len(filtered_logs)
        paginated_logs = filtered_logs[offset:offset + limit]
        
        return {
            'logs': paginated_logs,
            'total_count': total_count,
            'limit': limit,
            'offset': offset,
            'has_more': offset + limit < total_count
        }

    def get_audit_stats(self) -> Dict[str, Any]:
        """Get audit statistics"""
        total_logs = len(self.audit_logs)
        
        # Count by action
        action_counts = {}
        for log in self.audit_logs:
            action = log['action']
            action_counts[action] = action_counts.get(action, 0) + 1
        
        # Count by actor
        actor_counts = {}
        for log in self.audit_logs:
            actor = log['actor']
            actor_counts[actor] = actor_counts.get(actor, 0) + 1
        
        # Count by severity
        severity_counts = {}
        for log in self.audit_logs:
            severity = log['severity']
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        return {
            'total_logs': total_logs,
            'action_breakdown': action_counts,
            'actor_breakdown': actor_counts,
            'severity_breakdown': severity_counts,
            'recent_activity': self.audit_logs[-10:] if self.audit_logs else []
        }

    def search_audit_logs(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Search audit logs by query"""
        query_lower = query.lower()
        matching_logs = []
        
        for log in self.audit_logs:
            # Search in action, actor, and details
            if (query_lower in log['action'].lower() or 
                query_lower in log['actor'].lower() or
                query_lower in str(log['details']).lower()):
                matching_logs.append(log)
        
        return matching_logs[:limit]

    def simulate_audit_events(self) -> None:
        """Simulate some audit events for demo purposes"""
        demo_events = [
            {
                'action': AuditAction.VERDICT_CREATED.value,
                'actor': 'system@phishguard.com',
                'event_id': 'demo-001',
                'details': {'score': 0.85, 'action': 'block', 'url': 'https://fake-bank.com'},
                'severity': 'info'
            },
            {
                'action': AuditAction.USER_LOGIN.value,
                'actor': 'analyst@company.com',
                'event_id': None,
                'details': {'login_method': 'password', 'ip': '192.168.1.100'},
                'severity': 'info'
            },
            {
                'action': AuditAction.VERDICT_OVERRIDDEN.value,
                'actor': 'analyst@company.com',
                'event_id': 'demo-001',
                'details': {'original_action': 'block', 'new_action': 'allow', 'reason': 'False positive'},
                'severity': 'warning'
            },
            {
                'action': AuditAction.POLICY_CREATED.value,
                'actor': 'admin@company.com',
                'event_id': None,
                'details': {'policy_name': 'High Risk Block', 'policy_type': 'score_threshold'},
                'severity': 'info'
            },
            {
                'action': AuditAction.CAMPAIGN_TRIGGERED.value,
                'actor': 'demo@phishguard.com',
                'event_id': None,
                'details': {'campaign_id': 'fake-bank', 'intensity': 5, 'events_generated': 10},
                'severity': 'info'
            }
        ]
        
        for event in demo_events:
            self.log_action(
                action=event['action'],
                actor=event['actor'],
                event_id=event['event_id'],
                details=event['details'],
                severity=event['severity']
            )