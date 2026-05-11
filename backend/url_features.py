"""
PhishGuard Pro - URL Features Module
Extract features from URLs for phishing detection
"""

import json
import math
import re
from urllib.parse import urlparse
from typing import Dict, Any

class URLFeatureExtractor:
    def __init__(self):
        self.redirects = self._load_redirects()
        self.shorteners = ['bit.ly', 'tinyurl.com', 'short.ly', 'goo.gl', 't.co', 'is.gd']
    
    def _load_redirects(self) -> Dict:
        """Load redirect mappings from JSON file"""
        try:
            with open('/workspace/data/redirects.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def extract_features(self, url: str) -> Dict[str, Any]:
        """Extract comprehensive features from URL"""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        
        features = {
            'length': len(url),
            'token_entropy': self._calculate_entropy(url),
            'has_punycode': self._has_punycode(domain),
            'has_at_symbol': '@' in url,
            'has_credentials': self._has_credentials(url),
            'num_subdomains': self._count_subdomains(domain),
            'path_entropy': self._calculate_entropy(parsed.path),
            'is_shortener': self._is_shortener(domain),
            'domain': domain,
            'scheme': parsed.scheme,
            'path': parsed.path,
            'query': parsed.query,
            'fragment': parsed.fragment,
            'final_url': self._resolve_redirect(url)
        }
        
        return features
    
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
    
    def _has_punycode(self, domain: str) -> bool:
        """Check if domain contains punycode"""
        return 'xn--' in domain
    
    def _has_credentials(self, url: str) -> bool:
        """Check if URL contains credentials"""
        credential_patterns = [
            r'@',  # username@domain
            r'user[:=]',  # user: or user=
            r'pass[:=]',  # pass: or pass=
            r'pwd[:=]',   # pwd: or pwd=
            r'auth[:=]'   # auth: or auth=
        ]
        return any(re.search(pattern, url, re.IGNORECASE) for pattern in credential_patterns)
    
    def _count_subdomains(self, domain: str) -> int:
        """Count number of subdomains"""
        if not domain or '.' not in domain:
            return 0
        
        parts = domain.split('.')
        # Remove TLD and domain, count remaining parts
        if len(parts) >= 2:
            return max(0, len(parts) - 2)
        return 0
    
    def _is_shortener(self, domain: str) -> bool:
        """Check if domain is a known URL shortener"""
        return any(shortener in domain for shortener in self.shorteners)
    
    def _resolve_redirect(self, url: str) -> str:
        """Resolve URL shortener redirects using demo data"""
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        path = parsed.path.lstrip('/')
        
        # Check if it's a known shortener
        if domain in self.redirects:
            if path in self.redirects[domain]:
                return self.redirects[domain][path]
        
        # Check for partial matches
        for shortener, mappings in self.redirects.items():
            if shortener in domain:
                for short_path, long_url in mappings.items():
                    if short_path in path:
                        return long_url
        
        return url  # Return original if no redirect found