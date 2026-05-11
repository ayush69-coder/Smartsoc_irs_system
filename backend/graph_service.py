"""
PhishGuard Pro - Graph Service
Domain graph analysis using NetworkX
"""

import json
import networkx as nx
from typing import Dict, List, Any, Tuple
from urllib.parse import urlparse

class GraphService:
    def __init__(self):
        self.graph = nx.Graph()
        self._build_graph()
    
    def _build_graph(self):
        """Build graph from demo campaigns"""
        try:
            with open('/workspace/data/demo_campaigns.json', 'r') as f:
                campaigns = json.load(f)
        except FileNotFoundError:
            campaigns = []
        
        # Add nodes and edges from campaigns
        for campaign in campaigns:
            domain = self._extract_domain(campaign.get('final_url', ''))
            if domain:
                # Add domain node
                self.graph.add_node(domain, 
                    type='domain',
                    label=campaign.get('label', 'unknown'),
                    source=campaign.get('source', 'unknown'),
                    timestamp=campaign.get('timestamp', '')
                )
                
                # Add edges to related domains
                related_domains = self._find_related_domains(campaign)
                for related_domain in related_domains:
                    if related_domain != domain:
                        self.graph.add_edge(domain, related_domain, 
                            relationship='related',
                            campaign_id=campaign.get('id', '')
                        )
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            parsed = urlparse(url)
            return parsed.netloc.lower()
        except:
            return ""
    
    def _find_related_domains(self, campaign: Dict) -> List[str]:
        """Find related domains from campaign data"""
        related = []
        
        # Extract domain from final URL
        final_domain = self._extract_domain(campaign.get('final_url', ''))
        if final_domain:
            related.append(final_domain)
        
        # Extract domain from original URL
        original_domain = self._extract_domain(campaign.get('url', ''))
        if original_domain:
            related.append(original_domain)
        
        # Add sender domain if it's an email
        if campaign.get('source') == 'email':
            sender = campaign.get('sender', '')
            if '@' in sender:
                sender_domain = sender.split('@')[1].lower()
                related.append(sender_domain)
        
        return list(set(related))  # Remove duplicates
    
    def query_domain(self, domain: str) -> Dict[str, Any]:
        """Query graph for domain neighbors and cluster info"""
        domain = domain.lower()
        
        if not self.graph.has_node(domain):
            return {
                "domain": domain,
                "neighbors": [],
                "cluster_score": 0.0,
                "node_info": None
            }
        
        # Get neighbors
        neighbors = list(self.graph.neighbors(domain))
        neighbor_info = []
        
        for neighbor in neighbors:
            node_data = self.graph.nodes[neighbor]
            neighbor_info.append({
                "domain": neighbor,
                "type": node_data.get('type', 'unknown'),
                "label": node_data.get('label', 'unknown'),
                "source": node_data.get('source', 'unknown')
            })
        
        # Calculate cluster score (simplified)
        cluster_score = self._calculate_cluster_score(domain)
        
        # Get node info
        node_data = self.graph.nodes[domain]
        node_info = {
            "type": node_data.get('type', 'unknown'),
            "label": node_data.get('label', 'unknown'),
            "source": node_data.get('source', 'unknown'),
            "timestamp": node_data.get('timestamp', ''),
            "degree": self.graph.degree(domain)
        }
        
        return {
            "domain": domain,
            "neighbors": neighbor_info,
            "cluster_score": cluster_score,
            "node_info": node_info
        }
    
    def _calculate_cluster_score(self, domain: str) -> float:
        """Calculate cluster score for domain"""
        if not self.graph.has_node(domain):
            return 0.0
        
        # Simple cluster score based on degree and neighbor labels
        degree = self.graph.degree(domain)
        neighbors = list(self.graph.neighbors(domain))
        
        # Count suspicious neighbors
        suspicious_count = 0
        for neighbor in neighbors:
            neighbor_data = self.graph.nodes[neighbor]
            if neighbor_data.get('label') == 'phishing':
                suspicious_count += 1
        
        # Calculate score (0.0 to 1.0)
        if degree == 0:
            return 0.0
        
        base_score = min(degree / 10.0, 1.0)  # Normalize degree
        suspicious_ratio = suspicious_count / len(neighbors) if neighbors else 0
        
        return min(base_score + suspicious_ratio * 0.5, 1.0)
    
    def get_graph_data(self) -> Dict[str, Any]:
        """Get full graph data for visualization"""
        nodes = []
        links = []
        
        for node, data in self.graph.nodes(data=True):
            nodes.append({
                "id": node,
                "type": data.get('type', 'unknown'),
                "label": data.get('label', 'unknown'),
                "source": data.get('source', 'unknown'),
                "degree": self.graph.degree(node)
            })
        
        for source, target, data in self.graph.edges(data=True):
            links.append({
                "source": source,
                "target": target,
                "relationship": data.get('relationship', 'unknown'),
                "campaign_id": data.get('campaign_id', '')
            })
        
        return {
            "nodes": nodes,
            "links": links,
            "total_nodes": len(nodes),
            "total_links": len(links)
        }