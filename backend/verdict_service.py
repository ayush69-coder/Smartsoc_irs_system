"""
PhishGuard Pro - Verdict Service
Deterministic phishing detection using demo data and rule-based scoring
"""

import json
import re
import math
from typing import Dict, List, Any
from urllib.parse import urlparse

class VerdictService:
    def __init__(self):
        self.demo_campaigns = self._load_demo_campaigns()
        self.redirects = self._load_redirects()
        self.suspicious_keywords = [
            'urgent', 'immediately', 'verify', 'suspended', 'compromised',
            'security', 'alert', 'action required', 'click here', 'update now',
            'expired', 'overdue', 'payment required', 'account locked'
        ]
        self.legitimate_domains = [
            'google.com', 'microsoft.com', 'apple.com', 'amazon.com',
            'cloud-provider.net', 'legitimate-bank.com'
        ]
    
    def _load_demo_campaigns(self) -> List[Dict]:
        """Load demo campaigns from JSON file"""
        try:
            with open('/workspace/data/demo_campaigns.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def _load_redirects(self) -> Dict:
        """Load redirect mappings from JSON file"""
        try:
            with open('/workspace/data/redirects.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def analyze_url(self, url: str) -> Dict[str, Any]:
        """Analyze URL for suspicious features"""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        features = {
            'length': len(url),
            'has_shortener': self._is_shortener(domain),
            'has_suspicious_domain': self._is_suspicious_domain(domain),
            'has_credentials': '@' in url or 'user:' in url or 'pass:' in url,
            'num_subdomains': len(domain.split('.')) - 2 if '.' in domain else 0,
            'path_entropy': self._calculate_entropy(parsed.path),
            'is_https': parsed.scheme == 'https'
        }
        
        return features
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze text content for suspicious patterns"""
        text_lower = text.lower()
        
        # Count suspicious keywords
        keyword_matches = sum(1 for keyword in self.suspicious_keywords 
                            if keyword in text_lower)
        
        # Calculate text entropy
        text_entropy = self._calculate_entropy(text)
        
        # Check for urgency indicators
        urgency_patterns = [
            r'\b(urgent|immediately|asap|right now)\b',
            r'\b(expires?|expiring|deadline)\b',
            r'\b(click here|click now|act now)\b'
        ]
        urgency_count = sum(len(re.findall(pattern, text_lower)) 
                           for pattern in urgency_patterns)
        
        return {
            'keyword_matches': keyword_matches,
            'text_entropy': text_entropy,
            'urgency_count': urgency_count,
            'length': len(text),
            'has_suspicious_patterns': keyword_matches > 2 or urgency_count > 1
        }
    
    def _is_shortener(self, domain: str) -> bool:
        """Check if domain is a known URL shortener"""
        shorteners = ['bit.ly', 'tinyurl.com', 'short.ly', 'goo.gl', 't.co']
        return any(shortener in domain for shortener in shorteners)
    
    def _is_suspicious_domain(self, domain: str) -> bool:
        """Check if domain appears suspicious"""
        suspicious_indicators = [
            'fake-', 'suspicious-', 'malicious-', 'scam-',
            'phishing-', 'fraud-', 'spam-'
        ]
        return any(indicator in domain for indicator in suspicious_indicators)
    
    def _calculate_entropy(self, text: str) -> float:
        """Calculate Shannon entropy of text"""
        if not text:
            return 0.0
        
        # Count character frequencies
        char_counts = {}
        for char in text:
            char_counts[char] = char_counts.get(char, 0) + 1
        
        # Calculate entropy
        entropy = 0.0
        text_len = len(text)
        for count in char_counts.values():
            probability = count / text_len
            entropy -= probability * math.log2(probability)
        
        return entropy
    
    def get_verdict(self, url: str, text: str, source: str) -> Dict[str, Any]:
        """Get phishing verdict for given inputs"""
        # Check against demo campaigns first
        demo_match = self._check_demo_campaigns(url, text, source)
        if demo_match:
            return demo_match
        
        # Fallback to rule-based analysis
        return self._rule_based_analysis(url, text, source)
    
    def _check_demo_campaigns(self, url: str, text: str, source: str) -> Dict[str, Any]:
        """Check if inputs match any demo campaigns"""
        for campaign in self.demo_campaigns:
            if (campaign['url'] == url or 
                campaign['final_url'] == url or
                campaign['subject'].lower() in text.lower()):
                
                # Determine action based on label
                if campaign['label'] == 'phishing':
                    action = 'block' if 'urgent' in text.lower() else 'warn'
                    score = 0.9 if action == 'block' else 0.7
                else:
                    action = 'allow'
                    score = 0.1
                
                return {
                    'score': score,
                    'action': action,
                    'reasons': self._generate_reasons(url, text, campaign),
                    'explain': {
                        'tokens': self._extract_important_tokens(text),
                        'url_features': self.analyze_url(url),
                        'campaign_match': campaign['id']
                    }
                }
        
        return None
    
    def _rule_based_analysis(self, url: str, text: str, source: str) -> Dict[str, Any]:
        """Fallback rule-based analysis"""
        url_features = self.analyze_url(url)
        text_features = self.analyze_text(text)
        
        # Calculate score based on features
        score = 0.0
        
        # URL-based scoring
        if url_features['has_shortener']:
            score += 0.3
        if url_features['has_suspicious_domain']:
            score += 0.4
        if url_features['has_credentials']:
            score += 0.2
        if url_features['num_subdomains'] > 3:
            score += 0.1
        
        # Text-based scoring
        if text_features['has_suspicious_patterns']:
            score += 0.3
        if text_features['keyword_matches'] > 3:
            score += 0.2
        if text_features['urgency_count'] > 2:
            score += 0.2
        
        # Source-based scoring
        if source == 'email' and score > 0.3:
            score += 0.1
        elif source == 'sms' and score > 0.2:
            score += 0.2
        
        # Determine action
        if score >= 0.7:
            action = 'block'
        elif score >= 0.4:
            action = 'warn'
        else:
            action = 'allow'
        
        return {
            'score': min(score, 1.0),
            'action': action,
            'reasons': self._generate_reasons(url, text, None),
            'explain': {
                'tokens': self._extract_important_tokens(text),
                'url_features': url_features
            }
        }
    
    def _generate_reasons(self, url: str, text: str, campaign: Dict = None) -> List[str]:
        """Generate human-readable reasons for the verdict"""
        reasons = []
        
        if campaign and campaign['label'] == 'phishing':
            reasons.append("Matches known phishing campaign pattern")
        
        url_features = self.analyze_url(url)
        if url_features['has_shortener']:
            reasons.append("URL appears to be a shortened link")
        if url_features['has_suspicious_domain']:
            reasons.append("Domain name appears suspicious")
        
        text_features = self.analyze_text(text)
        if text_features['has_suspicious_patterns']:
            reasons.append("Text contains suspicious keywords or patterns")
        if text_features['urgency_count'] > 1:
            reasons.append("Message contains multiple urgency indicators")
        
        if not reasons:
            reasons.append("No threats detected")
        
        return reasons
    
    def _extract_important_tokens(self, text: str) -> List[Dict[str, Any]]:
        """Extract important tokens with weights"""
        tokens = []
        text_lower = text.lower()
        
        for keyword in self.suspicious_keywords:
            if keyword in text_lower:
                weight = 0.8 if keyword in ['urgent', 'immediately', 'verify'] else 0.6
                tokens.append({
                    'token': keyword,
                    'weight': weight
                })
        
        # Add some common words with lower weights
        common_words = ['account', 'security', 'payment', 'update', 'click']
        for word in common_words:
            if word in text_lower and not any(t['token'] == word for t in tokens):
                tokens.append({
                    'token': word,
                    'weight': 0.2
                })
        
        return tokens[:8]  # Limit to top 8 tokens