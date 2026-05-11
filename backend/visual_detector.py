"""
PhishGuard Pro - Visual Detector
Heuristic visual analysis for brand impersonation detection
"""

import re
from typing import Dict, Any, List
from urllib.parse import urlparse

class VisualDetector:
    def __init__(self):
        self.brand_keywords = {
            'microsoft': ['microsoft', 'office', 'outlook', 'azure', 'windows'],
            'google': ['google', 'gmail', 'youtube', 'chrome', 'android'],
            'apple': ['apple', 'iphone', 'ipad', 'mac', 'icloud'],
            'amazon': ['amazon', 'aws', 'prime', 'kindle'],
            'facebook': ['facebook', 'meta', 'instagram', 'whatsapp'],
            'paypal': ['paypal', 'venmo'],
            'bank': ['bank', 'chase', 'wells', 'bofa', 'citibank', 'banking'],
            'cloud': ['cloud', 'aws', 'azure', 'gcp', 'digitalocean']
        }
        
        self.suspicious_indicators = [
            'fake-', 'suspicious-', 'malicious-', 'scam-',
            'phishing-', 'fraud-', 'spam-', 'clone-',
            'copy-', 'imitation-', 'lookalike-'
        ]
        
        self.visual_cues = {
            'logo_mismatch': 0.8,
            'layout_anomalies': 0.6,
            'color_scheme_similarity': 0.4,
            'font_consistency': 0.3,
            'button_placement': 0.5,
            'brand_name_variations': 0.7,
            'domain_mismatch': 0.9
        }
    
    def analyze_visual(self, url: str, title: str, dom: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze visual elements for impersonation"""
        domain = urlparse(url).netloc.lower()
        
        # Calculate impersonation score
        impersonation_score = self._calculate_impersonation_score(domain, title, dom)
        
        # Extract visual cues
        visual_cues = self._extract_visual_cues(domain, title, dom)
        
        # Determine if it's impersonation
        is_impersonation = impersonation_score > 0.6
        
        return {
            'impersonation_score': impersonation_score,
            'is_impersonation': is_impersonation,
            'visual_cues': visual_cues,
            'confidence': min(impersonation_score * 1.2, 1.0),
            'brand_detected': self._detect_brand(domain, title),
            'suspicious_domain': self._is_suspicious_domain(domain)
        }
    
    def _calculate_impersonation_score(self, domain: str, title: str, dom: Dict[str, Any]) -> float:
        """Calculate impersonation score based on various factors"""
        score = 0.0
        
        # Domain analysis
        if self._is_suspicious_domain(domain):
            score += 0.3
        
        # Brand name variations in domain
        brand_variations = self._check_brand_variations(domain)
        score += brand_variations * 0.2
        
        # Title analysis
        title_score = self._analyze_title(title)
        score += title_score * 0.2
        
        # DOM analysis
        dom_score = self._analyze_dom(dom)
        score += dom_score * 0.3
        
        return min(score, 1.0)
    
    def _extract_visual_cues(self, domain: str, title: str, dom: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract specific visual cues"""
        cues = []
        
        # Check for logo mismatch
        if self._check_logo_mismatch(domain, title):
            cues.append({
                'type': 'logo_mismatch',
                'description': 'Logo does not match expected brand',
                'confidence': 0.8
            })
        
        # Check for layout anomalies
        if self._check_layout_anomalies(dom):
            cues.append({
                'type': 'layout_anomalies',
                'description': 'Unusual layout patterns detected',
                'confidence': 0.6
            })
        
        # Check for brand name variations
        brand_variations = self._check_brand_variations(domain)
        if brand_variations > 0.5:
            cues.append({
                'type': 'brand_name_variations',
                'description': 'Domain contains brand name variations',
                'confidence': brand_variations
            })
        
        # Check for domain mismatch
        if self._check_domain_mismatch(domain, title):
            cues.append({
                'type': 'domain_mismatch',
                'description': 'Domain does not match expected brand domain',
                'confidence': 0.9
            })
        
        return cues
    
    def _is_suspicious_domain(self, domain: str) -> bool:
        """Check if domain appears suspicious"""
        return any(indicator in domain for indicator in self.suspicious_indicators)
    
    def _detect_brand(self, domain: str, title: str) -> str:
        """Detect which brand is being impersonated"""
        text = f"{domain} {title}".lower()
        
        for brand, keywords in self.brand_keywords.items():
            if any(keyword in text for keyword in keywords):
                return brand
        
        return "unknown"
    
    def _check_brand_variations(self, domain: str) -> float:
        """Check for brand name variations in domain"""
        domain_lower = domain.lower()
        variations = 0
        
        for brand, keywords in self.brand_keywords.items():
            for keyword in keywords:
                if keyword in domain_lower:
                    # Check for variations
                    if f"fake-{keyword}" in domain_lower:
                        variations += 0.8
                    elif f"{keyword}-fake" in domain_lower:
                        variations += 0.8
                    elif f"{keyword}-security" in domain_lower:
                        variations += 0.6
                    elif f"{keyword}-verification" in domain_lower:
                        variations += 0.6
                    else:
                        variations += 0.2
        
        return min(variations, 1.0)
    
    def _analyze_title(self, title: str) -> float:
        """Analyze page title for impersonation indicators"""
        title_lower = title.lower()
        score = 0.0
        
        # Check for urgency words
        urgency_words = ['urgent', 'immediately', 'verify', 'suspended', 'compromised']
        urgency_count = sum(1 for word in urgency_words if word in title_lower)
        score += urgency_count * 0.1
        
        # Check for brand names
        for brand, keywords in self.brand_keywords.items():
            if any(keyword in title_lower for keyword in keywords):
                score += 0.2
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r'verify\s+your\s+account',
            r'security\s+alert',
            r'account\s+suspended',
            r'immediate\s+action'
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, title_lower):
                score += 0.3
        
        return min(score, 1.0)
    
    def _analyze_dom(self, dom: Dict[str, Any]) -> float:
        """Analyze DOM structure for impersonation indicators"""
        score = 0.0
        
        if not dom or 'html' not in dom:
            return score
        
        # Check for suspicious form patterns
        if 'forms' in dom and dom['forms']:
            for form in dom['forms']:
                if 'action' in form and 'verify' in form['action'].lower():
                    score += 0.2
                if 'action' in form and 'secure' in form['action'].lower():
                    score += 0.2
        
        # Check for suspicious links
        if 'links' in dom and dom['links']:
            for link in dom['links']:
                if any(suspicious in link.lower() for suspicious in ['verify', 'secure', 'urgent']):
                    score += 0.1
        
        # Check for suspicious text content
        if 'text_content' in dom:
            text = dom['text_content'].lower()
            suspicious_phrases = [
                'verify your identity',
                'account suspended',
                'immediate action required',
                'click here to secure'
            ]
            
            for phrase in suspicious_phrases:
                if phrase in text:
                    score += 0.1
        
        return min(score, 1.0)
    
    def _check_logo_mismatch(self, domain: str, title: str) -> bool:
        """Check for logo mismatch (simplified heuristic)"""
        # In a real implementation, this would analyze actual logo images
        # For demo, we'll use domain-title mismatch as a proxy
        brand_detected = self._detect_brand(domain, title)
        if brand_detected != "unknown":
            # Check if domain matches expected brand domain
            expected_domains = {
                'microsoft': ['microsoft.com', 'office.com'],
                'google': ['google.com', 'gmail.com'],
                'apple': ['apple.com', 'icloud.com'],
                'amazon': ['amazon.com', 'aws.amazon.com']
            }
            
            if brand_detected in expected_domains:
                return not any(expected in domain for expected in expected_domains[brand_detected])
        
        return False
    
    def _check_layout_anomalies(self, dom: Dict[str, Any]) -> bool:
        """Check for layout anomalies (simplified heuristic)"""
        if not dom or 'html' not in dom:
            return False
        
        # Check for unusual form patterns
        if 'forms' in dom and dom['forms']:
            for form in dom['forms']:
                if 'inputs' in form and form['inputs'] > 5:
                    return True  # Unusually many inputs
        
        return False
    
    def _check_domain_mismatch(self, domain: str, title: str) -> bool:
        """Check for domain-title mismatch"""
        brand_detected = self._detect_brand(domain, title)
        if brand_detected != "unknown":
            # Check if domain contains brand name but is not official
            for brand, keywords in self.brand_keywords.items():
                if brand == brand_detected:
                    for keyword in keywords:
                        if keyword in domain.lower():
                            # Check if it's an official domain
                            official_domains = {
                                'microsoft': ['microsoft.com', 'office.com'],
                                'google': ['google.com', 'gmail.com'],
                                'apple': ['apple.com', 'icloud.com'],
                                'amazon': ['amazon.com', 'aws.amazon.com']
                            }
                            
                            if brand in official_domains:
                                return not any(official in domain for official in official_domains[brand])
        
        return False