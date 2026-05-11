#!/usr/bin/env python3
"""
PhishGuard Pro - Windows Desktop Application

A standalone Windows desktop application for PhishGuard Pro
phishing detection and response platform.

Author: PhishGuard Pro Team
Version: 1.0.0
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import requests
import json
import threading
import webbrowser
from datetime import datetime
import os
import sys
from pathlib import Path
import subprocess
import queue
import time

class PhishGuardWindowsApp:
    """Main Windows Application Class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("PhishGuard Pro - Windows Desktop")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # Configure style
        self.setup_styles()
        
        # API Configuration
        self.api_base_url = "http://localhost:8000"
        self.is_backend_running = False
        
        # Queue for thread communication
        self.message_queue = queue.Queue()
        
        # Initialize UI
        self.setup_ui()
        self.check_backend_status()
        
        # Start message queue processor
        self.process_queue()
    
    def setup_styles(self):
        """Setup application styles and themes"""
        style = ttk.Style()
        
        # Configure theme
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'), foreground='#34495e')
        style.configure('Success.TLabel', foreground='#27ae60')
        style.configure('Warning.TLabel', foreground='#f39c12')
        style.configure('Error.TLabel', foreground='#e74c3c')
        
        # Configure buttons
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))
        style.configure('Danger.TButton', font=('Arial', 10, 'bold'), foreground='#e74c3c')
    
    def setup_ui(self):
        """Setup the main user interface"""
        # Create main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🛡️ PhishGuard Pro", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Status bar
        self.setup_status_bar(main_frame)
        
        # Main content area
        self.setup_main_content(main_frame)
        
        # Menu bar
        self.setup_menu()
    
    def setup_status_bar(self, parent):
        """Setup status bar"""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        status_frame.columnconfigure(1, weight=1)
        
        # Backend status
        self.backend_status_label = ttk.Label(status_frame, text="Backend: Checking...", style='Warning.TLabel')
        self.backend_status_label.grid(row=0, column=0, sticky=tk.W)
        
        # API URL
        self.api_url_label = ttk.Label(status_frame, text=f"API: {self.api_base_url}")
        self.api_url_label.grid(row=0, column=1, sticky=tk.E)
    
    def setup_main_content(self, parent):
        """Setup main content area with tabs"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # URL Analysis Tab
        self.setup_url_analysis_tab()
        
        # Live Feed Tab
        self.setup_live_feed_tab()
        
        # Settings Tab
        self.setup_settings_tab()
        
        # About Tab
        self.setup_about_tab()
    
    def setup_url_analysis_tab(self):
        """Setup URL analysis tab"""
        url_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(url_frame, text="🔍 URL Analysis")
        
        # URL input section
        input_frame = ttk.LabelFrame(url_frame, text="Enter URL to Analyze", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        input_frame.columnconfigure(1, weight=1)
        
        ttk.Label(input_frame, text="URL:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.url_entry = ttk.Entry(input_frame, width=50)
        self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.analyze_button = ttk.Button(input_frame, text="Analyze URL", command=self.analyze_url, style='Action.TButton')
        self.analyze_button.grid(row=0, column=2)
        
        # Results section
        results_frame = ttk.LabelFrame(url_frame, text="Analysis Results", padding="10")
        results_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(1, weight=1)
        
        # Score display
        self.score_frame = ttk.Frame(results_frame)
        self.score_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.score_label = ttk.Label(self.score_frame, text="Phishing Score: --", style='Header.TLabel')
        self.score_label.grid(row=0, column=0, sticky=tk.W)
        
        self.action_label = ttk.Label(self.score_frame, text="Action: --", style='Header.TLabel')
        self.action_label.grid(row=0, column=1, sticky=tk.W, padx=(20, 0))
        
        # Detailed results
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, width=70)
        self.results_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        url_frame.columnconfigure(0, weight=1)
        url_frame.rowconfigure(1, weight=1)
    
    def setup_live_feed_tab(self):
        """Setup live feed tab"""
        feed_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(feed_frame, text="📊 Live Feed")
        
        # Controls
        controls_frame = ttk.Frame(feed_frame)
        controls_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        controls_frame.columnconfigure(1, weight=1)
        
        ttk.Label(controls_frame, text="Filter:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.filter_entry = ttk.Entry(controls_frame, width=30)
        self.filter_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.refresh_button = ttk.Button(controls_frame, text="Refresh", command=self.refresh_live_feed, style='Action.TButton')
        self.refresh_button.grid(row=0, column=2, padx=(0, 10))
        
        self.auto_refresh_var = tk.BooleanVar()
        self.auto_refresh_check = ttk.Checkbutton(controls_frame, text="Auto-refresh", variable=self.auto_refresh_var, command=self.toggle_auto_refresh)
        self.auto_refresh_check.grid(row=0, column=3)
        
        # Live feed display
        self.live_feed_text = scrolledtext.ScrolledText(feed_frame, height=20, width=80)
        self.live_feed_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        feed_frame.columnconfigure(0, weight=1)
        feed_frame.rowconfigure(1, weight=1)
        
        # Auto-refresh timer
        self.auto_refresh_timer = None
    
    def setup_settings_tab(self):
        """Setup settings tab"""
        settings_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(settings_frame, text="⚙️ Settings")
        
        # API Settings
        api_frame = ttk.LabelFrame(settings_frame, text="API Configuration", padding="10")
        api_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        api_frame.columnconfigure(1, weight=1)
        
        ttk.Label(api_frame, text="Backend URL:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.api_url_entry = ttk.Entry(api_frame, width=40)
        self.api_url_entry.insert(0, self.api_base_url)
        self.api_url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.update_api_button = ttk.Button(api_frame, text="Update", command=self.update_api_url, style='Action.TButton')
        self.update_api_button.grid(row=0, column=2)
        
        # Backend Control
        backend_frame = ttk.LabelFrame(settings_frame, text="Backend Control", padding="10")
        backend_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.start_backend_button = ttk.Button(backend_frame, text="Start Backend", command=self.start_backend, style='Action.TButton')
        self.start_backend_button.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_backend_button = ttk.Button(backend_frame, text="Stop Backend", command=self.stop_backend, style='Danger.TButton')
        self.stop_backend_button.grid(row=0, column=1, padx=(0, 10))
        
        # Logs
        logs_frame = ttk.LabelFrame(settings_frame, text="Application Logs", padding="10")
        logs_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        logs_frame.columnconfigure(0, weight=1)
        logs_frame.rowconfigure(0, weight=1)
        
        self.logs_text = scrolledtext.ScrolledText(logs_frame, height=10, width=80)
        self.logs_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        settings_frame.columnconfigure(0, weight=1)
        settings_frame.rowconfigure(2, weight=1)
    
    def setup_about_tab(self):
        """Setup about tab"""
        about_frame = ttk.Frame(self.notebook, padding="20")
        self.notebook.add(about_frame, text="ℹ️ About")
        
        # App info
        info_text = """
