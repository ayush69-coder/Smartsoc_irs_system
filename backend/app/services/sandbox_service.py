"""
Sandbox Service - Simulates behavioral analysis and threat detection
"""
import json
import time
import random
from typing import Dict, List, Any
from datetime import datetime, timedelta


class SandboxService:
    def __init__(self):
        self.sandbox_reports = {}
        self.campaign_patterns = {
            'fake-bank': {
                'network_calls': ['api.bank.com', 'secure-login.net', 'phishing-site.com'],
                'files_dropped': ['bank_credentials.exe', 'keylogger.dll'],
                'processes': ['svchost.exe', 'bank_verification.exe'],
                'iocs': ['192.168.1.100', 'malicious-domain.net', 'suspicious-hash-123']
            },
            'fake-cloud': {
                'network_calls': ['cloud-storage.com', 'office365-fake.net', 'microsoft-login.com'],
                'files_dropped': ['cloud_sync.exe', 'document_stealer.dll'],
                'processes': ['onedrive.exe', 'cloud_backup.exe'],
                'iocs': ['10.0.0.50', 'fake-cloud.net', 'malicious-hash-456']
            },
            'invoice-scam': {
                'network_calls': ['invoice-payment.com', 'billing-system.net', 'payment-gateway.com'],
                'files_dropped': ['invoice_reader.exe', 'payment_stealer.dll'],
                'processes': ['invoice_processor.exe', 'payment_handler.exe'],
                'iocs': ['172.16.0.25', 'invoice-scam.net', 'suspicious-hash-789']
            },
            'microsoft-impersonation': {
                'network_calls': ['microsoft-security.com', 'office365-update.net', 'windows-update.com'],
                'files_dropped': ['microsoft_update.exe', 'security_patch.dll'],
                'processes': ['windows_update.exe', 'security_center.exe'],
                'iocs': ['203.0.113.10', 'microsoft-fake.net', 'malicious-hash-abc']
            },
            'package-delivery': {
                'network_calls': ['delivery-tracking.com', 'package-update.net', 'shipping-service.com'],
                'files_dropped': ['delivery_tracker.exe', 'package_monitor.dll'],
                'processes': ['delivery_app.exe', 'tracking_service.exe'],
                'iocs': ['198.51.100.5', 'delivery-scam.net', 'suspicious-hash-def']
            }
        }

    def submit_for_analysis(self, url: str, attachment: str = None) -> Dict[str, Any]:
        """Submit URL/attachment for sandbox analysis"""
        submission_id = f"sandbox_{int(time.time())}_{random.randint(1000, 9999)}"
        
        # Determine campaign type based on URL
        campaign_type = self._detect_campaign_type(url)
        
        # Generate realistic sandbox report
        report = self._generate_sandbox_report(submission_id, url, campaign_type, attachment)
        
        # Store report
        self.sandbox_reports[submission_id] = report
        
        return {
            "submission_id": submission_id,
            "status": "submitted",
            "estimated_completion": "5-10 minutes",
            "report_url": f"/api/sandbox/report/{submission_id}"
        }

    def get_report(self, submission_id: str) -> Dict[str, Any]:
        """Get sandbox analysis report"""
        if submission_id not in self.sandbox_reports:
            return {"error": "Report not found"}
        
        return self.sandbox_reports[submission_id]

    def _detect_campaign_type(self, url: str) -> str:
        """Detect campaign type based on URL patterns"""
        url_lower = url.lower()
        
        if any(keyword in url_lower for keyword in ['bank', 'verification', 'account', 'login']):
            return 'fake-bank'
        elif any(keyword in url_lower for keyword in ['cloud', 'office', 'microsoft', 'onedrive']):
            return 'fake-cloud'
        elif any(keyword in url_lower for keyword in ['invoice', 'payment', 'billing', 'receipt']):
            return 'invoice-scam'
        elif any(keyword in url_lower for keyword in ['microsoft', 'windows', 'security', 'update']):
            return 'microsoft-impersonation'
        elif any(keyword in url_lower for keyword in ['delivery', 'package', 'tracking', 'shipping']):
            return 'package-delivery'
        else:
            return 'fake-bank'  # Default fallback

    def _generate_sandbox_report(self, submission_id: str, url: str, campaign_type: str, attachment: str = None) -> Dict[str, Any]:
        """Generate realistic sandbox analysis report"""
        start_time = datetime.now()
        analysis_duration = random.randint(300, 600)  # 5-10 minutes
        
        # Get campaign patterns
        patterns = self.campaign_patterns.get(campaign_type, self.campaign_patterns['fake-bank'])
        
        # Generate timeline events
        timeline = self._generate_timeline(start_time, analysis_duration, patterns)
        
        # Generate extracted artifacts
        artifacts = self._generate_artifacts(patterns)
        
        # Generate IOCs
        iocs = self._generate_iocs(patterns)
        
        # Calculate threat score
        threat_score = self._calculate_threat_score(patterns, timeline, artifacts)
        
        # Determine verdict
        verdict = self._determine_verdict(threat_score)
        
        return {
            "submission_id": submission_id,
            "url": url,
            "attachment": attachment,
            "status": "completed",
            "analysis_duration": analysis_duration,
            "threat_score": threat_score,
            "verdict": verdict,
            "campaign_type": campaign_type,
            "timeline": timeline,
            "artifacts": artifacts,
            "iocs": iocs,
            "summary": {
                "network_connections": len(timeline.get('network_events', [])),
                "files_created": len([a for a in artifacts if a['type'] == 'file']),
                "processes_spawned": len(timeline.get('process_events', [])),
                "suspicious_activities": len([e for e in timeline.get('all_events', []) if e.get('severity') == 'high'])
            },
            "created_at": start_time.isoformat(),
            "completed_at": (start_time + timedelta(seconds=analysis_duration)).isoformat()
        }

    def _generate_timeline(self, start_time: datetime, duration: int, patterns: Dict) -> Dict[str, List]:
        """Generate realistic timeline of events"""
        timeline = {
            "network_events": [],
            "process_events": [],
            "file_events": [],
            "all_events": []
        }
        
        current_time = start_time
        
        # Network events
        for i, domain in enumerate(patterns['network_calls']):
            event_time = current_time + timedelta(seconds=random.randint(30, 120))
            event = {
                "timestamp": event_time.isoformat(),
                "type": "network_connection",
                "domain": domain,
                "ip": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
                "port": random.choice([80, 443, 8080, 8443]),
                "protocol": random.choice(["HTTP", "HTTPS", "TCP"]),
                "severity": "high" if "phishing" in domain or "fake" in domain else "medium"
            }
            timeline["network_events"].append(event)
            timeline["all_events"].append(event)
        
        # Process events
        for i, process in enumerate(patterns['processes']):
            event_time = current_time + timedelta(seconds=random.randint(60, 180))
            event = {
                "timestamp": event_time.isoformat(),
                "type": "process_creation",
                "process_name": process,
                "pid": random.randint(1000, 9999),
                "parent_pid": random.randint(100, 999),
                "command_line": f"{process} --silent --background",
                "severity": "high" if "malicious" in process or "stealer" in process else "medium"
            }
            timeline["process_events"].append(event)
            timeline["all_events"].append(event)
        
        # File events
        for i, file in enumerate(patterns['files_dropped']):
            event_time = current_time + timedelta(seconds=random.randint(90, 240))
            event = {
                "timestamp": event_time.isoformat(),
                "type": "file_creation",
                "filename": file,
                "path": f"C:\\Users\\User\\AppData\\Local\\Temp\\{file}",
                "size": random.randint(1024, 1024*1024),
                "hash": f"sha256:{''.join(random.choices('0123456789abcdef', k=64))}",
                "severity": "high" if file.endswith('.exe') or file.endswith('.dll') else "medium"
            }
            timeline["file_events"].append(event)
            timeline["all_events"].append(event)
        
        # Sort all events by timestamp
        timeline["all_events"].sort(key=lambda x: x["timestamp"])
        
        return timeline

    def _generate_artifacts(self, patterns: Dict) -> List[Dict]:
        """Generate extracted artifacts"""
        artifacts = []
        
        # Files
        for file in patterns['files_dropped']:
            artifacts.append({
                "type": "file",
                "name": file,
                "path": f"C:\\Users\\User\\AppData\\Local\\Temp\\{file}",
                "size": random.randint(1024, 1024*1024),
                "hash": f"sha256:{''.join(random.choices('0123456789abcdef', k=64))}",
                "classification": "malicious" if file.endswith('.exe') else "suspicious"
            })
        
        # Registry entries
        artifacts.append({
            "type": "registry",
            "key": "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
            "value": "MaliciousApp",
            "data": "C:\\Users\\User\\AppData\\Local\\Temp\\malicious.exe",
            "classification": "malicious"
        })
        
        # Memory dumps
        artifacts.append({
            "type": "memory",
            "process_name": "suspicious_process.exe",
            "pid": random.randint(1000, 9999),
            "size": random.randint(1024*1024, 10*1024*1024),
            "classification": "suspicious"
        })
        
        return artifacts

    def _generate_iocs(self, patterns: Dict) -> List[Dict]:
        """Generate Indicators of Compromise"""
        iocs = []
        
        # IP addresses
        for ip in patterns['iocs']:
            iocs.append({
                "type": "ip_address",
                "value": ip,
                "classification": "malicious",
                "confidence": random.uniform(0.7, 0.95)
            })
        
        # Domains
        for domain in patterns['network_calls']:
            if "phishing" in domain or "fake" in domain:
                iocs.append({
                    "type": "domain",
                    "value": domain,
                    "classification": "malicious",
                    "confidence": random.uniform(0.8, 0.95)
                })
        
        # File hashes
        for i in range(3):
            iocs.append({
                "type": "file_hash",
                "value": f"sha256:{''.join(random.choices('0123456789abcdef', k=64))}",
                "classification": "malicious",
                "confidence": random.uniform(0.6, 0.9)
            })
        
        return iocs

    def _calculate_threat_score(self, patterns: Dict, timeline: Dict, artifacts: List[Dict]) -> float:
        """Calculate overall threat score"""
        score = 0.0
        
        # Network connections
        malicious_connections = len([e for e in timeline['network_events'] if e.get('severity') == 'high'])
        score += min(malicious_connections * 0.2, 0.4)
        
        # Process creation
        malicious_processes = len([e for e in timeline['process_events'] if e.get('severity') == 'high'])
        score += min(malicious_processes * 0.15, 0.3)
        
        # File creation
        malicious_files = len([a for a in artifacts if a.get('classification') == 'malicious'])
        score += min(malicious_files * 0.1, 0.2)
        
        # IOCs
        high_confidence_iocs = len([ioc for ioc in patterns['iocs'] if random.random() > 0.3])
        score += min(high_confidence_iocs * 0.05, 0.1)
        
        return min(score, 1.0)

    def _determine_verdict(self, threat_score: float) -> str:
        """Determine sandbox verdict based on threat score"""
        if threat_score >= 0.8:
            return "malicious"
        elif threat_score >= 0.5:
            return "suspicious"
        else:
            return "clean"