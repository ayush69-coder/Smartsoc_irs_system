import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ThemeProvider } from './contexts/ThemeContext'
import Sidebar from './components/Sidebar'
import Navbar from './components/Navbar'
import Overview from './pages/Overview'
import LiveFeed from './pages/LiveFeed'
import Investigate from './pages/Investigate'
import DomainGraph from './pages/DomainGraph'
import Policies from './pages/Policies'
import Settings from './pages/Settings'
import './index.css'

function App() {
  return (
    <ThemeProvider>
      <Router>
        <div className="min-h-screen bg-gray-900 text-white">
          <div className="flex">
            <Sidebar />
            <div className="flex-1 flex flex-col">
              <Navbar />
              <main className="flex-1 p-6">
                <Routes>
                  <Route path="/" element={<Overview />} />
                  <Route path="/live-feed" element={<LiveFeed />} />
                  <Route path="/investigate" element={<Investigate />} />
                  <Route path="/domain-graph" element={<DomainGraph />} />
                  <Route path="/policies" element={<Policies />} />
                  <Route path="/settings" element={<Settings />} />
                </Routes>
              </main>
            </div>
          </div>
        </div>
      </Router>
    </ThemeProvider>
  )
}

export default App