🛡️ PhishGuard Pro - Windows Desktop Application

Version: 1.0.0
Author: PhishGuard Pro Team

Features:
• Real-time URL analysis
• Live phishing feed monitoring
• AI-powered threat detection
• Easy-to-use desktop interface

This Windows application provides a user-friendly interface
for the PhishGuard Pro phishing detection platform.

For more information, visit our GitHub repository:
https://github.com/vishxtr/HACKATHON_REAL2.0

© 2024 PhishGuard Pro. All rights reserved.
        """
        
        about_text = scrolledtext.ScrolledText(about_frame, height=20, width=70, wrap=tk.WORD)
        about_text.insert(tk.END, info_text)
        about_text.config(state=tk.DISABLED)
        about_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        about_frame.columnconfigure(0, weight=1)
        about_frame.rowconfigure(0, weight=1)
    
    def setup_menu(self):
        """Setup menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export Results", command=self.export_results)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Check Backend Status", command=self.check_backend_status)
        tools_menu.add_command(label="Open Backend Dashboard", command=self.open_backend_dashboard)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Documentation", command=self.open_documentation)
        help_menu.add_command(label="About", command=self.show_about)
    
    def check_backend_status(self):
        """Check if backend is running"""
        def check_status():
            try:
                response = requests.get(f"{self.api_base_url}/api/health", timeout=5)
                if response.status_code == 200:
                    self.message_queue.put(("backend_status", "Backend: Running", "success"))
                else:
                    self.message_queue.put(("backend_status", "Backend: Error", "error"))
            except requests.exceptions.RequestException:
                self.message_queue.put(("backend_status", "Backend: Not Running", "error"))
        
        threading.Thread(target=check_status, daemon=True).start()
    
    def analyze_url(self):
        """Analyze URL for phishing"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL to analyze")
            return
        
        def analyze():
            try:
                self.message_queue.put(("log", f"Analyzing URL: {url}"))
                
                # Prepare request data
                data = {
                    "url": url,
                    "text": "",
                    "source": "windows_app"
                }
                
                response = requests.post(f"{self.api_base_url}/api/verdict", json=data, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    self.message_queue.put(("analysis_result", result))
                else:
                    self.message_queue.put(("error", f"Analysis failed: {response.status_code}"))
                    
            except requests.exceptions.RequestException as e:
                self.message_queue.put(("error", f"Connection error: {str(e)}"))
        
        threading.Thread(target=analyze, daemon=True).start()
    
    def refresh_live_feed(self):
        """Refresh live feed data"""
        def refresh():
            try:
                self.message_queue.put(("log", "Refreshing live feed..."))
                
                response = requests.get(f"{self.api_base_url}/api/live", timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    self.message_queue.put(("live_feed", data))
                else:
                    self.message_queue.put(("error", f"Failed to fetch live feed: {response.status_code}"))
                    
            except requests.exceptions.RequestException as e:
                self.message_queue.put(("error", f"Connection error: {str(e)}"))
        
        threading.Thread(target=refresh, daemon=True).start()
    
    def toggle_auto_refresh(self):
        """Toggle auto-refresh for live feed"""
        if self.auto_refresh_var.get():
            self.start_auto_refresh()
        else:
            self.stop_auto_refresh()
    
    def start_auto_refresh(self):
        """Start auto-refresh timer"""
        self.auto_refresh_timer = self.root.after(5000, self.auto_refresh_callback)
    
    def stop_auto_refresh(self):
        """Stop auto-refresh timer"""
        if self.auto_refresh_timer:
            self.root.after_cancel(self.auto_refresh_timer)
            self.auto_refresh_timer = None
    
    def auto_refresh_callback(self):
        """Auto-refresh callback"""
        if self.auto_refresh_var.get():
            self.refresh_live_feed()
            self.auto_refresh_timer = self.root.after(5000, self.auto_refresh_callback)
    
    def update_api_url(self):
        """Update API URL"""
        new_url = self.api_url_entry.get().strip()
        if new_url:
            self.api_base_url = new_url
            self.api_url_label.config(text=f"API: {self.api_base_url}")
            self.log_message(f"API URL updated to: {self.api_base_url}")
            self.check_backend_status()
    
    def start_backend(self):
        """Start backend server"""
        def start():
            try:
                self.log_message("Starting backend server...")
                # This would start the backend server
                # For now, just check if it's running
                self.check_backend_status()
            except Exception as e:
                self.message_queue.put(("error", f"Failed to start backend: {str(e)}"))
        
        threading.Thread(target=start, daemon=True).start()
    
    def stop_backend(self):
        """Stop backend server"""
        self.log_message("Backend stop requested (not implemented)")
    
    def export_results(self):
        """Export analysis results"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.results_text.get(1.0, tk.END))
                self.log_message(f"Results exported to: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export results: {str(e)}")
    
    def open_backend_dashboard(self):
        """Open backend dashboard in browser"""
        webbrowser.open(f"{self.api_base_url}/docs")
    
    def open_documentation(self):
        """Open documentation"""
        webbrowser.open("https://github.com/vishxtr/HACKATHON_REAL2.0")
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About PhishGuard Pro", 
                           "PhishGuard Pro Windows Desktop Application\n\n"
                           "Version 1.0.0\n"
                           "AI-Powered Phishing Detection Platform")
    
    def log_message(self, message):
        """Log message to logs text area"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # Switch to settings tab to show logs
        self.notebook.select(2)  # Settings tab
        
        self.logs_text.insert(tk.END, log_entry)
        self.logs_text.see(tk.END)
    
    def process_queue(self):
        """Process messages from queue"""
        try:
            while True:
                message_type, data = self.message_queue.get_nowait()
                
                if message_type == "backend_status":
                    text, style = data
                    self.backend_status_label.config(text=text, style=f'{style}.TLabel')
                    self.is_backend_running = (style == "success")
                
                elif message_type == "analysis_result":
                    self.display_analysis_result(data)
                
                elif message_type == "live_feed":
                    self.display_live_feed(data)
                
                elif message_type == "error":
                    self.log_message(f"Error: {data}")
                    messagebox.showerror("Error", data)
                
                elif message_type == "log":
                    self.log_message(data)
                    
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.process_queue)
    
    def display_analysis_result(self, result):
        """Display analysis result"""
        score = result.get('score', 0)
        action = result.get('action', 'Unknown')
        reasons = result.get('reasons', [])
        explain = result.get('explain', {})
        
        # Update score display
        self.score_label.config(text=f"Phishing Score: {score:.2f}")
        self.action_label.config(text=f"Action: {action}")
        
        # Color code based on score
        if score > 0.7:
            self.score_label.config(style='Error.TLabel')
        elif score > 0.4:
            self.score_label.config(style='Warning.TLabel')
        else:
            self.score_label.config(style='Success.TLabel')
        
        # Display detailed results
        self.results_text.delete(1.0, tk.END)
        
        result_text = f"""Analysis Results for URL:
{'='*50}

