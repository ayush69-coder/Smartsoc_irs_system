import React, { useState, useEffect } from 'react'
import { 
  MagnifyingGlassIcon, 
  EyeIcon, 
  ShieldExclamationIcon,
  CheckCircleIcon,
  ExclamationTriangleIcon,
  XMarkIcon,
  ChartBarIcon,
  LinkIcon,
  ClockIcon
} from '@heroicons/react/24/outline'

interface SecurityEvent {
  id: string
  timestamp: string
  source: 'email' | 'sms' | 'web'
  sender: string
  subject: string
  body: string
  url: string
  final_url: string
  label: string
  score: number
  action: 'allow' | 'warn' | 'block'
  explain?: {
    tokens: Array<{ token: string; weight: number }>
    url_features: any
    visual_cues?: any
  }
}

const LiveFeed: React.FC = () => {
  const [events, setEvents] = useState<SecurityEvent[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [filterSource, setFilterSource] = useState<string>('all')
  const [filterAction, setFilterAction] = useState<string>('all')
  const [selectedEvent, setSelectedEvent] = useState<SecurityEvent | null>(null)

  useEffect(() => {
    fetchEvents()
  }, [])

  const fetchEvents = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/live', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({})
      })
      
      if (response.ok) {
        const data = await response.json()
        setEvents(data.events || [])
      }
    } catch (error) {
      console.error('Error fetching events:', error)
    } finally {
      setLoading(false)
    }
  }

  const filteredEvents = events.filter(event => {
    const matchesSearch = event.subject.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         event.sender.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesSource = filterSource === 'all' || event.source === filterSource
    const matchesAction = filterAction === 'all' || event.action === filterAction
    
    return matchesSearch && matchesSource && matchesAction
  })

  const getActionIcon = (action: string) => {
    switch (action) {
      case 'block':
        return <ShieldExclamationIcon className="h-5 w-5 text-red-500" />
      case 'warn':
        return <ExclamationTriangleIcon className="h-5 w-5 text-yellow-500" />
      case 'allow':
        return <CheckCircleIcon className="h-5 w-5 text-green-500" />
      default:
        return null
    }
  }

  const getActionColor = (action: string) => {
    switch (action) {
      case 'block':
        return 'bg-red-100 text-red-800'
      case 'warn':
        return 'bg-yellow-100 text-yellow-800'
      case 'allow':
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getSourceColor = (source: string) => {
    switch (source) {
      case 'email':
        return 'bg-blue-100 text-blue-800'
      case 'sms':
        return 'bg-purple-100 text-purple-800'
      case 'web':
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
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
        <h1 className="text-3xl font-bold text-white">Live Feed</h1>
        <p className="text-gray-400 mt-2">Real-time security events and alerts</p>
      </div>

      {/* Filters */}
      <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Search
            </label>
            <div className="relative">
              <MagnifyingGlassIcon className="h-5 w-5 absolute left-3 top-3 text-gray-400" />
              <input
                type="text"
                placeholder="Search events..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 bg-gray-700 border border-gray-600 rounded-md text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Source
            </label>
            <select
              value={filterSource}
              onChange={(e) => setFilterSource(e.target.value)}
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Sources</option>
              <option value="email">Email</option>
              <option value="sms">SMS</option>
              <option value="web">Web</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Action
            </label>
            <select
              value={filterAction}
              onChange={(e) => setFilterAction(e.target.value)}
              className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Actions</option>
              <option value="block">Block</option>
              <option value="warn">Warn</option>
              <option value="allow">Allow</option>
            </select>
          </div>
        </div>
      </div>

      {/* Events List */}
      <div className="bg-gray-800 rounded-lg border border-gray-700">
        <div className="p-6 border-b border-gray-700">
          <h2 className="text-xl font-semibold text-white">
            Events ({filteredEvents.length})
          </h2>
        </div>
        
        <div className="divide-y divide-gray-700">
          {filteredEvents.map((event, index) => (
            <div 
              key={event.id} 
              className="p-6 hover:bg-gray-700 transition-colors animate-fade-in hover-lift"
              style={{ animationDelay: `${index * 0.05}s` }}
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getSourceColor(event.source)}`}>
                      {event.source.toUpperCase()}
                    </span>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getActionColor(event.action)}`}>
                      {event.action.toUpperCase()}
                    </span>
                    <span className="text-gray-400 text-sm">
                      {new Date(event.timestamp).toLocaleString()}
                    </span>
                  </div>
                  
                  <h3 className="text-lg font-medium text-white mb-1">
                    {event.subject}
                  </h3>
                  
                  <p className="text-gray-400 text-sm mb-2">
                    From: {event.sender}
                  </p>
                  
                  <p className="text-gray-300 text-sm mb-3 line-clamp-2">
                    {event.body}
                  </p>
                  
                  <div className="flex items-center space-x-4">
                    <span className="text-sm text-gray-400">
                      Score: {(event.score * 100).toFixed(1)}%
                    </span>
                    <a 
                      href={event.url} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="text-blue-400 hover:text-blue-300 text-sm"
                    >
                      {event.url}
                    </a>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2 ml-4">
                  {getActionIcon(event.action)}
                  <button
                    onClick={() => setSelectedEvent(event)}
                    className="p-2 text-gray-400 hover:text-white hover:bg-gray-600 rounded-md transition-colors"
                  >
                    <EyeIcon className="h-5 w-5" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Event Detail Slide-over */}
      {selectedEvent && (
        <div className="fixed inset-0 z-50 overflow-hidden">
          <div className="absolute inset-0 bg-black bg-opacity-50 animate-fade-in" onClick={() => setSelectedEvent(null)} />
          <div className="fixed inset-y-0 right-0 flex max-w-full pl-10">
            <div className="w-screen max-w-md">
              <div className="flex h-full flex-col overflow-y-scroll bg-gray-800 shadow-xl animate-slide-in">
                {/* Header */}
                <div className="px-4 py-6 sm:px-6 border-b border-gray-700">
                  <div className="flex items-center justify-between">
                    <h2 className="text-lg font-medium text-white">Event Analysis</h2>
                    <button
                      onClick={() => setSelectedEvent(null)}
                      className="text-gray-400 hover:text-white transition-colors"
                    >
                      <XMarkIcon className="h-6 w-6" />
                    </button>
                  </div>
                </div>

                {/* Content */}
                <div className="relative flex-1 px-4 py-6 sm:px-6">
                  <div className="space-y-6">
                    {/* Basic Info */}
                    <div className="space-y-4">
                      <div>
                        <h3 className="text-sm font-medium text-gray-400 mb-2">Subject</h3>
                        <p className="text-white text-lg">{selectedEvent.subject}</p>
                      </div>
                      
                      <div>
                        <h3 className="text-sm font-medium text-gray-400 mb-2">Sender</h3>
                        <p className="text-gray-300">{selectedEvent.sender}</p>
                      </div>
                      
                      <div>
                        <h3 className="text-sm font-medium text-gray-400 mb-2">Message</h3>
                        <p className="text-gray-300 text-sm leading-relaxed">{selectedEvent.body}</p>
                      </div>
                    </div>

                    {/* URLs */}
                    <div className="space-y-4">
                      <h3 className="text-sm font-medium text-gray-400">URLs</h3>
                      <div className="space-y-3">
                        <div>
                          <div className="flex items-center space-x-2 mb-1">
                            <LinkIcon className="h-4 w-4 text-gray-400" />
                            <span className="text-xs text-gray-400">Original URL</span>
                          </div>
                          <a 
                            href={selectedEvent.url} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="text-blue-400 hover:text-blue-300 text-sm break-all"
                          >
                            {selectedEvent.url}
                          </a>
                        </div>
                        <div>
                          <div className="flex items-center space-x-2 mb-1">
                            <LinkIcon className="h-4 w-4 text-gray-400" />
                            <span className="text-xs text-gray-400">Final URL</span>
                          </div>
                          <a 
                            href={selectedEvent.final_url} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="text-blue-400 hover:text-blue-300 text-sm break-all"
                          >
                            {selectedEvent.final_url}
                          </a>
                        </div>
                      </div>
                    </div>

                    {/* Score and Action */}
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-gray-700 rounded-lg p-4">
                        <div className="flex items-center space-x-2 mb-2">
                          <ChartBarIcon className="h-4 w-4 text-gray-400" />
                          <h3 className="text-sm font-medium text-gray-400">Risk Score</h3>
                        </div>
                        <div className="flex items-center space-x-2">
                          <div className="flex-1 bg-gray-600 rounded-full h-2">
                            <div 
                              className={`h-2 rounded-full ${
                                selectedEvent.score > 0.7 ? 'bg-red-500' : 
                                selectedEvent.score > 0.4 ? 'bg-yellow-500' : 'bg-green-500'
                              }`}
                              style={{ width: `${selectedEvent.score * 100}%` }}
                            />
                          </div>
                          <span className="text-white font-medium">
                            {(selectedEvent.score * 100).toFixed(1)}%
                          </span>
                        </div>
                      </div>
                      
                      <div className="bg-gray-700 rounded-lg p-4">
                        <div className="flex items-center space-x-2 mb-2">
                          {getActionIcon(selectedEvent.action)}
                          <h3 className="text-sm font-medium text-gray-400">Action</h3>
                        </div>
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getActionColor(selectedEvent.action)}`}>
                          {selectedEvent.action.toUpperCase()}
                        </span>
                      </div>
                    </div>

                    {/* Explainability */}
                    {selectedEvent.explain && (
                      <div className="space-y-4">
                        <h3 className="text-sm font-medium text-gray-400">AI Explanation</h3>
                        
                        {/* Token Analysis */}
                        {selectedEvent.explain.tokens && selectedEvent.explain.tokens.length > 0 && (
                          <div className="bg-gray-700 rounded-lg p-4">
                            <h4 className="text-sm font-medium text-white mb-3">Key Tokens</h4>
                            <div className="space-y-2">
                              {selectedEvent.explain.tokens.slice(0, 8).map((token, index) => (
                                <div key={index} className="flex items-center justify-between">
                                  <span className="text-gray-300 text-sm">{token.token}</span>
                                  <div className="flex items-center space-x-2">
                                    <div className="w-16 bg-gray-600 rounded-full h-1.5">
                                      <div 
                                        className="bg-blue-500 h-1.5 rounded-full"
                                        style={{ width: `${token.weight * 100}%` }}
                                      />
                                    </div>
                                    <span className="text-xs text-gray-400 w-8">
                                      {(token.weight * 100).toFixed(0)}%
                                    </span>
                                  </div>
                                </div>
                              ))}
                            </div>
                          </div>
                        )}

                        {/* URL Features */}
                        {selectedEvent.explain.url_features && (
                          <div className="bg-gray-700 rounded-lg p-4">
                            <h4 className="text-sm font-medium text-white mb-3">URL Analysis</h4>
                            <div className="grid grid-cols-2 gap-3 text-xs">
                              <div className="flex justify-between">
                                <span className="text-gray-400">Length:</span>
                                <span className="text-white">{selectedEvent.explain.url_features.length}</span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-gray-400">Shortener:</span>
                                <span className={selectedEvent.explain.url_features.is_shortener ? 'text-red-400' : 'text-green-400'}>
                                  {selectedEvent.explain.url_features.is_shortener ? 'Yes' : 'No'}
                                </span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-gray-400">Subdomains:</span>
                                <span className="text-white">{selectedEvent.explain.url_features.num_subdomains}</span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-gray-400">Credentials:</span>
                                <span className={selectedEvent.explain.url_features.has_credentials ? 'text-red-400' : 'text-green-400'}>
                                  {selectedEvent.explain.url_features.has_credentials ? 'Yes' : 'No'}
                                </span>
                              </div>
                            </div>
                          </div>
                        )}

                        {/* Visual Cues */}
                        {selectedEvent.explain.visual_cues && (
                          <div className="bg-gray-700 rounded-lg p-4">
                            <h4 className="text-sm font-medium text-white mb-3">Visual Analysis</h4>
                            <div className="space-y-2">
                              <div className="flex justify-between">
                                <span className="text-gray-400 text-sm">Impersonation Score:</span>
                                <span className="text-white text-sm">
                                  {(selectedEvent.explain.visual_cues.impersonation_score * 100).toFixed(1)}%
                                </span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-gray-400 text-sm">Brand Detected:</span>
                                <span className="text-white text-sm capitalize">
                                  {selectedEvent.explain.visual_cues.brand_detected || 'Unknown'}
                                </span>
                              </div>
                            </div>
                          </div>
                        )}
                      </div>
                    )}

                    {/* Timestamp */}
                    <div className="flex items-center space-x-2 text-xs text-gray-400">
                      <ClockIcon className="h-4 w-4" />
                      <span>
                        {new Date(selectedEvent.timestamp).toLocaleString()}
                      </span>
                    </div>
                  </div>
                </div>

                {/* Footer Actions */}
                <div className="flex-shrink-0 border-t border-gray-700 px-4 py-4">
                  <div className="flex space-x-3">
                    <button className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition-colors">
                      Mark as False Positive
                    </button>
                    <button className="flex-1 bg-gray-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-gray-700 transition-colors">
                      Quarantine
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default LiveFeed