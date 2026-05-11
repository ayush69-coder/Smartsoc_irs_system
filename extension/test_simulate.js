#!/usr/bin/env node

/**
 * PhishGuard Pro Extension Test Simulation
 * Simulates the background script logic for CI/testing
 */

const fs = require('fs');
const path = require('path');

// Mock Chrome APIs for testing
const mockChrome = {
    runtime: {
        sendMessage: (message, callback) => {
            console.log('📤 Sending message:', message);
            
            // Simulate API responses
            if (message.action === 'checkUrl') {
                const mockVerdict = {
                    score: 0.85,
                    action: 'block',
                    reasons: ['High risk score detected', 'Suspicious domain pattern'],
                    explain: {
                        tokens: [
                            { token: 'urgent', weight: 0.9 },
                            { token: 'verify', weight: 0.8 },
                            { token: 'account', weight: 0.7 },
                            { token: 'security', weight: 0.6 }
                        ],
                        url_features: {
                            length: 45,
                            has_credentials: false,
                            num_subdomains: 2,
                            is_shortener: false
                        },
                        visual_cues: {
                            impersonation_score: 0.8,
                            brand_detected: 'bank'
                        }
                    }
                };
                callback(mockVerdict);
            } else if (message.action === 'getSettings') {
                callback({
                    enabled: true,
                    demoMode: true,
                    apiUrl: 'http://localhost:8000',
                    autoCheck: true,
                    showNotifications: true
                });
            } else {
                callback({ error: 'Unknown action' });
            }
        }
    },
    storage: {
        local: {
            get: (keys, callback) => {
                console.log('📦 Getting from storage:', keys);
                callback({ demo_events: [] });
            },
            set: (data, callback) => {
                console.log('💾 Setting to storage:', data);
                if (callback) callback();
            }
        }
    },
    tabs: {
        onUpdated: {
            addListener: (callback) => {
                console.log('👂 Added tab update listener');
            }
        }
    },
    action: {
        onClicked: {
            addListener: (callback) => {
                console.log('👂 Added action click listener');
            }
        }
    }
};

// Mock DOM for banner injection
const mockDOM = {
    createElement: (tag) => {
        console.log(`🏗️  Creating ${tag} element`);
        return {
            id: 'phishguard-banner',
            innerHTML: '',
            style: {},
            addEventListener: (event, callback) => {
                console.log(`👂 Added ${event} listener`);
            }
        };
    },
    body: {
        insertBefore: (element, reference) => {
            console.log('📄 Inserting banner into DOM');
        },
        firstChild: null,
        style: {}
    },
    querySelectorAll: (selector) => {
        console.log(`🔍 Querying selector: ${selector}`);
        return [];
    }
};

// Simulate the background script logic
class PhishGuardSimulator {
    constructor() {
        this.settings = {
            enabled: true,
            demoMode: true,
            apiUrl: 'http://localhost:8000',
            autoCheck: true,
            showNotifications: true
        };
        
        this.demoEvents = [
            {
                id: 'demo-001',
                url: 'https://fake-bank-verification.com/verify',
                final_url: 'https://fake-bank-verification.com/verify',
                score: 0.85,
                action: 'block',
                label: 'phishing'
            },
            {
                id: 'demo-002', 
                url: 'https://microsoft-security-alert.net/update',
                final_url: 'https://microsoft-security-alert.net/update',
                score: 0.75,
                action: 'warn',
                label: 'phishing'
            }
        ];
    }

    async quickLocalCheck(url) {
        console.log(`🔍 Quick local check for: ${url}`);
        
        const matchingEvent = this.demoEvents.find(event => 
            event.url === url || event.final_url === url
        );
        
        if (matchingEvent) {
            console.log('✅ Found matching demo event');
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
        
        console.log('❌ No matching demo event found');
        return null;
    }

    async checkWithBackend(url) {
        console.log(`🌐 Checking with backend: ${url}`);
        
        // Simulate API call
        return new Promise((resolve) => {
            setTimeout(() => {
                const verdict = {
                    score: 0.85,
                    action: 'block',
                    reasons: ['High risk score detected', 'Suspicious domain pattern'],
                    explain: {
                        tokens: [
                            { token: 'urgent', weight: 0.9 },
                            { token: 'verify', weight: 0.8 },
                            { token: 'account', weight: 0.7 }
                        ],
                        url_features: {
                            length: url.length,
                            has_credentials: url.includes('@'),
                            num_subdomains: url.split('.').length - 2,
                            is_shortener: false
                        },
                        visual_cues: {
                            impersonation_score: 0.8,
                            brand_detected: 'bank'
                        }
                    }
                };
                resolve(verdict);
            }, 100);
        });
    }

    async handleVerdict(verdict, url) {
        console.log(`🎯 Handling verdict for ${url}:`, verdict.action);
        
        if (verdict.action === 'block') {
            this.showBlockBanner(verdict, url);
        } else if (verdict.action === 'warn') {
            this.showWarningBanner(verdict, url);
        }
    }

    showBlockBanner(verdict, url) {
        console.log('🚨 Showing BLOCK banner');
        
        const banner = mockDOM.createElement('div');
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
        
        mockDOM.body.insertBefore(banner, mockDOM.body.firstChild);
        console.log('✅ Block banner injected into DOM');
    }

    showWarningBanner(verdict, url) {
        console.log('⚠️  Showing WARNING banner');
        
        const banner = mockDOM.createElement('div');
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
                max-width: 300px;
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
        
        mockDOM.body.insertBefore(banner, null);
        console.log('✅ Warning banner injected into DOM');
    }

    async simulateExtensionFlow() {
        console.log('🚀 Starting PhishGuard Pro Extension Simulation');
        console.log('=' .repeat(50));
        
        // Test URLs
        const testUrls = [
            'https://fake-bank-verification.com/verify',
            'https://microsoft-security-alert.net/update',
            'https://google.com/search',
            'https://suspicious-phishing-site.com/login'
        ];
        
        for (const url of testUrls) {
            console.log(`\n🔍 Testing URL: ${url}`);
            console.log('-'.repeat(30));
            
            // Quick local check
            const localVerdict = await this.quickLocalCheck(url);
            if (localVerdict) {
                await this.handleVerdict(localVerdict, url);
                continue;
            }
            
            // Backend check
            const backendVerdict = await this.checkWithBackend(url);
            await this.handleVerdict(backendVerdict, url);
        }
        
        console.log('\n✅ Extension simulation completed successfully!');
        console.log('=' .repeat(50));
    }
}

// Run the simulation
const simulator = new PhishGuardSimulator();
simulator.simulateExtensionFlow().catch(console.error);