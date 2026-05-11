"""
URL feature extraction service
"""

import urllib.parse
import re
import math
from typing import Dict, Any

class URLFeatureExtractor:
    """Service for extracting features from URLs"""
    
    def __init__(self):
        # Load redirect mappings (simulated)
        self.redirect_mappings = {
            "bit.ly": "https://example.com/malicious",
            "tinyurl.com": "https://example.com/phishing",
            "goo.gl": "https://example.com/suspicious"
        }
    
    def extract_features(self, url: str) -> Dict[str, Any]:
        """Extract features from URL"""
        try:
            parsed = urllib.parse.urlparse(url)
            
            features = {
                "length": len(url),
                "token_entropy": self._calculate_entropy(url),
                "has_punycode": self._has_punycode(url),
                "has_at_symbol": "@" in url,
                "has_credentials": self._has_credentials(parsed),
                "num_subdomains": self._count_subdomains(parsed.hostname or ""),
                "path_entropy": self._calculate_entropy(parsed.path or ""),
                "is_shortener": self._is_shortener(parsed.hostname or ""),
                "domain": parsed.hostname or "",
                "scheme": parsed.scheme,
                "path": parsed.path,
                "query": parsed.query,
                "fragment": parsed.fragment
            }
            
            return features
            
        except Exception as e:
            # Return default features if parsing fails
            return {
                "length": len(url),
                "token_entropy": 0.0,
                "has_punycode": False,
                "has_at_symbol": False,
                "has_credentials": False,
                "num_subdomains": 0,
                "path_entropy": 0.0,
                "is_shortener": False,
                "domain": "",
                "scheme": "",
                "path": "",
                "query": "",
                "fragment": ""
            }
    
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
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        return entropy
    
    def _has_punycode(self, url: str) -> bool:
        """Check if URL contains punycode"""
        return "xn--" in url.lower()
    
    def _has_credentials(self, parsed) -> bool:
        """Check if URL contains credentials"""
        return bool(parsed.username or parsed.password)
    
    def _count_subdomains(self, hostname: str) -> int:
        """Count number of subdomains"""
        if not hostname:
            return 0
        
        parts = hostname.split(".")
        # Remove TLD and domain, count remaining parts
        if len(parts) > 2:
            return len(parts) - 2
        return 0
    
    def _is_shortener(self, hostname: str) -> bool:
        """Check if domain is a known URL shortener"""
        if not hostname:
            return False
        
        shorteners = [
            "bit.ly", "tinyurl.com", "goo.gl", "t.co", "short.link",
            "is.gd", "v.gd", "ow.ly", "buff.ly", "shorturl.at"
        ]
        
        return any(shortener in hostname.lower() for shortener in shorteners)