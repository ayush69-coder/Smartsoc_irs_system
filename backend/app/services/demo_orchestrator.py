"""
Demo Orchestrator Service - Triggers crafted campaigns for demo purposes
"""
import json
import time
import random
from typing import Dict, List, Any
from datetime import datetime, timedelta


class DemoOrchestrator:
    def __init__(self):
        self.active_campaigns = {}
        self.campaign_templates = {
            'fake-bank': {
                'name': 'Fake Bank Verification Campaign',
                'description': 'Simulates banking phishing attempts',
                'events_per_minute': 5,
                'duration_minutes': 10,
                'templates': [
                    {
                        'subject': 'Urgent: Verify Your Account',
                        'sender': 'security@bank-verification.com',
                        'body': 'Your account has been flagged for suspicious activity. Please verify your identity immediately.',
                        'url': 'https://fake-bank-verification.com/verify',
                        'final_url': 'https://fake-bank-verification.com/verify',
                        'label': 'phishing',
                        'score': 0.85
                    },
                    {
                        'subject': 'Account Suspension Notice',
                        'sender': 'noreply@bank-security.com',
                        'body': 'Your account will be suspended in 24 hours unless you verify your information.',
                        'url': 'https://bank-security-alert.com/suspend',
                        'final_url': 'https://bank-security-alert.com/suspend',
                        'label': 'phishing',
                        'score': 0.90
                    }
                ]
            },
            'fake-cloud': {
                'name': 'Fake Cloud Storage Campaign',
                'description': 'Simulates cloud service phishing attempts',
                'events_per_minute': 3,
                'duration_minutes': 8,
                'templates': [
                    {
                        'subject': 'Your Storage is Almost Full',
                        'sender': 'storage@cloud-service.com',
                        'body': 'Upgrade your storage plan to avoid losing your files.',
                        'url': 'https://fake-cloud-storage.com/upgrade',
                        'final_url': 'https://fake-cloud-storage.com/upgrade',
                        'label': 'phishing',
                        'score': 0.75
                    },
                    {
                        'subject': 'Security Alert: Unusual Activity',
                        'sender': 'security@cloud-provider.com',
                        'body': 'We detected unusual activity in your cloud account. Please review immediately.',
                        'url': 'https://cloud-security-alert.net/review',
                        'final_url': 'https://cloud-security-alert.net/review',
                        'label': 'phishing',
                        'score': 0.80
                    }
                ]
            },
            'invoice-scam': {
                'name': 'Invoice Scam Campaign',
                'description': 'Simulates invoice and payment phishing attempts',
                'events_per_minute': 4,
                'duration_minutes': 6,
                'templates': [
                    {
                        'subject': 'Payment Overdue - Immediate Action Required',
                        'sender': 'billing@invoice-service.com',
                        'body': 'Your payment is overdue. Please pay immediately to avoid service interruption.',
                        'url': 'https://invoice-payment-scam.com/pay',
                        'final_url': 'https://invoice-payment-scam.com/pay',
                        'label': 'phishing',
                        'score': 0.70
                    },
                    {
                        'subject': 'Invoice #INV-2024-001',
                        'sender': 'accounts@billing-system.com',
                        'body': 'Please find attached invoice for services rendered.',
                        'url': 'https://fake-invoice-system.com/view/INV-2024-001',
                        'final_url': 'https://fake-invoice-system.com/view/INV-2024-001',
                        'label': 'phishing',
                        'score': 0.65
                    }
                ]
            },
            'microsoft-impersonation': {
                'name': 'Microsoft Impersonation Campaign',
                'description': 'Simulates Microsoft security alerts and updates',
                'events_per_minute': 6,
                'duration_minutes': 12,
                'templates': [
                    {
                        'subject': 'Security Update Required',
                        'sender': 'security@microsoft-update.com',
                        'body': 'Critical security update available. Install immediately to protect your account.',
                        'url': 'https://microsoft-security-update.net/install',
                        'final_url': 'https://microsoft-security-update.net/install',
                        'label': 'phishing',
                        'score': 0.88
                    },
                    {
                        'subject': 'Account Verification Needed',
                        'sender': 'noreply@microsoft-account.com',
                        'body': 'Your Microsoft account needs verification. Click here to verify.',
                        'url': 'https://microsoft-account-verify.com/verify',
                        'final_url': 'https://microsoft-account-verify.com/verify',
                        'label': 'phishing',
                        'score': 0.82
                    }
                ]
            },
            'package-delivery': {
                'name': 'Package Delivery Campaign',
                'description': 'Simulates package delivery and tracking phishing attempts',
                'events_per_minute': 2,
                'duration_minutes': 5,
                'templates': [
                    {
                        'subject': 'Package Delivery Failed',
                        'sender': 'delivery@package-service.com',
                        'body': 'Your package delivery failed. Please reschedule delivery.',
                        'url': 'https://package-delivery-reschedule.com/reschedule',
                        'final_url': 'https://package-delivery-reschedule.com/reschedule',
                        'label': 'phishing',
                        'score': 0.60
                    },
                    {
                        'subject': 'Track Your Package',
                        'sender': 'tracking@shipping-service.com',
                        'body': 'Your package is ready for delivery. Track your shipment.',
                        'url': 'https://package-tracking-scam.com/track',
                        'final_url': 'https://package-tracking-scam.com/track',
                        'label': 'phishing',
                        'score': 0.55
                    }
                ]
            }
        }

    def trigger_campaign(self, campaign_id: str, intensity: int = 5) -> Dict[str, Any]:
        """Trigger a demo campaign with specified intensity"""
        if campaign_id not in self.campaign_templates:
            return {"error": f"Campaign '{campaign_id}' not found"}
        
        campaign_template = self.campaign_templates[campaign_id]
        campaign_instance_id = f"{campaign_id}_{int(time.time())}"
        
        # Calculate campaign parameters based on intensity (1-10)
        intensity_factor = intensity / 10.0
        events_per_minute = max(1, int(campaign_template['events_per_minute'] * intensity_factor))
        duration_minutes = max(1, int(campaign_template['duration_minutes'] * intensity_factor))
        
        campaign = {
            'id': campaign_instance_id,
            'campaign_id': campaign_id,
            'name': campaign_template['name'],
            'description': campaign_template['description'],
            'intensity': intensity,
            'events_per_minute': events_per_minute,
            'duration_minutes': duration_minutes,
            'status': 'running',
            'started_at': datetime.now().isoformat(),
            'events_generated': 0,
            'templates': campaign_template['templates']
        }
        
        self.active_campaigns[campaign_instance_id] = campaign
        
        return {
            "campaign_instance_id": campaign_instance_id,
            "campaign_name": campaign_template['name'],
            "intensity": intensity,
            "events_per_minute": events_per_minute,
            "duration_minutes": duration_minutes,
            "status": "started",
            "message": f"Campaign '{campaign_template['name']}' started with intensity {intensity}"
        }

    def generate_campaign_events(self, campaign_instance_id: str) -> List[Dict[str, Any]]:
        """Generate events for a running campaign"""
        if campaign_instance_id not in self.active_campaigns:
            return []
        
        campaign = self.active_campaigns[campaign_instance_id]
        
        if campaign['status'] != 'running':
            return []
        
        # Check if campaign should still be running
        started_at = datetime.fromisoformat(campaign['started_at'])
        elapsed_minutes = (datetime.now() - started_at).total_seconds() / 60
        
        if elapsed_minutes >= campaign['duration_minutes']:
            campaign['status'] = 'completed'
            return []
        
        # Generate events for this minute
        events_to_generate = campaign['events_per_minute']
        events = []
        
        for _ in range(events_to_generate):
            template = random.choice(campaign['templates'])
            
            # Add some variation to the template
            event = self._create_event_from_template(template, campaign['campaign_id'])
            events.append(event)
            campaign['events_generated'] += 1
        
        return events

    def _create_event_from_template(self, template: Dict[str, Any], campaign_id: str) -> Dict[str, Any]:
        """Create an event from a template with some variation"""
        event_id = f"demo-{int(time.time())}-{random.randint(1000, 9999)}"
        
        # Add some variation to the score
        base_score = template['score']
        score_variation = random.uniform(-0.1, 0.1)
        final_score = max(0.0, min(1.0, base_score + score_variation))
        
        # Determine action based on score
        if final_score >= 0.8:
            action = 'block'
        elif final_score >= 0.5:
            action = 'warn'
        else:
            action = 'allow'
        
        # Add some variation to the URL
        base_url = template['url']
        if random.random() < 0.3:  # 30% chance of URL variation
            base_url = base_url.replace('.com', f'-{random.randint(1, 999)}.com')
        
        return {
            'id': event_id,
            'timestamp': datetime.now().isoformat(),
            'source': random.choice(['email', 'sms', 'web']),
            'sender': template['sender'],
            'subject': template['subject'],
            'body': template['body'],
            'url': base_url,
            'final_url': base_url,
            'label': template['label'],
            'score': final_score,
            'action': action,
            'campaign_id': campaign_id,
            'whois': {
                'registrar': 'Fake Registrar Inc.',
                'created_date': '2024-01-15',
                'expiry_date': '2025-01-15',
                'nameservers': ['ns1.fake-registrar.com', 'ns2.fake-registrar.com']
            },
            'ssl_cert': {
                'issuer': 'Fake Certificate Authority',
                'valid_from': '2024-01-01',
                'valid_to': '2025-01-01',
                'subject': f'CN={base_url.split("//")[1].split("/")[0]}'
            }
        }

    def get_campaign_status(self, campaign_instance_id: str) -> Dict[str, Any]:
        """Get status of a campaign"""
        if campaign_instance_id not in self.active_campaigns:
            return {"error": "Campaign not found"}
        
        campaign = self.active_campaigns[campaign_instance_id]
        
        # Update status if campaign should be completed
        started_at = datetime.fromisoformat(campaign['started_at'])
        elapsed_minutes = (datetime.now() - started_at).total_seconds() / 60
        
        if elapsed_minutes >= campaign['duration_minutes'] and campaign['status'] == 'running':
            campaign['status'] = 'completed'
        
        return {
            'campaign_instance_id': campaign_instance_id,
            'status': campaign['status'],
            'events_generated': campaign['events_generated'],
            'elapsed_minutes': round(elapsed_minutes, 2),
            'remaining_minutes': max(0, campaign['duration_minutes'] - elapsed_minutes)
        }

    def list_active_campaigns(self) -> List[Dict[str, Any]]:
        """List all active campaigns"""
        return list(self.active_campaigns.values())

    def stop_campaign(self, campaign_instance_id: str) -> Dict[str, Any]:
        """Stop a running campaign"""
        if campaign_instance_id not in self.active_campaigns:
            return {"error": "Campaign not found"}
        
        campaign = self.active_campaigns[campaign_instance_id]
        campaign['status'] = 'stopped'
        
        return {
            "campaign_instance_id": campaign_instance_id,
            "status": "stopped",
            "message": f"Campaign '{campaign['name']}' stopped"
        }