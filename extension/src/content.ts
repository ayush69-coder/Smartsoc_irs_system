import { PhishingVerdict, SecurityEvent } from './types';

class PhishGuardContent {
  private isEnabled: boolean = true;
  private demoMode: boolean = true;

  constructor() {
    this.initialize();
  }

  private async initialize() {
    // Get settings from background script
    const settings = await this.getSettings();
    this.isEnabled = settings.enabled;
    this.demoMode = settings.demoMode;

    if (this.isEnabled) {
      this.setupPageAnalysis();
      this.setupMessageListener();
    }
  }

  private async getSettings(): Promise<any> {
    return new Promise((resolve) => {
      chrome.runtime.sendMessage({ action: 'getSettings' }, (response) => {
        resolve(response || { enabled: true, demoMode: true });
      });
    });
  }

  private setupPageAnalysis() {
    // Analyze page content when DOM is ready
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', () => this.analyzePage());
    } else {
      this.analyzePage();
    }
  }

  private async analyzePage() {
    const url = window.location.href;
    
    // Quick local check for demo mode
    if (this.demoMode) {
      const localVerdict = await this.quickLocalCheck(url);
      if (localVerdict) {
        this.handleVerdict(localVerdict);
        return;
      }
    }

    // Extract page content for analysis
    const pageContent = this.extractPageContent();
    
    // Send to background for analysis
    chrome.runtime.sendMessage({
      action: 'analyzePage',
      url: url,
      content: pageContent
    });
  }

  private async quickLocalCheck(url: string): Promise<PhishingVerdict | null> {
    try {
      const demoEvents = await this.getDemoEvents();
      const matchingEvent = demoEvents.find((event: SecurityEvent) => 
        event.url === url || event.final_url === url
      );
      
      if (matchingEvent) {
        return {
          score: matchingEvent.score,
          action: matchingEvent.action,
          reasons: [`Demo event: ${matchingEvent.label}`],
          explain: {
            tokens: this.extractTokens(document.body.textContent || ''),
            url_features: this.analyzeUrl(url),
            visual_cues: this.analyzeVisualCues()
          }
        };
      }
    } catch (error) {
      console.error('Error in quick local check:', error);
    }
    
    return null;
  }

  private async getDemoEvents(): Promise<SecurityEvent[]> {
    return new Promise((resolve) => {
      chrome.runtime.sendMessage({ action: 'getDemoEvents' }, (response) => {
        resolve(response || []);
      });
    });
  }

  private extractPageContent() {
    return {
      title: document.title,
      url: window.location.href,
      text: document.body.textContent || '',
      links: Array.from(document.querySelectorAll('a')).map(a => ({
        href: a.href,
        text: a.textContent?.trim() || ''
      })),
      forms: Array.from(document.querySelectorAll('form')).map(form => ({
        action: form.action,
        method: form.method,
        inputs: Array.from(form.querySelectorAll('input')).map(input => ({
          type: input.type,
          name: input.name,
          placeholder: input.placeholder
        }))
      }))
    };
  }

  private extractTokens(text: string): Array<{ token: string; weight: number }> {
    // Simple token extraction for demo
    const words = text.toLowerCase()
      .replace(/[^\w\s]/g, ' ')
      .split(/\s+/)
      .filter(word => word.length > 3);
    
    const tokenCounts: { [key: string]: number } = {};
    words.forEach(word => {
      tokenCounts[word] = (tokenCounts[word] || 0) + 1;
    });
    
    return Object.entries(tokenCounts)
      .map(([token, count]) => ({ token, weight: count / words.length }))
      .sort((a, b) => b.weight - a.weight)
      .slice(0, 10);
  }

  private analyzeUrl(url: string) {
    const urlObj = new URL(url);
    return {
      length: url.length,
      has_credentials: url.includes('@'),
      num_subdomains: urlObj.hostname.split('.').length - 2,
      is_shortener: this.isShortener(url),
      path_entropy: this.calculateEntropy(urlObj.pathname)
    };
  }

  private isShortener(url: string): boolean {
    const shorteners = ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly'];
    return shorteners.some(shortener => url.includes(shortener));
  }

  private calculateEntropy(text: string): number {
    const freq: { [key: string]: number } = {};
    for (const char of text) {
      freq[char] = (freq[char] || 0) + 1;
    }
    
    let entropy = 0;
    const length = text.length;
    for (const count of Object.values(freq)) {
      const p = count / length;
      entropy -= p * Math.log2(p);
    }
    
    return entropy;
  }

  private analyzeVisualCues() {
    return {
      impersonation_score: this.calculateImpersonationScore(),
      brand_detected: this.detectBrand(),
      layout_anomalies: this.detectLayoutAnomalies()
    };
  }

  private calculateImpersonationScore(): number {
    // Simple heuristic for demo
    const title = document.title.toLowerCase();
    const suspiciousKeywords = ['verify', 'urgent', 'security', 'account', 'suspended'];
    const brandKeywords = ['google', 'microsoft', 'apple', 'amazon', 'paypal'];
    
    let score = 0;
    suspiciousKeywords.forEach(keyword => {
      if (title.includes(keyword)) score += 0.2;
    });
    
    brandKeywords.forEach(brand => {
      if (title.includes(brand)) score += 0.1;
    });
    
    return Math.min(score, 1);
  }

  private detectBrand(): string | null {
    const title = document.title.toLowerCase();
    const brands = ['google', 'microsoft', 'apple', 'amazon', 'paypal', 'facebook'];
    
    for (const brand of brands) {
      if (title.includes(brand)) {
        return brand;
      }
    }
    
    return null;
  }

  private detectLayoutAnomalies(): string[] {
    const anomalies: string[] = [];
    
    // Check for suspicious form patterns
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
      const passwordInputs = form.querySelectorAll('input[type="password"]');
      const emailInputs = form.querySelectorAll('input[type="email"]');
      
      if (passwordInputs.length > 0 && emailInputs.length > 0) {
        anomalies.push('Login form detected');
      }
    });
    
    // Check for suspicious links
    const links = document.querySelectorAll('a');
    links.forEach(link => {
      const href = link.href;
      const text = link.textContent?.toLowerCase() || '';
      
      if (href !== text && text.includes('click here')) {
        anomalies.push('Suspicious link text');
      }
    });
    
    return anomalies;
  }

  private setupMessageListener() {
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      switch (request.action) {
        case 'showBanner':
          this.showBanner(request.config);
          break;
        case 'hideBanner':
          this.hideBanner();
          break;
        case 'analyzePage':
          this.analyzePage();
          break;
      }
    });
  }

  private handleVerdict(verdict: PhishingVerdict) {
    if (verdict.action === 'block') {
      this.showBlockBanner(verdict);
    } else if (verdict.action === 'warn') {
      this.showWarningBanner(verdict);
    }
  }

  private showBlockBanner(verdict: PhishingVerdict) {
    // This will be handled by the background script
    // The content script just provides the analysis data
  }

  private showWarningBanner(verdict: PhishingVerdict) {
    // This will be handled by the background script
    // The content script just provides the analysis data
  }

  private showBanner(config: any) {
    // Show custom banner based on config
    console.log('Showing banner:', config);
  }

  private hideBanner() {
    // Hide any existing banners
    const banners = document.querySelectorAll('[id^="phishguard-"]');
    banners.forEach(banner => banner.remove());
  }
}

// Initialize the content script
new PhishGuardContent();