#!/usr/bin/env python3
"""
PhishGuard Pro - Demo Data Generator
Generate deterministic demo campaigns for hackathon presentation
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Set seed for deterministic generation
random.seed(42)

class DemoDataGenerator:
    def __init__(self):
        self.campaigns = [
            {
                "name": "fake-bank",
                "templates": [
                    {
                        "subject": "Urgent: Verify Your Account Immediately",
                        "body": "Dear Customer, Your account has been temporarily suspended due to suspicious activity. Click here to verify your identity and restore access immediately.",
                        "sender_pattern": "security@{bank_domain}",
                        "url_pattern": "https://bit.ly/verify-account-{id}",
                        "final_url_pattern": "https://fake-bank-verification.com/verify?ref={id}",
                        "label": "phishing"
                    },
                    {
                        "subject": "Account Security Alert - Action Required",
                        "body": "We detected unusual login attempts on your account. Please verify your identity to secure your account.",
                        "sender_pattern": "alerts@{bank_domain}",
                        "url_pattern": "https://bit.ly/bank-security-{id}",
                        "final_url_pattern": "https://fake-bank-security.net/verify?token={id}",
                        "label": "phishing"
                    }
                ],
                "domains": ["fake-bank.com", "fake-bank-verification.com", "fake-bank-security.net"]
            },
            {
                "name": "fake-cloud",
                "templates": [
                    {
                        "subject": "Invoice Payment Required",
                        "body": "Your cloud service invoice is overdue. Please update your payment method immediately to avoid service interruption.",
                        "sender_pattern": "billing@{cloud_domain}",
                        "url_pattern": "https://cloud-provider.net/billing/pay?invoice={id}",
                        "final_url_pattern": "https://cloud-provider.net/billing/pay?invoice={id}",
                        "label": "legitimate"
                    },
                    {
                        "subject": "Cloud Storage Quota Exceeded",
                        "body": "Your cloud storage quota has been exceeded. Upgrade your plan to continue using our services.",
                        "sender_pattern": "support@{cloud_domain}",
                        "url_pattern": "https://bit.ly/cloud-upgrade-{id}",
                        "final_url_pattern": "https://fake-cloud-upgrade.com/upgrade?plan={id}",
                        "label": "phishing"
                    }
                ],
                "domains": ["cloud-provider.net", "fake-cloud-upgrade.com"]
            },
            {
                "name": "invoice-scam",
                "templates": [
                    {
                        "subject": "Payment Overdue - Immediate Action Required",
                        "body": "Your invoice #INV-{id} is overdue. Please pay immediately to avoid late fees and service suspension.",
                        "sender_pattern": "billing@invoice-{company}.com",
                        "url_pattern": "https://tinyurl.com/pay-invoice-{id}",
                        "final_url_pattern": "https://fake-invoice-payment.net/pay?invoice={id}",
                        "label": "phishing"
                    },
                    {
                        "subject": "Invoice Payment Confirmation",
                        "body": "Thank you for your payment. Your invoice #INV-{id} has been processed successfully.",
                        "sender_pattern": "receipts@legitimate-company.com",
                        "url_pattern": "https://legitimate-company.com/receipts/{id}",
                        "final_url_pattern": "https://legitimate-company.com/receipts/{id}",
                        "label": "legitimate"
                    }
                ],
                "domains": ["fake-invoice-payment.net", "legitimate-company.com"]
            },
            {
                "name": "microsoft-impersonation",
                "templates": [
                    {
                        "subject": "Your Microsoft Account Has Been Compromised",
                        "body": "We detected suspicious activity on your Microsoft account. Click here to secure it immediately.",
                        "sender_pattern": "support@fake-microsoft.com",
                        "url_pattern": "https://bit.ly/microsoft-security-{id}",
                        "final_url_pattern": "https://fake-microsoft-security.net/secure-account?token={id}",
                        "label": "phishing"
                    },
                    {
                        "subject": "Microsoft 365 Security Update",
                        "body": "Your Microsoft 365 subscription has been updated with new security features. Learn more about the changes.",
                        "sender_pattern": "noreply@microsoft.com",
                        "url_pattern": "https://microsoft.com/security/update-{id}",
                        "final_url_pattern": "https://microsoft.com/security/update-{id}",
                        "label": "legitimate"
                    }
                ],
                "domains": ["fake-microsoft.com", "fake-microsoft-security.net", "microsoft.com"]
            },
            {
                "name": "package-delivery",
                "templates": [
                    {
                        "subject": "Package Delivery Failed",
                        "body": "Your package delivery failed. Click here to reschedule: https://tinyurl.com/reschedule-{id}",
                        "sender_pattern": "delivery@package-service.com",
                        "url_pattern": "https://tinyurl.com/reschedule-{id}",
                        "final_url_pattern": "https://package-delivery-scam.net/reschedule?tracking={id}",
                        "label": "phishing"
                    },
                    {
                        "subject": "Package Delivered Successfully",
                        "body": "Your package has been delivered successfully. Track your next delivery at our website.",
                        "sender_pattern": "noreply@legitimate-delivery.com",
                        "url_pattern": "https://legitimate-delivery.com/track/{id}",
                        "final_url_pattern": "https://legitimate-delivery.com/track/{id}",
                        "label": "legitimate"
                    }
                ],
                "domains": ["package-delivery-scam.net", "legitimate-delivery.com"]
            }
        ]
        
        self.sources = ["email", "sms", "web"]
        self.legitimate_domains = [
            "google.com", "microsoft.com", "apple.com", "amazon.com",
            "cloud-provider.net", "legitimate-company.com", "legitimate-delivery.com"
        ]
    
    def generate_campaigns(self, count: int = 200) -> List[Dict[str, Any]]:
        """Generate demo campaigns"""
        campaigns = []
        
        # Generate 60% legitimate, 40% phishing
        phishing_count = int(count * 0.4)
        legitimate_count = count - phishing_count
        
        # Generate phishing campaigns
        for i in range(phishing_count):
            campaign = self._generate_phishing_campaign(i + 1)
            campaigns.append(campaign)
        
        # Generate legitimate campaigns
        for i in range(legitimate_count):
            campaign = self._generate_legitimate_campaign(i + phishing_count + 1)
            campaigns.append(campaign)
        
        # Shuffle to mix legitimate and phishing
        random.shuffle(campaigns)
        
        return campaigns
    
    def _generate_phishing_campaign(self, campaign_id: int) -> Dict[str, Any]:
        """Generate a phishing campaign"""
        campaign_type = random.choice(self.campaigns)
        template = random.choice(campaign_type["templates"])
        
        # Only use phishing templates
        if template["label"] != "phishing":
            template = next(t for t in campaign_type["templates"] if t["label"] == "phishing")
        
        # Generate unique ID
        unique_id = f"{campaign_id:03d}"
        
        # Select domain
        domain = random.choice(campaign_type["domains"])
        
        # Generate sender
        sender = template["sender_pattern"].format(
            bank_domain=domain,
            cloud_domain=domain,
            company=f"company{random.randint(1, 10)}"
        )
        
        # Generate URLs
        url = template["url_pattern"].format(id=unique_id)
        final_url = template["final_url_pattern"].format(id=unique_id)
        
        # Generate timestamp (last 30 days)
        days_ago = random.randint(0, 30)
        timestamp = datetime.utcnow() - timedelta(days=days_ago)
        
        return {
            "id": f"demo-{unique_id}",
            "timestamp": timestamp.isoformat() + "Z",
            "source": random.choice(self.sources),
            "sender": sender,
            "subject": template["subject"],
            "body": template["body"].format(id=unique_id),
            "url": url,
            "final_url": final_url,
            "whois": self._generate_whois(domain),
            "ssl_cert": self._generate_ssl_cert(domain),
            "label": "phishing"
        }
    
    def _generate_legitimate_campaign(self, campaign_id: int) -> Dict[str, Any]:
        """Generate a legitimate campaign"""
        # Use legitimate domains
        domain = random.choice(self.legitimate_domains)
        
        # Generate legitimate content
        legitimate_templates = [
            {
                "subject": "Security Update Available",
                "body": "A new security update is available for your account. Please update when convenient.",
                "sender": f"security@{domain}",
                "url": f"https://{domain}/security/update",
                "final_url": f"https://{domain}/security/update"
            },
            {
                "subject": "Account Activity Summary",
                "body": "Here's your monthly account activity summary. No action required.",
                "sender": f"noreply@{domain}",
                "url": f"https://{domain}/account/summary",
                "final_url": f"https://{domain}/account/summary"
            },
            {
                "subject": "Service Maintenance Notice",
                "body": "We will be performing scheduled maintenance on our services. Downtime is expected to be minimal.",
                "sender": f"notifications@{domain}",
                "url": f"https://{domain}/maintenance",
                "final_url": f"https://{domain}/maintenance"
            }
        ]
        
        template = random.choice(legitimate_templates)
        
        # Generate timestamp (last 30 days)
        days_ago = random.randint(0, 30)
        timestamp = datetime.utcnow() - timedelta(days=days_ago)
        
        return {
            "id": f"demo-{campaign_id:03d}",
            "timestamp": timestamp.isoformat() + "Z",
            "source": random.choice(self.sources),
            "sender": template["sender"],
            "subject": template["subject"],
            "body": template["body"],
            "url": template["url"],
            "final_url": template["final_url"],
            "whois": self._generate_whois(domain),
            "ssl_cert": self._generate_ssl_cert(domain),
            "label": "legitimate"
        }
    
    def _generate_whois(self, domain: str) -> Dict[str, str]:
        """Generate fake WHOIS data"""
        if any(legit in domain for legit in self.legitimate_domains):
            return {
                "registrar": "Legitimate Registrar Inc",
                "created_date": "2020-01-01T00:00:00Z",
                "expires_date": "2026-01-01T00:00:00Z"
            }
        else:
            return {
                "registrar": "Suspicious Domains LLC",
                "created_date": "2024-01-01T00:00:00Z",
                "expires_date": "2024-12-31T00:00:00Z"
            }
    
    def _generate_ssl_cert(self, domain: str) -> Dict[str, str]:
        """Generate fake SSL certificate data"""
        if any(legit in domain for legit in self.legitimate_domains):
            return {
                "issuer": "Legitimate CA",
                "valid_from": "2024-01-01T00:00:00Z",
                "valid_to": "2025-01-01T00:00:00Z"
            }
        else:
            return {
                "issuer": "Self-Signed",
                "valid_from": "2024-01-01T00:00:00Z",
                "valid_to": "2024-12-31T00:00:00Z"
            }

def main():
    """Generate demo campaigns and save to JSON"""
    generator = DemoDataGenerator()
    campaigns = generator.generate_campaigns(200)
    
    # Save to file
    with open('/workspace/data/demo_campaigns.json', 'w') as f:
        json.dump(campaigns, f, indent=2)
    
    # Print summary
    phishing_count = sum(1 for c in campaigns if c['label'] == 'phishing')
    legitimate_count = len(campaigns) - phishing_count
    
    print(f"Generated {len(campaigns)} demo campaigns:")
    print(f"  - Phishing: {phishing_count}")
    print(f"  - Legitimate: {legitimate_count}")
    print(f"  - Saved to: /workspace/data/demo_campaigns.json")

if __name__ == "__main__":
    main()