import React, { useState, useEffect } from 'react'
import { EyeIcon } from '@heroicons/react/24/outline'

interface GraphNode {
  id: string
  domain: string
  type: string
  label: string
  source: string
  degree: number
  event_count?: number
}

interface GraphLink {
  source: string
  target: string
  relationship: string
  campaign_id: string
}

interface GraphData {
  nodes: GraphNode[]
  links: GraphLink[]
  total_nodes: number
  total_links: number
}

const DomainGraph: React.FC = () => {
  const [graphData, setGraphData] = useState<GraphData | null>(null)
  const [loading, setLoading] = useState(true)
  const [selectedDomain, setSelectedDomain] = useState<string>('')
  const [domainInfo, setDomainInfo] = useState<any>(null)

  useEffect(() => {
    fetchGraphData()
  }, [])

  const fetchGraphData = async () => {
    try {
      // Fetch from backend API
      const response = await fetch('http://localhost:8000/api/graph/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ domain: '' })
      })
      
      if (response.ok) {
        const data = await response.json()
        const events = data.events || []
        
        // Extract unique domains from events
        const domainMap = new Map()
        const links = []
        
        events.forEach((event: any) => {
          const domain = event.final_url.replace(/^https?:\/\//, '').split('/')[0]
          if (!domainMap.has(domain)) {
            domainMap.set(domain, {
              id: domain,
              domain: domain,
              type: 'domain',
              label: event.label,
              source: event.source,
              degree: 0,
              event_count: 0
            })
          }
          
          const node = domainMap.get(domain)
          node.event_count += 1
          node.degree += 1
        })
        
        // Create links between domains that appear in the same events
        const domains = Array.from(domainMap.values())
        for (let i = 0; i < domains.length; i++) {
          for (let j = i + 1; j < domains.length; j++) {
            if (Math.random() < 0.3) { // Random connections for demo
              links.push({
                source: domains[i].id,
                target: domains[j].id,
                relationship: 'related',
                campaign_id: 'demo-link'
              })
            }
          }
        }
        
        setGraphData({
          nodes: domains,
          links: links,
          total_nodes: domains.length,
          total_links: links.length
        })
      }
    } catch (error) {
      console.error('Error fetching graph data:', error)
      // Fallback to mock data
      setGraphData({
        nodes: [
          { id: 'fake-bank-verification.com', domain: 'fake-bank-verification.com', type: 'domain', label: 'phishing', source: 'email', degree: 3, event_count: 2 },
          { id: 'fake-microsoft-security.net', domain: 'fake-microsoft-security.net', type: 'domain', label: 'phishing', source: 'email', degree: 2, event_count: 1 },
          { id: 'package-delivery-scam.net', domain: 'package-delivery-scam.net', type: 'domain', label: 'phishing', source: 'sms', degree: 1, event_count: 1 },
          { id: 'google.com', domain: 'google.com', type: 'domain', label: 'legitimate', source: 'web', degree: 1, event_count: 1 },
          { id: 'microsoft.com', domain: 'microsoft.com', type: 'domain', label: 'legitimate', source: 'web', degree: 1, event_count: 1 }
        ],
        links: [
          { source: 'fake-bank-verification.com', target: 'fake-microsoft-security.net', relationship: 'related', campaign_id: 'demo-001' },
          { source: 'fake-bank-verification.com', target: 'package-delivery-scam.net', relationship: 'related', campaign_id: 'demo-002' },
          { source: 'fake-microsoft-security.net', target: 'google.com', relationship: 'related', campaign_id: 'demo-003' }
        ],
        total_nodes: 5,
        total_links: 3
      })
    } finally {
      setLoading(false)
    }
  }

  const fetchDomainInfo = async (domain: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/graph/query?domain=${domain}`)
      if (response.ok) {
        const data = await response.json()
        setDomainInfo(data)
      }
    } catch (error) {
      console.error('Error fetching domain info:', error)
    }
  }

  const handleDomainClick = (domain: string) => {
    setSelectedDomain(domain)
    fetchDomainInfo(domain)
  }


  const getNodeSize = (degree: number) => {
    return Math.max(20, degree * 10)
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white">Domain Graph</h1>
        <p className="text-gray-400 mt-2">Visualize domain relationships and clusters</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Graph Visualization */}
        <div className="lg:col-span-2">
          <div className="bg-gray-800 rounded-lg border border-gray-700">
            <div className="p-6 border-b border-gray-700">
              <h2 className="text-xl font-semibold text-white">Domain Network</h2>
              <p className="text-gray-400 text-sm mt-1">
                {graphData?.total_nodes} nodes, {graphData?.total_links} connections
              </p>
            </div>
            
            <div className="p-6">
              <div className="relative h-96 bg-gray-900 rounded-lg overflow-hidden">
                {/* Force-directed graph visualization */}
                <svg className="absolute inset-0 w-full h-full">
                  {/* Connection lines */}
                  {graphData?.links.map((link, index) => {
                    const sourceNode = graphData.nodes.find(n => n.id === link.source)
                    const targetNode = graphData.nodes.find(n => n.id === link.target)
                    if (!sourceNode || !targetNode) return null
                    
                    const sourceX = 50 + (Math.random() - 0.5) * 60
                    const sourceY = 50 + (Math.random() - 0.5) * 60
                    const targetX = 50 + (Math.random() - 0.5) * 60
                    const targetY = 50 + (Math.random() - 0.5) * 60
                    
                    return (
                      <line
                        key={index}
                        x1={`${sourceX}%`}
                        y1={`${sourceY}%`}
                        x2={`${targetX}%`}
                        y2={`${targetY}%`}
                        stroke="#6B7280"
                        strokeWidth="1"
                        className="opacity-30"
                      />
                    )
                  })}
                  
                  {/* Nodes */}
                  {graphData?.nodes.map((node) => {
                    const x = 50 + (Math.random() - 0.5) * 60
                    const y = 50 + (Math.random() - 0.5) * 60
                    const size = getNodeSize(node.degree)
                    
                    return (
                      <g key={node.id}>
                        <circle
                          cx={`${x}%`}
                          cy={`${y}%`}
                          r={size / 2}
                          fill={node.label === 'phishing' ? '#EF4444' : node.label === 'legitimate' ? '#10B981' : '#6B7280'}
                          className="cursor-pointer hover:opacity-80 transition-opacity"
                          onClick={() => handleDomainClick(node.domain)}
                        />
                        <text
                          x={`${x}%`}
                          y={`${y + 1}%`}
                          textAnchor="middle"
                          className="text-xs fill-white pointer-events-none"
                          fontSize="10"
                        >
                          {node.domain.split('.')[0].substring(0, 8)}
                        </text>
                      </g>
                    )
                  })}
                </svg>
                
                {/* Instructions */}
                <div className="absolute top-4 left-4 text-xs text-gray-400">
                  Click nodes to view details
                </div>
              </div>
              
              <div className="mt-4 flex items-center justify-center space-x-4">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                  <span className="text-sm text-gray-300">Phishing</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  <span className="text-sm text-gray-300">Legitimate</span>
                </div>
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-gray-500 rounded-full"></div>
                  <span className="text-sm text-gray-300">Unknown</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Domain Details */}
        <div className="space-y-6">
          <div className="bg-gray-800 rounded-lg border border-gray-700">
            <div className="p-6 border-b border-gray-700">
              <h2 className="text-xl font-semibold text-white">Domain Details</h2>
            </div>
            
            <div className="p-6">
              {selectedDomain ? (
                <div className="space-y-4">
                  <div>
                    <h3 className="font-medium text-white mb-2">Selected Domain</h3>
                    <p className="text-gray-300 text-sm break-all">{selectedDomain}</p>
                  </div>
                  
                  {domainInfo && (
                    <>
                      <div className="bg-gray-700 rounded-lg p-3">
                        <h3 className="font-medium text-white mb-2">Cluster Score</h3>
                        <div className="flex items-center space-x-2">
                          <div className="flex-1 bg-gray-600 rounded-full h-2">
                            <div 
                              className="bg-blue-500 h-2 rounded-full"
                              style={{ width: `${domainInfo.cluster_score * 100}%` }}
                            />
                          </div>
                          <span className="text-white text-sm font-medium">
                            {(domainInfo.cluster_score * 100).toFixed(1)}%
                          </span>
                        </div>
                      </div>
                      
                      <div>
                        <h3 className="font-medium text-white mb-2">Neighbors ({domainInfo.neighbors.length})</h3>
                        <div className="space-y-2 max-h-32 overflow-y-auto">
                          {domainInfo.neighbors.map((neighbor: any, index: number) => (
                            <div key={index} className="flex items-center justify-between text-sm">
                              <span className="text-gray-300 truncate">{neighbor.domain}</span>
                              <span className={`px-2 py-1 rounded text-xs ${
                                neighbor.label === 'phishing' ? 'bg-red-100 text-red-800' :
                                neighbor.label === 'legitimate' ? 'bg-green-100 text-green-800' :
                                'bg-gray-100 text-gray-800'
                              }`}>
                                {neighbor.label}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                      
                      {domainInfo.node_info && (
                        <div className="bg-gray-700 rounded-lg p-3">
                          <h3 className="font-medium text-white mb-2">Node Info</h3>
                          <div className="space-y-1 text-xs">
                            <div className="flex justify-between">
                              <span className="text-gray-400">Type:</span>
                              <span className="text-white">{domainInfo.node_info.type}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-gray-400">Degree:</span>
                              <span className="text-white">{domainInfo.node_info.degree}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-gray-400">Source:</span>
                              <span className="text-white">{domainInfo.node_info.source}</span>
                            </div>
                          </div>
                        </div>
                      )}
                    </>
                  )}
                </div>
              ) : (
                <div className="text-center text-gray-400">
                  <EyeIcon className="h-8 w-8 mx-auto mb-2" />
                  <p>Click a domain to view details</p>
                </div>
              )}
            </div>
          </div>

          {/* Graph Statistics */}
          <div className="bg-gray-800 rounded-lg border border-gray-700">
            <div className="p-6 border-b border-gray-700">
              <h2 className="text-xl font-semibold text-white">Statistics</h2>
            </div>
            
            <div className="p-6 space-y-4">
              <div className="flex justify-between">
                <span className="text-gray-400">Total Nodes</span>
                <span className="text-white font-medium">{graphData?.total_nodes}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Total Links</span>
                <span className="text-white font-medium">{graphData?.total_links}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Phishing Domains</span>
                <span className="text-white font-medium">
                  {graphData?.nodes.filter(n => n.label === 'phishing').length}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Legitimate Domains</span>
                <span className="text-white font-medium">
                  {graphData?.nodes.filter(n => n.label === 'legitimate').length}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DomainGraph