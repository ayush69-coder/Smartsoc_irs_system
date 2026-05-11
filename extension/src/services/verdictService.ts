/**
 * Verdict service for checking URLs
 */

export interface Verdict {
  score: number;
  action: 'allow' | 'warn' | 'block';
  reasons: string[];
  explain: {
    tokens: Array<{ token: string; weight: number }>;
    url_features: Record<string, any>;
  };
}

export class VerdictService {
  private apiUrl: string;

  constructor() {
    this.apiUrl = 'http://localhost:8000/api';
  }

  async checkUrl(url: string): Promise<Verdict> {
    try {
      const response = await fetch(`${this.apiUrl}/verdict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: url,
          text: '', // We'll extract text from the page if needed
          source: 'web'
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error checking URL:', error);
      // Return a safe verdict if API is unavailable
      return {
        score: 0,
        action: 'allow',
        reasons: ['Unable to check URL - API unavailable'],
        explain: {
          tokens: [],
          url_features: {}
        }
      };
    }
  }

  getDemoVerdict(url: string): Verdict {
    // Demo verdicts for demonstration purposes
    const demoVerdicts: Record<string, Verdict> = {
      'bit.ly': {
        score: 0.85,
        action: 'block',
        reasons: ['Shortened URL detected', 'High risk of phishing'],
        explain: {
          tokens: [
            { token: 'bit.ly', weight: 0.8 },
            { token: 'shortened', weight: 0.6 }
          ],
          url_features: {
            is_shortener: true,
            length: 20
          }
        }
      },
      'suspicious-site.com': {
        score: 0.75,
        action: 'warn',
        reasons: ['Suspicious domain name', 'Unusual URL pattern'],
        explain: {
          tokens: [
            { token: 'suspicious', weight: 0.7 },
            { token: 'site', weight: 0.3 }
          ],
          url_features: {
            has_punycode: false,
            length: 50
          }
        }
      },
      'phishing-bank.com': {
        score: 0.95,
        action: 'block',
        reasons: ['Potential bank impersonation', 'High phishing risk'],
        explain: {
          tokens: [
            { token: 'phishing', weight: 0.9 },
            { token: 'bank', weight: 0.8 }
          ],
          url_features: {
            has_punycode: false,
            length: 60
          }
        }
      }
    };

    // Check for exact matches first
    if (demoVerdicts[url]) {
      return demoVerdicts[url];
    }

    // Check for partial matches
    for (const [pattern, verdict] of Object.entries(demoVerdicts)) {
      if (url.includes(pattern)) {
        return verdict;
      }
    }

    // Default safe verdict
    return {
      score: 0.1,
      action: 'allow',
      reasons: ['No threats detected'],
      explain: {
        tokens: [],
        url_features: {}
      }
    };
  }
}