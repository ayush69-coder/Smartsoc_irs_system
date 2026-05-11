"""
Verdict service for phishing detection
"""

import re
import math
from typing import Dict, List, Any
from app.models.schemas import TokenWeight, ExplainData

class VerdictService:
    """Service for generating phishing verdicts"""
    
    def __init__(self):
        self.phishing_keywords = [
            "urgent", "verify", "account", "suspended", "click here", "immediately",
            "security", "update", "confirm", "expired", "limited time", "act now",
            "congratulations", "winner", "prize", "free", "guaranteed", "risk-free"
        ]
        
        self.suspicious_patterns = [
            r"https?://[^\s]+",  # URLs
            r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",  # IP addresses
            r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",  # Email addresses
        ]
    
    def analyze(self, url: str, text: str, source: str, url_features: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content and return verdict"""
        
        # Calculate text-based score
        text_score = self._analyze_text(text)
        
        # Calculate URL-based score
        url_score = self._analyze_url_features(url_features)
        
        # Combine scores
        combined_score = (text_score * 0.6) + (url_score * 0.4)
        
        # Determine action
        if combined_score >= 0.8:
            action = "block"
        elif combined_score >= 0.5:
            action = "warn"
        else:
            action = "allow"
        
        # Generate reasons
        reasons = self._generate_reasons(text_score, url_score, url_features)
        
        # Extract important tokens
        tokens = self._extract_important_tokens(text)
        
        # Create explanation
        explain = ExplainData(
            tokens=tokens,
            url_features=url_features,
            visual_cues=None
        )
        
        return {
            "score": round(combined_score, 3),
            "action": action,
            "reasons": reasons,
            "explain": explain
        }
    
    def _analyze_text(self, text: str) -> float:
        """Analyze text content for phishing indicators"""
        text_lower = text.lower()
        score = 0.0
        
        # Check for phishing keywords
        keyword_matches = sum(1 for keyword in self.phishing_keywords if keyword in text_lower)
        score += min(keyword_matches * 0.1, 0.5)
        
        # Check for suspicious patterns
        pattern_matches = sum(1 for pattern in self.suspicious_patterns if re.search(pattern, text))
        score += min(pattern_matches * 0.15, 0.3)
        
        # Check for urgency indicators
        urgency_words = ["urgent", "immediately", "asap", "now", "today"]
        urgency_matches = sum(1 for word in urgency_words if word in text_lower)
        score += min(urgency_matches * 0.1, 0.2)
        
        return min(score, 1.0)
    
    def _analyze_url_features(self, url_features: Dict[str, Any]) -> float:
        """Analyze URL features for phishing indicators"""
        score = 0.0
        
        # Length-based scoring
        if url_features.get("length", 0) > 100:
            score += 0.2
        
        # Entropy-based scoring
        if url_features.get("token_entropy", 0) > 0.8:
            score += 0.3
        
        # Suspicious characters
        if url_features.get("has_punycode", False):
            score += 0.4
        
        if url_features.get("has_at_symbol", False):
            score += 0.2
        
        # Shortener detection
        if url_features.get("is_shortener", False):
            score += 0.1
        
        return min(score, 1.0)
    
    def _generate_reasons(self, text_score: float, url_score: float, url_features: Dict[str, Any]) -> List[str]:
        """Generate human-readable reasons for the verdict"""
        reasons = []
        
        if text_score > 0.5:
            reasons.append("Text contains suspicious keywords or patterns")
        
        if url_score > 0.5:
            reasons.append("URL shows characteristics of phishing attempts")
        
        if url_features.get("has_punycode", False):
            reasons.append("URL contains punycode characters (potential IDN homograph attack)")
        
        if url_features.get("is_shortener", False):
            reasons.append("URL appears to be a shortened link")
        
        if url_features.get("length", 0) > 100:
            reasons.append("URL is unusually long")
        
        if not reasons:
            reasons.append("Content appears legitimate")
        
        return reasons
    
    def _extract_important_tokens(self, text: str) -> List[TokenWeight]:
        """Extract important tokens from text"""
        # Simple tokenization and scoring
        words = re.findall(r'\b\w+\b', text.lower())
        word_scores = {}
        
        for word in words:
            if word in self.phishing_keywords:
                word_scores[word] = 0.8
            elif len(word) > 10:  # Long words might be suspicious
                word_scores[word] = 0.3
            else:
                word_scores[word] = 0.1
        
        # Sort by score and take top 8
        sorted_words = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)[:8]
        
        return [TokenWeight(token=word, weight=score) for word, score in sorted_words]