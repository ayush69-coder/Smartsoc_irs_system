/**
 * Popup script for PhishGuard Pro Extension
 */

import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';

interface Verdict {
  score: number;
  action: 'allow' | 'warn' | 'block';
  reasons: string[];
}

interface Settings {
  demoMode: boolean;
  enabled: boolean;
}

const Popup: React.FC = () => {
  const [currentUrl, setCurrentUrl] = useState<string>('');
  const [verdict, setVerdict] = useState<Verdict | null>(null);
  const [settings, setSettings] = useState<Settings>({ demoMode: false, enabled: true });
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    initializePopup();
  }, []);

  const initializePopup = async () => {
    try {
      // Get current tab URL
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      if (tab.url) {
        setCurrentUrl(tab.url);
      }

      // Get settings
      const response = await chrome.runtime.sendMessage({ type: 'GET_SETTINGS' });
      if (response.success) {
        setSettings(response.settings);
      }
    } catch (error) {
      console.error('Error initializing popup:', error);
    }
  };

  const handleCheckUrl = async () => {
    setLoading(true);
    try {
      const response = await chrome.runtime.sendMessage({
        type: 'CHECK_URL',
        url: currentUrl
      });

      if (response.success) {
        setVerdict(response.verdict);
      } else {
        console.error('Error checking URL:', response.error);
      }
    } catch (error) {
      console.error('Error checking URL:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSettingsClick = () => {
    chrome.tabs.create({ url: chrome.runtime.getURL('options.html') });
  };

  const handleDemoModeToggle = async (checked: boolean) => {
    const newSettings = { ...settings, demoMode: checked };
    setSettings(newSettings);
    
    try {
      await chrome.runtime.sendMessage({
        type: 'UPDATE_SETTINGS',
        settings: newSettings
      });
    } catch (error) {
      console.error('Error updating settings:', error);
    }
  };

  const getVerdictClass = () => {
    if (!verdict) return '';
    switch (verdict.action) {
      case 'block': return 'danger';
      case 'warn': return 'warning';
      case 'allow': return 'safe';
      default: return '';
    }
  };

  const getVerdictText = () => {
    if (!verdict) return 'Checking...';
    switch (verdict.action) {
      case 'block': return 'Blocked - Phishing Detected';
      case 'warn': return 'Warning - Suspicious';
      case 'allow': return 'Safe - No Threats';
      default: return 'Unknown';
    }
  };

  return (
    <div className="popup-container">
      <div className="header">
        <div className="logo">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
          <span>PhishGuard Pro</span>
        </div>
        <div className="status-indicator">
          <div className={`status-dot ${settings.enabled ? 'active' : ''}`}></div>
          <span>{settings.enabled ? 'Active' : 'Inactive'}</span>
        </div>
      </div>
      
      <div className="content">
        <div className="current-site">
          <h3>Current Site</h3>
          <p>{currentUrl || 'Loading...'}</p>
          <div className={`verdict ${getVerdictClass()}`}>
            <span className="verdict-label">{getVerdictText()}</span>
          </div>
        </div>
        
        <div className="actions">
          <button 
            id="checkButton" 
            className="btn btn-primary"
            onClick={handleCheckUrl}
            disabled={loading}
          >
            {loading ? 'Checking...' : 'Check This Page'}
          </button>
          <button 
            id="settingsButton" 
            className="btn btn-secondary"
            onClick={handleSettingsClick}
          >
            Settings
          </button>
        </div>
        
        <div className="demo-mode">
          <label className="checkbox-label">
            <input 
              type="checkbox" 
              id="demoMode"
              checked={settings.demoMode}
              onChange={(e) => handleDemoModeToggle(e.target.checked)}
            />
            <span className="checkmark"></span>
            Demo Mode
          </label>
        </div>
      </div>
      
      <div className="footer">
        <p>Version 1.0.0</p>
      </div>
    </div>
  );
};

// Render the popup
const container = document.getElementById('root');
if (container) {
  const root = createRoot(container);
  root.render(<Popup />);
}