Phishing Score: {score:.2f}
Recommended Action: {action}

Reasons:
{chr(10).join(f'• {reason}' for reason in reasons)}

Detailed Analysis:
{json.dumps(explain, indent=2)}

Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        self.results_text.insert(tk.END, result_text)
        self.log_message(f"Analysis complete - Score: {score:.2f}, Action: {action}")
    
    def display_live_feed(self, data):
        """Display live feed data"""
        events = data.get('events', [])
        total = data.get('total', 0)
        
        self.live_feed_text.delete(1.0, tk.END)
        
        feed_text = f"""Live Phishing Feed - {total} events
{'='*60}

"""
        
        for event in events[:20]:  # Show last 20 events
            timestamp = event.get('timestamp', 'Unknown')
            source = event.get('source', 'Unknown')
            sender = event.get('sender', 'Unknown')
            subject = event.get('subject', 'No Subject')
            score = event.get('score', 0)
            action = event.get('action', 'Unknown')
            
            feed_text += f"""[{timestamp}] {source.upper()}
From: {sender}
Subject: {subject}
Score: {score:.2f} | Action: {action}
{'-'*60}

"""
        
        self.live_feed_text.insert(tk.END, feed_text)
        self.log_message(f"Live feed updated - {total} events")

def main():
    """Main entry point"""
    root = tk.Tk()
    app = PhishGuardWindowsApp(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()