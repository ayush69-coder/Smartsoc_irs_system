import { PhishingVerdict, SecurityEvent, ExtensionSettings } from './types';

class PhishGuardBackground {
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
    // Load settings from storage
    await this.loadSettings();
    
    // Set up listeners
    this.setupListeners();
    
    // Initialize demo mode
    if (this.settings.demoMode) {
      await this.initializeDemoMode();
    }
  }

  private async loadSettings() {
    try {
      const result = await chrome.storage.sync.get(['phishguard_settings']);
      if (result.phishguard_settings) {
        this.settings = { ...this.settings, ...result.phishguard_settings };
      }
    } catch (error) {
      console.error('Error loading settings:', error);
    }
  }

  private async saveSettings() {
    try {
      await chrome.storage.sync.set({ phishguard_settings: this.settings });
    } catch (error) {
      console.error('Error saving settings:', error);
    }
  }

  private setupListeners() {
    // Handle tab updates
    chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
      if (changeInfo.status === 'complete' && tab.url && this.settings.enabled) {
        this.checkUrl(tab.url, tabId);
      }
    });

    // Handle messages from content script
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      this.handleMessage(request, sender, sendResponse);
      return true; // Keep message channel open for async response
    });

    // Handle extension icon click
    chrome.action.onClicked.addListener((tab) => {
      this.handleIconClick(tab);
    });
  }

  private async initializeDemoMode() {
    // Load demo redirects for quick local checks
    try {
      const response = await fetch(`${this.settings.apiUrl}/api/live`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      });
      
      if (response.ok) {
        const data = await response.json();
        const demoEvents = data.events || [];
        
        // Store demo events for quick access
        await chrome.storage.local.set({ 
          demo_events: demoEvents.slice(0, 50) // Store first 50 events
        });
      }
    } catch (error) {
      console.error('Error initializing demo mode:', error);
    }
  }

  private async checkUrl(url: string, tabId: number) {
    if (!this.settings.enabled || !url) return;

    try {
      // Quick local check first
      const localVerdict = await this.quickLocalCheck(url);
      if (localVerdict) {
        await this.handleVerdict(localVerdict, tabId, url);
        return;
      }

      // If not found locally, check with backend
      if (this.settings.autoCheck) {
        const verdict = await this.checkWithBackend(url);
        if (verdict) {
          await this.handleVerdict(verdict, tabId, url);
        }
      }
    } catch (error) {
      console.error('Error checking URL:', error);
    }
  }

  private async quickLocalCheck(url: string): Promise<PhishingVerdict | null> {
    try {
      const result = await chrome.storage.local.get(['demo_events']);
      const demoEvents = result.demo_events || [];
      
      // Find matching event
      const matchingEvent = demoEvents.find((event: SecurityEvent) => 
        event.url === url || event.final_url === url
      );
      
      if (matchingEvent) {
        return {
          score: matchingEvent.score,
          action: matchingEvent.action,
          reasons: [`Demo event: ${matchingEvent.label}`],
          explain: {
            tokens: [],
            url_features: {},
            visual_cues: {}
          }
        };
      }
    } catch (error) {
      console.error('Error in quick local check:', error);
    }
    
    return null;
  }

  private async checkWithBackend(url: string): Promise<PhishingVerdict | null> {
    try {
      const response = await fetch(`${this.settings.apiUrl}/api/verdict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          url: url,
          text: '', // Content script will provide this
          source: 'web'
        })
      });

      if (response.ok) {
        return await response.json();
      }
    } catch (error) {
      console.error('Error checking with backend:', error);
    }
    
    return null;
  }

  private async handleVerdict(verdict: PhishingVerdict, tabId: number, url: string) {
    if (verdict.action === 'block') {
      await this.showBlockBanner(tabId, verdict, url);
    } else if (verdict.action === 'warn') {
      await this.showWarningBanner(tabId, verdict, url);
    }
  }

  private async showBlockBanner(tabId: number, verdict: PhishingVerdict, url: string) {
    try {
      await chrome.scripting.executeScript({
        target: { tabId },
        func: this.injectBlockBanner,
        args: [verdict, url]
      });
    } catch (error) {
      console.error('Error showing block banner:', error);
    }
  }

  private async showWarningBanner(tabId: number, verdict: PhishingVerdict, url: string) {
    try {
      await chrome.scripting.executeScript({
        target: { tabId },
        func: this.injectWarningBanner,
        args: [verdict, url]
      });
    } catch (error) {
      console.error('Error showing warning banner:', error);
    }
  }

  private injectBlockBanner(verdict: PhishingVerdict, url: string) {
    // Remove existing banners
    const existingBanner = document.getElementById('phishguard-banner');
    if (existingBanner) {
      existingBanner.remove();
    }

    // Create block banner
    const banner = document.createElement('div');
    banner.id = 'phishguard-banner';
    banner.innerHTML = `
      <div style="
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: linear-gradient(135deg, #EF4444, #DC2626);
        color: white;
        padding: 16px;
        z-index: 10000;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      ">
        <div style="max-width: 1200px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between;">
          <div style="display: flex; align-items: center; gap: 12px;">
            <div style="
              width: 24px;
              height: 24px;
              background: white;
              border-radius: 50%;
              display: flex;
              align-items: center;
              justify-content: center;
              font-weight: bold;
              color: #EF4444;
            ">⚠</div>
            <div>
              <div style="font-weight: 600; font-size: 16px; margin-bottom: 4px;">
                🚨 PHISHING DETECTED
              </div>
              <div style="font-size: 14px; opacity: 0.9;">
                This site has been identified as a potential phishing attempt (Risk: ${(verdict.score * 100).toFixed(1)}%)
              </div>
            </div>
          </div>
          <div style="display: flex; gap: 8px;">
            <button id="phishguard-return" style="
              background: white;
              color: #EF4444;
              border: none;
              padding: 8px 16px;
              border-radius: 6px;
              font-weight: 600;
              cursor: pointer;
              font-size: 14px;
            ">Return to Safety</button>
            <button id="phishguard-dismiss" style="
              background: transparent;
              color: white;
              border: 1px solid white;
              padding: 8px 16px;
              border-radius: 6px;
              cursor: pointer;
              font-size: 14px;
            ">Dismiss</button>
          </div>
        </div>
      </div>
    `;

    // Add banner to page
    document.body.insertBefore(banner, document.body.firstChild);
    document.body.style.paddingTop = '80px';

    // Add event listeners
    const returnBtn = document.getElementById('phishguard-return');
    const dismissBtn = document.getElementById('phishguard-dismiss');

    returnBtn?.addEventListener('click', () => {
      window.location.href = 'https://www.google.com';
    });

    dismissBtn?.addEventListener('click', () => {
      banner.remove();
      document.body.style.paddingTop = '0';
    });
  }

  private injectWarningBanner(verdict: PhishingVerdict, url: string) {
    // Remove existing banners
    const existingBanner = document.getElementById('phishguard-warning');
    if (existingBanner) {
      existingBanner.remove();
    }

    // Create warning banner
    const banner = document.createElement('div');
    banner.id = 'phishguard-warning';
    banner.innerHTML = `
      <div style="
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #F59E0B, #D97706);
        color: white;
        padding: 12px 16px;
        border-radius: 8px;
        z-index: 10000;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        max-width: 300px;
        animation: slideIn 0.3s ease-out;
      ">
        <div style="display: flex; align-items: center; gap: 8px;">
          <div style="font-size: 18px;">⚠️</div>
          <div>
            <div style="font-weight: 600; font-size: 14px; margin-bottom: 2px;">
              Suspicious Site
            </div>
            <div style="font-size: 12px; opacity: 0.9;">
              Risk: ${(verdict.score * 100).toFixed(1)}%
            </div>
          </div>
          <button id="phishguard-warning-dismiss" style="
            background: transparent;
            color: white;
            border: none;
            font-size: 16px;
            cursor: pointer;
            margin-left: auto;
          ">×</button>
        </div>
      </div>
    `;

    // Add banner to page
    document.body.appendChild(banner);

    // Auto-dismiss after 10 seconds
    setTimeout(() => {
      if (banner.parentNode) {
        banner.remove();
      }
    }, 10000);

    // Add event listener
    const dismissBtn = document.getElementById('phishguard-warning-dismiss');
    dismissBtn?.addEventListener('click', () => {
      banner.remove();
    });
  }

  private async handleMessage(request: any, sender: chrome.runtime.MessageSender, sendResponse: (response?: any) => void) {
    switch (request.action) {
      case 'checkUrl':
        const verdict = await this.checkWithBackend(request.url);
        sendResponse(verdict);
        break;
      
      case 'getSettings':
        sendResponse(this.settings);
        break;
      
      case 'updateSettings':
        this.settings = { ...this.settings, ...request.settings };
        await this.saveSettings();
        sendResponse({ success: true });
        break;
      
      case 'getDemoEvents':
        const result = await chrome.storage.local.get(['demo_events']);
        sendResponse(result.demo_events || []);
        break;
      
      default:
        sendResponse({ error: 'Unknown action' });
    }
  }

  private async handleIconClick(tab: chrome.tabs.Tab) {
    if (tab.id) {
      try {
        await chrome.scripting.executeScript({
          target: { tabId: tab.id },
          func: () => {
            // Toggle extension popup or show quick check
            console.log('PhishGuard Pro: Quick check requested');
          }
        });
      } catch (error) {
        console.error('Error handling icon click:', error);
      }
    }
  }
}

// Initialize the background service
new PhishGuardBackground();