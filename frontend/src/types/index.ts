export interface User {
  id: string
  username: string
  role: 'viewer' | 'analyst' | 'admin'
  email: string
}

export interface SecurityEvent {
  id: string
  timestamp: string
  source: 'email' | 'sms' | 'web'
  sender: string
  subject: string
  body: string
  url: string
  final_url: string
  whois: Record<string, any>
  ssl_cert: Record<string, any>
  label: string
  verdict?: Verdict
}

export interface Verdict {
  score: number
  action: 'allow' | 'warn' | 'block'
  reasons: string[]
  explain: {
    tokens: Array<{ token: string; weight: number }>
    url_features: Record<string, any>
    visual_cues?: Record<string, any>
  }
}

export interface KPIMetric {
  label: string
  value: string | number
  change?: number
  trend?: 'up' | 'down' | 'stable'
}

export interface Policy {
  id: string
  name: string
  type: string
  enabled: boolean
  config: Record<string, any>
}

export interface Theme {
  mode: 'light' | 'dark'
}