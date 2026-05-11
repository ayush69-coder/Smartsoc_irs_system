/**
 * Storage service for managing extension settings
 */

export interface Settings {
  demoMode: boolean;
  enabled: boolean;
  apiUrl: string;
  notifications: boolean;
}

export class StorageService {
  private defaultSettings: Settings = {
    demoMode: true,
    enabled: true,
    apiUrl: 'http://localhost:8000/api',
    notifications: true
  };

  async getSettings(): Promise<Settings> {
    try {
      const result = await chrome.storage.local.get(['settings']);
      return { ...this.defaultSettings, ...result.settings };
    } catch (error) {
      console.error('Error getting settings:', error);
      return this.defaultSettings;
    }
  }

  async updateSettings(settings: Partial<Settings>): Promise<void> {
    try {
      const currentSettings = await this.getSettings();
      const newSettings = { ...currentSettings, ...settings };
      await chrome.storage.local.set({ settings: newSettings });
    } catch (error) {
      console.error('Error updating settings:', error);
      throw error;
    }
  }

  async clearSettings(): Promise<void> {
    try {
      await chrome.storage.local.remove(['settings']);
    } catch (error) {
      console.error('Error clearing settings:', error);
      throw error;
    }
  }
}