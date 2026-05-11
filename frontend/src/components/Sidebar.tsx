import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { 
  HomeIcon, 
  ChartBarIcon, 
  MagnifyingGlassIcon, 
  ShareIcon, 
  ShieldCheckIcon, 
  CogIcon 
} from '@heroicons/react/24/outline'

const navigation = [
  { name: 'Overview', href: '/', icon: HomeIcon },
  { name: 'Live Feed', href: '/live-feed', icon: ChartBarIcon },
  { name: 'Investigate', href: '/investigate', icon: MagnifyingGlassIcon },
  { name: 'Domain Graph', href: '/domain-graph', icon: ShareIcon },
  { name: 'Policies', href: '/policies', icon: ShieldCheckIcon },
  { name: 'Settings', href: '/settings', icon: CogIcon },
]

const Sidebar: React.FC = () => {
  const location = useLocation()

  return (
    <div className="w-64 bg-gray-800 min-h-screen">
      <div className="p-6">
        <h1 className="text-2xl font-bold text-white">
          PhishGuard <span className="text-blue-400">Pro</span>
        </h1>
        <p className="text-gray-400 text-sm mt-1">AI-Powered Phishing Detection</p>
      </div>
      
      <nav className="mt-8">
        <div className="px-4 space-y-2">
          {navigation.map((item) => {
            const isActive = location.pathname === item.href
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`group flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                  isActive
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                }`}
              >
                <item.icon
                  className={`mr-3 h-5 w-5 ${
                    isActive ? 'text-white' : 'text-gray-400 group-hover:text-white'
                  }`}
                />
                {item.name}
              </Link>
            )
          })}
        </div>
      </nav>
    </div>
  )
}

export default Sidebar