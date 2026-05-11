import { ExtensionSettings, PhishingVerdict } from './types';

class PhishGuardPopup {
  private settings: ExtensionSettings = {
    enabled: true,
    demoMode: true,
    apiUrl: 'http://localhost:8000',
    autoCheck: true,
    showNotifications: true
  };

  constructor() {
    this.initialize();
  }

  private async initialize() {
    await this.loadSettings();
    this.render();
    this.setupEventListeners();
  }

  private async loadSettings() {
    try {
      const response = await chrome.runtime.sendMessage({ action: 'getSettings' });
      if (response) {
        this.settings = { ...this.settings, ...response };
      }
    } catch (error) {
      console.error('Error loading settings:', error);
    }
  }

  private async saveSettings() {
    try {
      await chrome.runtime.sendMessage({
        action: 'updateSettings',
        settings: this.settings
      });
    } catch (error) {
      console.error('Error saving settings:', error);
    }
  }

  private render() {
    const popup = document.getElementById('popup');
    if (!popup) return;

    popup.innerHTML = `
      <div class="popup-container">
        <div class="header">
          <div class="logo">
            <div class="logo-icon">🛡️</div>
            <div class="logo-text">
              <div class="title">PhishGuard Pro</div>
              <div class="subtitle">AI-Powered Protection</div>
            </div>
          </div>
          <div class="status ${this.settings.enabled ? 'enabled' : 'disabled'}">
            ${this.settings.enabled ? '🟢 Active' : '🔴 Disabled'}
          </div>
        </div>

        <div class="content">
          <div class="section">
            <h3>Quick Check</h3>
            <div class="quick-check">
              <input type="url" id="url-input" placeholder="Enter URL to check..." />
              <button id="check-btn" class="btn btn-primary">Check URL</button>
            </div>
            <div id="check-result" class="check-result"></div>
          </div>

          <div class="section">
            <h3>Settings</h3>
            <div class="settings">
              <label class="setting-item">
                <input type="checkbox" id="enabled" ${this.settings.enabled ? 'checked' : ''} />
                <span>Enable Protection</span>
              </label>
              <label class="setting-item">
                <input type="checkbox" id="demoMode" ${this.settings.demoMode ? 'checked' : ''} />
                <span>Demo Mode</span>
              </label>
              <label class="setting-item">
                <input type="checkbox" id="autoCheck" ${this.settings.autoCheck ? 'checked' : ''} />
                <span>Auto Check Pages</span>
              </label>
              <label class="setting-item">
                <input type="checkbox" id="showNotifications" ${this.settings.showNotifications ? 'checked' : ''} />
                <span>Show Notifications</span>
              </label>
            </div>
          </div>

          <div class="section">
            <h3>Recent Activity</h3>
            <div id="recent-activity" class="recent-activity">
              <div class="loading">Loading...</div>
            </div>
          </div>

          <div class="section">
            <h3>About</h3>
            <div class="about">
              <p>PhishGuard Pro v1.0.0</p>
              <p>AI-powered phishing detection</p>
              <a href="#" id="dashboard-link">Open Dashboard</a>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  private setupEventListeners() {
    // Settings toggles
    document.getElementById('enabled')?.addEventListener('change', (e) => {
      this.settings.enabled = (e.target as HTMLInputElement).checked;
      this.saveSettings();
      this.updateStatus();
    });

    document.getElementById('demoMode')?.addEventListener('change', (e) => {
      this.settings.demoMode = (e.target as HTMLInputElement).checked;
      this.saveSettings();
    });

    document.getElementById('autoCheck')?.addEventListener('change', (e) => {
      this.settings.autoCheck = (e.target as HTMLInputElement).checked;
      this.saveSettings();
    });

    document.getElementById('showNotifications')?.addEventListener('change', (e) => {
      this.settings.showNotifications = (e.target as HTMLInputElement).checked;
      this.saveSettings();
    });

    // Quick check
    document.getElementById('check-btn')?.addEventListener('click', () => {
      this.checkUrl();
    });

    document.getElementById('url-input')?.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        this.checkUrl();
      }
    });

    // Dashboard link
    document.getElementById('dashboard-link')?.addEventListener('click', (e) => {
      e.preventDefault();
      chrome.tabs.create({ url: 'http://localhost:3001' });
    });

    // Load recent activity
    this.loadRecentActivity();
  }

  private updateStatus() {
    const status = document.querySelector('.status');
    if (status) {
      status.className = `status ${this.settings.enabled ? 'enabled' : 'disabled'}`;
      status.textContent = this.settings.enabled ? '🟢 Active' : '🔴 Disabled';
    }
  }

  private async checkUrl() {
    const urlInput = document.getElementById('url-input') as HTMLInputElement;
    const resultDiv = document.getElementById('check-result');
    
    if (!urlInput.value.trim()) {
      this.showResult('Please enter a URL to check.', 'error');
      return;
    }

    this.showResult('Checking URL...', 'loading');

    try {
      const response = await chrome.runtime.sendMessage({
        action: 'checkUrl',
        url: urlInput.value.trim()
      });

      if (response) {
        this.displayVerdict(response);
      } else {
        this.showResult('Unable to check URL. Please try again.', 'error');
      }
    } catch (error) {
      console.error('Error checking URL:', error);
      this.showResult('Error checking URL. Please try again.', 'error');
    }
  }

  private displayVerdict(verdict: PhishingVerdict) {
    const resultDiv = document.getElementById('check-result');
    if (!resultDiv) return;

    const riskPercentage = (verdict.score * 100).toFixed(1);
    const actionClass = verdict.action === 'block' ? 'block' : 
                       verdict.action === 'warn' ? 'warn' : 'allow';

    resultDiv.innerHTML = `
      <div class="verdict ${actionClass}">
        <div class="verdict-header">
          <div class="verdict-icon">
            ${verdict.action === 'block' ? '🚨' : 
              verdict.action === 'warn' ? '⚠️' : '✅'}
          </div>
          <div class="verdict-info">
            <div class="verdict-action">${verdict.action.toUpperCase()}</div>
            <div class="verdict-score">Risk: ${riskPercentage}%</div>
          </div>
        </div>
        <div class="verdict-reasons">
          <h4>Reasons:</h4>
          <ul>
            ${verdict.reasons.map(reason => `<li>${reason}</li>`).join('')}
          </ul>
        </div>
        ${verdict.explain.tokens.length > 0 ? `
          <div class="verdict-tokens">
            <h4>Key Tokens:</h4>
            <div class="tokens">
              ${verdict.explain.tokens.slice(0, 5).map(token => 
                `<span class="token" style="opacity: ${token.weight}">${token.token}</span>`
              ).join('')}
            </div>
          </div>
        ` : ''}
      </div>
    `;
  }

  private showResult(message: string, type: 'loading' | 'error' | 'success') {
    const resultDiv = document.getElementById('check-result');
    if (!resultDiv) return;

    resultDiv.innerHTML = `
      <div class="result ${type}">
        ${type === 'loading' ? '⏳' : type === 'error' ? '❌' : '✅'} ${message}
      </div>
    `;
  }

  private async loadRecentActivity() {
    const activityDiv = document.getElementById('recent-activity');
    if (!activityDiv) return;

    try {
      const response = await chrome.runtime.sendMessage({ action: 'getDemoEvents' });
      const events = response || [];

      if (events.length === 0) {
        activityDiv.innerHTML = '<div class="no-activity">No recent activity</div>';
        return;
      }

      const recentEvents = events.slice(0, 3);
      activityDiv.innerHTML = recentEvents.map((event: any) => `
        <div class="activity-item">
          <div class="activity-icon ${event.action}">
            ${event.action === 'block' ? '🚨' : 
              event.action === 'warn' ? '⚠️' : '✅'}
          </div>
          <div class="activity-info">
            <div class="activity-url">${event.url}</div>
            <div class="activity-time">${new Date(event.timestamp).toLocaleTimeString()}</div>
          </div>
        </div>
      `).join('');
    } catch (error) {
      console.error('Error loading recent activity:', error);
      activityDiv.innerHTML = '<div class="no-activity">Error loading activity</div>';
    }
  }
}

// Initialize popup when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  new PhishGuardPopup();
});