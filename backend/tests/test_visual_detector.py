"""
Test visual detector functionality
"""

import pytest
from visual_detector import VisualDetector

def test_visual_detector_initialization():
    """Test visual detector initialization"""
    detector = VisualDetector()
    assert detector is not None
    assert len(detector.brand_keywords) > 0
    assert len(detector.suspicious_indicators) > 0

def test_analyze_visual_phishing():
    """Test visual analysis for phishing site"""
    detector = VisualDetector()
    
    url = "https://fake-microsoft-security.net/secure"
    title = "Microsoft Account Security Alert"
    dom = {
        "html": {"tag": "html"},
        "text_content": "Verify your Microsoft account immediately",
        "forms": [{"action": "/verify", "inputs": 3}],
        "links": ["/verify", "/help"]
    }
    
    result = detector.analyze_visual(url, title, dom)
    
    assert "impersonation_score" in result
    assert "is_impersonation" in result
    assert "visual_cues" in result
    assert "confidence" in result
    assert "brand_detected" in result
    assert "suspicious_domain" in result
    
    assert isinstance(result["impersonation_score"], (int, float))
    assert isinstance(result["is_impersonation"], bool)
    assert isinstance(result["visual_cues"], list)

def test_analyze_visual_legitimate():
    """Test visual analysis for legitimate site"""
    detector = VisualDetector()
    
    url = "https://microsoft.com/security"
    title = "Microsoft Security Center"
    dom = {
        "html": {"tag": "html"},
        "text_content": "Official Microsoft security information",
        "forms": [],
        "links": ["/help", "/privacy"]
    }
    
    result = detector.analyze_visual(url, title, dom)
    
    assert result["impersonation_score"] < 0.5  # Should be low for legitimate site
    assert result["is_impersonation"] == False
    assert result["brand_detected"] == "microsoft"

def test_detect_brand():
    """Test brand detection"""
    detector = VisualDetector()
    
    # Test Microsoft detection
    assert detector._detect_brand("fake-microsoft.com", "Microsoft Account") == "microsoft"
    
    # Test Google detection
    assert detector._detect_brand("google.com", "Gmail Security") == "google"
    
    # Test unknown brand
    assert detector._detect_brand("example.com", "Random Site") == "unknown"

def test_suspicious_domain_detection():
    """Test suspicious domain detection"""
    detector = VisualDetector()
    
    # Test suspicious domains
    assert detector._is_suspicious_domain("fake-microsoft.com") == True
    assert detector._is_suspicious_domain("suspicious-bank.net") == True
    assert detector._is_suspicious_domain("phishing-site.org") == True
    
    # Test legitimate domains
    assert detector._is_suspicious_domain("microsoft.com") == False
    assert detector._is_suspicious_domain("google.com") == False
    assert detector._is_suspicious_domain("example.com") == False