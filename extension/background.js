// PhishGuard Pro Background Script
chrome.runtime.onInstalled.addListener(() => {
  console.log('PhishGuard Pro extension installed');
});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    // Check URL for phishing indicators
    checkUrl(tab.url, tabId);
  }
});

async function checkUrl(url, tabId) {
  try {
    const response = await fetch('http://localhost:8000/api/verdict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        url: url,
        text: '',
        source: 'extension'
      })
    });
    
    const result = await response.json();
    
    if (result.score > 0.7) {
      chrome.tabs.sendMessage(tabId, {
        action: 'showWarning',
        score: result.score,
        reasons: result.reasons
      });
    }
  } catch (error) {
    console.error('Error checking URL:', error);
  }
}
