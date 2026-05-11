"""
PhishGuard Pro - Render Service
Page rendering with Playwright fallback for demo
"""

import base64
import json
import os
from typing import Dict, Any, Optional
from urllib.parse import urlparse
from visual_detector import VisualDetector

class RenderService:
    def __init__(self):
        self.demo_domains = [
            'fake-bank-verification.com',
            'package-delivery-scam.net',
            'fake-microsoft-security.net',
            'malicious-site.net',
            'scam-site.com'
        ]
        self.sample_screenshot = self._load_sample_screenshot()
        self.visual_detector = VisualDetector()
    
    def _load_sample_screenshot(self) -> str:
        """Load sample screenshot for demo fallback"""
        try:
            with open('/workspace/data/renders/sample.png', 'rb') as f:
                return base64.b64encode(f.read()).decode('utf-8')
        except FileNotFoundError:
            # Create a minimal 1x1 pixel PNG as fallback
            return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
    
    def render_page(self, url: str) -> Dict[str, Any]:
        """Render page and return screenshot + DOM"""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        # Check if it's a demo domain
        if not any(demo_domain in domain for demo_domain in self.demo_domains):
            dom = self._generate_demo_dom(url, "Non-demo domain - using fallback")
            title = "Demo Fallback"
            status = "fallback"
        else:
            # For demo domains, generate realistic content
            render_result = self._generate_demo_render(url, domain)
            dom = render_result["dom"]
            title = render_result["title"]
            status = render_result["status"]
        
        # Perform visual analysis
        visual_analysis = self.visual_detector.analyze_visual(url, title, dom)
        
        return {
            "screenshot": self.sample_screenshot,
            "dom": dom,
            "title": title,
            "status": status,
            "visual_analysis": visual_analysis
        }
    
    def _generate_demo_render(self, url: str, domain: str) -> Dict[str, Any]:
        """Generate demo render for known demo domains"""
        if 'fake-bank' in domain:
            return {
                "screenshot": self.sample_screenshot,
                "dom": self._generate_bank_dom(url),
                "title": "Bank Security Verification",
                "status": "rendered"
            }
        elif 'microsoft' in domain:
            return {
                "screenshot": self.sample_screenshot,
                "dom": self._generate_microsoft_dom(url),
                "title": "Microsoft Account Security",
                "status": "rendered"
            }
        elif 'package' in domain:
            return {
                "screenshot": self.sample_screenshot,
                "dom": self._generate_package_dom(url),
                "title": "Package Delivery Service",
                "status": "rendered"
            }
        else:
            return {
                "screenshot": self.sample_screenshot,
                "dom": self._generate_demo_dom(url, "Suspicious website detected"),
                "title": "Suspicious Site",
                "status": "rendered"
            }
    
    def _generate_bank_dom(self, url: str) -> Dict[str, Any]:
        """Generate DOM for fake bank site"""
        return {
            "html": {
                "tag": "html",
                "attributes": {"lang": "en"},
                "children": [
                    {
                        "tag": "head",
                        "children": [
                            {"tag": "title", "text": "Bank Security Verification"},
                            {"tag": "meta", "attributes": {"charset": "utf-8"}}
                        ]
                    },
                    {
                        "tag": "body",
                        "attributes": {"style": "font-family: Arial, sans-serif; margin: 40px;"},
                        "children": [
                            {
                                "tag": "div",
                                "attributes": {"class": "header"},
                                "children": [
                                    {"tag": "h1", "text": "Security Alert - Account Verification Required"},
                                    {"tag": "p", "text": "Your account has been temporarily suspended due to suspicious activity."}
                                ]
                            },
                            {
                                "tag": "form",
                                "attributes": {"action": "/verify", "method": "post"},
                                "children": [
                                    {"tag": "input", "attributes": {"type": "text", "placeholder": "Account Number"}},
                                    {"tag": "input", "attributes": {"type": "password", "placeholder": "Password"}},
                                    {"tag": "button", "text": "Verify Account Now"}
                                ]
                            }
                        ]
                    }
                ]
            },
            "text_content": "Bank Security Verification - Your account has been temporarily suspended due to suspicious activity. Account Number Password Verify Account Now",
            "links": ["/verify", "/help", "/contact"],
            "forms": [{"action": "/verify", "method": "post", "inputs": 2}]
        }
    
    def _generate_microsoft_dom(self, url: str) -> Dict[str, Any]:
        """Generate DOM for fake Microsoft site"""
        return {
            "html": {
                "tag": "html",
                "attributes": {"lang": "en"},
                "children": [
                    {
                        "tag": "head",
                        "children": [
                            {"tag": "title", "text": "Microsoft Account Security"},
                            {"tag": "meta", "attributes": {"charset": "utf-8"}}
                        ]
                    },
                    {
                        "tag": "body",
                        "attributes": {"style": "font-family: Segoe UI, sans-serif; margin: 40px;"},
                        "children": [
                            {
                                "tag": "div",
                                "attributes": {"class": "header"},
                                "children": [
                                    {"tag": "h1", "text": "Microsoft Account Security Alert"},
                                    {"tag": "p", "text": "We detected suspicious activity on your Microsoft account."}
                                ]
                            },
                            {
                                "tag": "form",
                                "attributes": {"action": "/secure", "method": "post"},
                                "children": [
                                    {"tag": "input", "attributes": {"type": "email", "placeholder": "Email Address"}},
                                    {"tag": "input", "attributes": {"type": "password", "placeholder": "Password"}},
                                    {"tag": "button", "text": "Secure Account"}
                                ]
                            }
                        ]
                    }
                ]
            },
            "text_content": "Microsoft Account Security Alert - We detected suspicious activity on your Microsoft account. Email Address Password Secure Account",
            "links": ["/secure", "/help", "/privacy"],
            "forms": [{"action": "/secure", "method": "post", "inputs": 2}]
        }
    
    def _generate_package_dom(self, url: str) -> Dict[str, Any]:
        """Generate DOM for fake package delivery site"""
        return {
            "html": {
                "tag": "html",
                "attributes": {"lang": "en"},
                "children": [
                    {
                        "tag": "head",
                        "children": [
                            {"tag": "title", "text": "Package Delivery Service"},
                            {"tag": "meta", "attributes": {"charset": "utf-8"}}
                        ]
                    },
                    {
                        "tag": "body",
                        "attributes": {"style": "font-family: Arial, sans-serif; margin: 40px;"},
                        "children": [
                            {
                                "tag": "div",
                                "attributes": {"class": "header"},
                                "children": [
                                    {"tag": "h1", "text": "Package Delivery Failed"},
                                    {"tag": "p", "text": "Your package delivery failed. Please reschedule to avoid additional fees."}
                                ]
                            },
                            {
                                "tag": "form",
                                "attributes": {"action": "/reschedule", "method": "post"},
                                "children": [
                                    {"tag": "input", "attributes": {"type": "text", "placeholder": "Tracking Number"}},
                                    {"tag": "input", "attributes": {"type": "text", "placeholder": "Phone Number"}},
                                    {"tag": "button", "text": "Reschedule Delivery"}
                                ]
                            }
                        ]
                    }
                ]
            },
            "text_content": "Package Delivery Failed - Your package delivery failed. Please reschedule to avoid additional fees. Tracking Number Phone Number Reschedule Delivery",
            "links": ["/reschedule", "/track", "/contact"],
            "forms": [{"action": "/reschedule", "method": "post", "inputs": 2}]
        }
    
    def _generate_demo_dom(self, url: str, message: str) -> Dict[str, Any]:
        """Generate generic demo DOM"""
        return {
            "html": {
                "tag": "html",
                "attributes": {"lang": "en"},
                "children": [
                    {
                        "tag": "head",
                        "children": [
                            {"tag": "title", "text": "Demo Site"},
                            {"tag": "meta", "attributes": {"charset": "utf-8"}}
                        ]
                    },
                    {
                        "tag": "body",
                        "attributes": {"style": "font-family: Arial, sans-serif; margin: 40px;"},
                        "children": [
                            {
                                "tag": "div",
                                "attributes": {"class": "content"},
                                "children": [
                                    {"tag": "h1", "text": "Demo Website"},
                                    {"tag": "p", "text": message}
                                ]
                            }
                        ]
                    }
                ]
            },
            "text_content": f"Demo Website - {message}",
            "links": ["/", "/about", "/contact"],
            "forms": []
        }