import React, { useState } from 'react'
import { PlusIcon, TrashIcon, PencilIcon, PlayIcon } from '@heroicons/react/24/outline'

interface Policy {
  id: string
  name: string
  type: 'score_threshold' | 'domain_blocklist' | 'sender_whitelist'
  condition: string
  action: 'allow' | 'warn' | 'block'
  enabled: boolean
  hit_count: number
}

const Policies: React.FC = () => {
  const [policies, setPolicies] = useState<Policy[]>([
    {
      id: '1',
      name: 'High Score Block',
      type: 'score_threshold',
      condition: 'score > 0.8',
      action: 'block',
      enabled: true,
      hit_count: 23
    },
    {
      id: '2',
      name: 'Known Phishing Domains',
      type: 'domain_blocklist',
      condition: 'domain in [fake-bank.com, fake-microsoft.com]',
      action: 'block',
      enabled: true,
      hit_count: 45
    },
    {
      id: '3',
      name: 'Trusted Senders',
      type: 'sender_whitelist',
      condition: 'sender in [noreply@google.com, security@microsoft.com]',
      action: 'allow',
      enabled: true,
      hit_count: 12
    }
  ])

  const [showCreateModal, setShowCreateModal] = useState(false)
  const [showTestModal, setShowTestModal] = useState(false)
  const [testEvent, setTestEvent] = useState({
    url: 'https://fake-bank-verification.com/verify',
    sender: 'security@fake-bank.com',
    subject: 'Urgent: Verify Your Account',
    score: 0.9
  })
  const [testResult, setTestResult] = useState<any>(null)
  const [newPolicy, setNewPolicy] = useState<Partial<Policy>>({
    name: '',
    type: 'score_threshold',
    condition: '',
    action: 'warn',
    enabled: true
  })

  const handleCreatePolicy = () => {
    if (newPolicy.name && newPolicy.condition) {
      const policy: Policy = {
        id: Date.now().toString(),
        name: newPolicy.name,
        type: newPolicy.type as Policy['type'],
        condition: newPolicy.condition,
        action: newPolicy.action as Policy['action'],
        enabled: newPolicy.enabled || true,
        hit_count: 0
      }
      setPolicies([...policies, policy])
      setNewPolicy({ name: '', type: 'score_threshold', condition: '', action: 'warn', enabled: true })
      setShowCreateModal(false)
    }
  }

  const handleTogglePolicy = (id: string) => {
    setPolicies(policies.map(policy => 
      policy.id === id ? { ...policy, enabled: !policy.enabled } : policy
    ))
  }

  const handleDeletePolicy = (id: string) => {
    setPolicies(policies.filter(policy => policy.id !== id))
  }

  const handleTestPolicies = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/policies/evaluate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: testEvent.url,
          text: testEvent.subject,
          source: 'email',
          score: 0.8
        })
      })
      
      if (response.ok) {
        const result = await response.json()
        setTestResult(result)
      }
    } catch (error) {
      console.error('Error testing policies:', error)
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

  const getTypeLabel = (type: string) => {
    switch (type) {
      case 'score_threshold':
        return 'Score Threshold'
      case 'domain_blocklist':
        return 'Domain Blocklist'
      case 'sender_whitelist':
        return 'Sender Whitelist'
      default:
        return type
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Policies</h1>
          <p className="text-gray-400 mt-2">Manage detection rules and policies</p>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={() => setShowTestModal(true)}
            className="inline-flex items-center px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
          >
            <PlayIcon className="h-5 w-5 mr-2" />
            Test Policies
          </button>
          <button
            onClick={() => setShowCreateModal(true)}
            className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
          >
            <PlusIcon className="h-5 w-5 mr-2" />
            Create Policy
          </button>
        </div>
      </div>

      {/* Policies List */}
      <div className="bg-gray-800 rounded-lg border border-gray-700">
        <div className="p-6 border-b border-gray-700">
          <h2 className="text-xl font-semibold text-white">Active Policies</h2>
        </div>
        
        <div className="divide-y divide-gray-700">
          {policies.map((policy) => (
            <div key={policy.id} className="p-6 hover:bg-gray-700 transition-colors">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center space-x-3 mb-2">
                    <h3 className="text-lg font-medium text-white">{policy.name}</h3>
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getActionColor(policy.action)}`}>
                      {policy.action.toUpperCase()}
                    </span>
                    <span className="text-sm text-gray-400">
                      {getTypeLabel(policy.type)}
                    </span>
                    <span className={`text-sm ${policy.enabled ? 'text-green-400' : 'text-red-400'}`}>
                      {policy.enabled ? 'Enabled' : 'Disabled'}
                    </span>
                  </div>
                  
                  <p className="text-gray-300 text-sm mb-3">
                    <span className="font-medium">Condition:</span> {policy.condition}
                  </p>
                  
                  <div className="flex items-center space-x-4 text-sm text-gray-400">
                    <span>Hits: {policy.hit_count}</span>
                    <span>ID: {policy.id}</span>
                  </div>
                </div>
                
                <div className="flex items-center space-x-2 ml-4">
                  <button
                    onClick={() => handleTogglePolicy(policy.id)}
                    className={`px-3 py-1 rounded-md text-xs font-medium transition-colors ${
                      policy.enabled 
                        ? 'bg-red-100 text-red-800 hover:bg-red-200' 
                        : 'bg-green-100 text-green-800 hover:bg-green-200'
                    }`}
                  >
                    {policy.enabled ? 'Disable' : 'Enable'}
                  </button>
                  <button className="p-2 text-gray-400 hover:text-white hover:bg-gray-600 rounded-md transition-colors">
                    <PencilIcon className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => handleDeletePolicy(policy.id)}
                    className="p-2 text-gray-400 hover:text-red-400 hover:bg-gray-600 rounded-md transition-colors"
                  >
                    <TrashIcon className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Create Policy Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-gray-800 rounded-lg max-w-md w-full">
            <div className="p-6 border-b border-gray-700">
              <h3 className="text-xl font-semibold text-white">Create New Policy</h3>
            </div>
            
            <div className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Policy Name
                </label>
                <input
                  type="text"
                  value={newPolicy.name || ''}
                  onChange={(e) => setNewPolicy({ ...newPolicy, name: e.target.value })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Enter policy name"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Policy Type
                </label>
                <select
                  value={newPolicy.type || 'score_threshold'}
                  onChange={(e) => setNewPolicy({ ...newPolicy, type: e.target.value as Policy['type'] })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="score_threshold">Score Threshold</option>
                  <option value="domain_blocklist">Domain Blocklist</option>
                  <option value="sender_whitelist">Sender Whitelist</option>
                </select>
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Condition
                </label>
                <input
                  type="text"
                  value={newPolicy.condition || ''}
                  onChange={(e) => setNewPolicy({ ...newPolicy, condition: e.target.value })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="e.g., score > 0.8"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Action
                </label>
                <select
                  value={newPolicy.action || 'warn'}
                  onChange={(e) => setNewPolicy({ ...newPolicy, action: e.target.value as Policy['action'] })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="allow">Allow</option>
                  <option value="warn">Warn</option>
                  <option value="block">Block</option>
                </select>
              </div>
            </div>
            
            <div className="p-6 border-t border-gray-700 flex justify-end space-x-3">
              <button
                onClick={() => setShowCreateModal(false)}
                className="px-4 py-2 text-gray-300 hover:text-white transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleCreatePolicy}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
              >
                Create Policy
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Test Policies Modal */}
      {showTestModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-gray-800 rounded-lg max-w-2xl w-full">
            <div className="p-6 border-b border-gray-700">
              <h3 className="text-xl font-semibold text-white">Test Policies</h3>
            </div>
            
            <div className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Test Event URL
                </label>
                <input
                  type="text"
                  value={testEvent.url}
                  onChange={(e) => setTestEvent({ ...testEvent, url: e.target.value })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="https://example.com"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Sender
                </label>
                <input
                  type="text"
                  value={testEvent.sender}
                  onChange={(e) => setTestEvent({ ...testEvent, sender: e.target.value })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="sender@example.com"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Subject
                </label>
                <input
                  type="text"
                  value={testEvent.subject}
                  onChange={(e) => setTestEvent({ ...testEvent, subject: e.target.value })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="Email subject"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Risk Score
                </label>
                <input
                  type="number"
                  min="0"
                  max="1"
                  step="0.1"
                  value={testEvent.score}
                  onChange={(e) => setTestEvent({ ...testEvent, score: parseFloat(e.target.value) })}
                  className="w-full px-3 py-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <button
                onClick={handleTestPolicies}
                className="w-full bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition-colors"
              >
                Test Policies
              </button>
              
              {testResult && (
                <div className="mt-6 space-y-4">
                  <h4 className="font-medium text-white">Test Results</h4>
                  
                  <div className="bg-gray-700 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-gray-400">Final Action:</span>
                      <span className={`px-2 py-1 rounded text-sm font-medium ${
                        testResult.final_action === 'block' ? 'bg-red-100 text-red-800' :
                        testResult.final_action === 'warn' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-green-100 text-green-800'
                      }`}>
                        {testResult.final_action.toUpperCase()}
                      </span>
                    </div>
                    <div className="text-sm text-gray-300">
                      <strong>Reason:</strong> {testResult.reason}
                    </div>
                  </div>
                  
                  {testResult.policy_hits && testResult.policy_hits.length > 0 && (
                    <div>
                      <h5 className="font-medium text-white mb-2">Policy Hits ({testResult.policy_hits.length})</h5>
                      <div className="space-y-2">
                        {testResult.policy_hits.map((hit: any, index: number) => (
                          <div key={index} className="bg-gray-700 rounded-lg p-3">
                            <div className="flex items-center justify-between mb-1">
                              <span className="text-white text-sm font-medium">{hit.policy_name}</span>
                              <span className={`px-2 py-1 rounded text-xs font-medium ${
                                hit.action === 'block' ? 'bg-red-100 text-red-800' :
                                hit.action === 'warn' ? 'bg-yellow-100 text-yellow-800' :
                                'bg-green-100 text-green-800'
                              }`}>
                                {hit.action.toUpperCase()}
                              </span>
                            </div>
                            <p className="text-gray-300 text-xs">{hit.reason}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
            
            <div className="p-6 border-t border-gray-700 flex justify-end space-x-3">
              <button
                onClick={() => {
                  setShowTestModal(false)
                  setTestResult(null)
                }}
                className="px-4 py-2 text-gray-300 hover:text-white transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Policies