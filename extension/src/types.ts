export interface PhishingVerdict {
  score: number;
  action: 'allow' | 'warn' | 'block';
  reasons: string[];
  explain: {
    tokens: Array<{ token: string; weight: number }>;
    url_features: any;
    visual_cues?: any;
  };
}

export interface SecurityEvent {
  id: string;
  timestamp: string;
  source: 'email' | 'sms' | 'web';
  sender: string;
  subject: string;
  body: string;
  url: string;
  final_url: string;
  label: string;
  score: number;
  action: 'allow' | 'warn' | 'block';
}

export interface ExtensionSettings {
  enabled: boolean;
  demoMode: boolean;
  apiUrl: string;
  autoCheck: boolean;
  showNotifications: boolean;
}

export interface BannerConfig {
  type: 'block' | 'warn';
  title: string;
  message: string;
  action: string;
  url: string;
}