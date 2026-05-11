import React from 'react'
import { MagnifyingGlassIcon } from '@heroicons/react/24/outline'

const Investigate: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white">Investigate</h1>
        <p className="text-gray-400 mt-2">Deep dive into security events and threats</p>
      </div>

      <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
        <div className="text-center">
          <MagnifyingGlassIcon className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-white mb-2">Investigation Tools</h2>
          <p className="text-gray-400 mb-6">
            Advanced investigation features coming soon
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-gray-700 rounded-lg p-4">
              <h3 className="font-medium text-white mb-2">URL Analysis</h3>
              <p className="text-gray-400 text-sm">Analyze suspicious URLs for threats</p>
            </div>
            <div className="bg-gray-700 rounded-lg p-4">
              <h3 className="font-medium text-white mb-2">Email Forensics</h3>
              <p className="text-gray-400 text-sm">Deep dive into email headers and content</p>
            </div>
            <div className="bg-gray-700 rounded-lg p-4">
              <h3 className="font-medium text-white mb-2">Threat Intelligence</h3>
              <p className="text-gray-400 text-sm">Correlate with known threat indicators</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Investigate