import React, { useState, useEffect } from 'react'
import { 
  ChartBarIcon, 
  ExclamationTriangleIcon, 
  ClockIcon, 
  ShieldCheckIcon 
} from '@heroicons/react/24/outline'

interface KPIData {
  totalEvents: number
  phishRate: number
  avgLatency: number
  recentAlerts: number
}

const Overview: React.FC = () => {
  const [kpiData, setKpiData] = useState<KPIData>({
    totalEvents: 0,
    phishRate: 0,
    avgLatency: 0,
    recentAlerts: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Simulate API call to get KPI data
    const fetchKPIData = async () => {
      try {
        // In a real app, this would call the backend API
        await new Promise(resolve => setTimeout(resolve, 1000))
        
        setKpiData({
          totalEvents: 1247,
          phishRate: 23.4,
          avgLatency: 45,
          recentAlerts: 8
        })
      } catch (error) {
        console.error('Error fetching KPI data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchKPIData()
  }, [])

  const kpiCards = [
    {
      title: 'Total Events',
      value: kpiData.totalEvents.toLocaleString(),
      icon: ChartBarIcon,
      color: 'blue',
      change: '+12%',
      changeType: 'positive'
    },
    {
      title: 'Phish Rate',
      value: `${kpiData.phishRate}%`,
      icon: ExclamationTriangleIcon,
      color: 'red',
      change: '-2.1%',
      changeType: 'positive'
    },
    {
      title: 'Avg Latency',
      value: `${kpiData.avgLatency}ms`,
      icon: ClockIcon,
      color: 'green',
      change: '-5ms',
      changeType: 'positive'
    },
    {
      title: 'Recent Alerts',
      value: kpiData.recentAlerts.toString(),
      icon: ShieldCheckIcon,
      color: 'yellow',
      change: '+3',
      changeType: 'negative'
    }
  ]

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
        <h1 className="text-3xl font-bold text-white">Overview</h1>
        <p className="text-gray-400 mt-2">Monitor your phishing detection system in real-time</p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {kpiCards.map((card, index) => (
          <div 
            key={card.title} 
            className="bg-gray-800 rounded-lg p-6 border border-gray-700 hover-lift animate-fade-in"
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm font-medium">{card.title}</p>
                <p className="text-2xl font-bold text-white mt-2">{card.value}</p>
                <p className={`text-sm mt-1 ${
                  card.changeType === 'positive' ? 'text-green-400' : 'text-red-400'
                }`}>
                  {card.change} from last hour
                </p>
              </div>
              <div className={`p-3 rounded-full bg-${card.color}-100 bg-opacity-20`}>
                <card.icon className={`h-6 w-6 text-${card.color}-400`} />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Recent Activity */}
      <div className="bg-gray-800 rounded-lg border border-gray-700 animate-fade-in" style={{ animationDelay: '0.4s' }}>
        <div className="p-6 border-b border-gray-700">
          <h2 className="text-xl font-semibold text-white">Recent Activity</h2>
        </div>
        <div className="p-6">
          <div className="space-y-4">
            {[
              { time: '2 minutes ago', event: 'Phishing attempt blocked', severity: 'high' },
              { time: '5 minutes ago', event: 'Suspicious email detected', severity: 'medium' },
              { time: '8 minutes ago', event: 'False positive reported', severity: 'low' },
              { time: '12 minutes ago', event: 'New policy created', severity: 'info' },
              { time: '15 minutes ago', event: 'Domain analysis completed', severity: 'info' }
            ].map((activity, index) => (
              <div key={index} className="flex items-center justify-between py-2">
                <div className="flex items-center space-x-3">
                  <div className={`w-2 h-2 rounded-full ${
                    activity.severity === 'high' ? 'bg-red-500' :
                    activity.severity === 'medium' ? 'bg-yellow-500' :
                    activity.severity === 'low' ? 'bg-green-500' : 'bg-blue-500'
                  }`} />
                  <span className="text-white">{activity.event}</span>
                </div>
                <span className="text-gray-400 text-sm">{activity.time}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Overview