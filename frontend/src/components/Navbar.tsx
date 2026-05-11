import React from 'react'
import { useTheme } from '../contexts/ThemeContext'
import { 
  SunIcon, 
  MoonIcon, 
  BellIcon, 
  UserCircleIcon 
} from '@heroicons/react/24/outline'

const Navbar: React.FC = () => {
  const { theme, toggleTheme } = useTheme()

  return (
    <div className="bg-gray-800 border-b border-gray-700 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <h2 className="text-xl font-semibold text-white">Dashboard</h2>
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
            Demo Environment
          </span>
        </div>
        
        <div className="flex items-center space-x-4">
          <button
            onClick={toggleTheme}
            className="p-2 rounded-md text-gray-400 hover:text-white hover:bg-gray-700 transition-colors"
          >
            {theme === 'dark' ? (
              <SunIcon className="h-5 w-5" />
            ) : (
              <MoonIcon className="h-5 w-5" />
            )}
          </button>
          
          <button className="p-2 rounded-md text-gray-400 hover:text-white hover:bg-gray-700 transition-colors">
            <BellIcon className="h-5 w-5" />
          </button>
          
          <button className="p-2 rounded-md text-gray-400 hover:text-white hover:bg-gray-700 transition-colors">
            <UserCircleIcon className="h-5 w-5" />
          </button>
        </div>
      </div>
    </div>
  )
}

export default Navbar