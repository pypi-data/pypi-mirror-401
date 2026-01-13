#!/usr/bin/env python3
"""
EroSolar AI Browser SDK

Control the AI Browser from Python. The browser runs visually while your script controls it.

Usage:
    from erosolar_browser import Browser
    
    browser = Browser()
    browser.navigate("https://example.com")
    browser.ai("fill out the contact form")
"""

import requests
import time
from typing import Dict, List, Optional

__version__ = "1.0.2"


class Browser:
    """Control the EroSolar AI Browser from Python."""
    
    def __init__(self, host: str = "localhost", ports: List[int] = None):
        """
        Connect to the browser.
        
        Args:
            host: Browser host (default: localhost)
            ports: List of ports to try (default: [9222, 9223, 9224])
        """
        self.host = host
        self.ports = ports or [9222, 9223, 9224]
        self.base_url = None
        self.timeout = 30
        
        self._connect()
    
    def _connect(self):
        """Find and connect to the browser API."""
        for port in self.ports:
            url = f"http://{self.host}:{port}"
            try:
                resp = requests.get(f"{url}/api/status", timeout=3)
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get('ready') or data.get('hasWindow'):
                        self.base_url = url
                        print(f"✓ Connected to EroSolar AI Browser on port {port}")
                        if data.get('hasApiKey'):
                            print("  API Key: configured")
                        return
            except:
                continue
        
        raise ConnectionError(
            "Cannot connect to browser.\n"
            "Make sure EroSolar AI Browser is running:\n"
            "  cd electron-ai-browser && npm run dev"
        )
    
    def _get(self, endpoint: str) -> Dict:
        """Make GET request."""
        try:
            resp = requests.get(f"{self.base_url}{endpoint}", timeout=self.timeout)
            return resp.json()
        except Exception as e:
            return {"error": str(e)}
    
    def _post(self, endpoint: str, data: Dict = None) -> Dict:
        """Make POST request."""
        try:
            resp = requests.post(f"{self.base_url}{endpoint}", json=data or {}, timeout=self.timeout)
            return resp.json()
        except Exception as e:
            return {"error": str(e)}
    
    # === Status & Info ===
    
    def status(self) -> Dict:
        """Get browser status."""
        return self._get("/api/status")
    
    def get_page(self) -> Dict:
        """Get current page info (url, title, text, form fields, buttons)."""
        return self._get("/api/page")
    
    # === Navigation ===
    
    def navigate(self, url: str, wait: float = 2.0) -> Dict:
        """
        Navigate to a URL.
        
        Args:
            url: URL to navigate to (https:// added if missing)
            wait: Seconds to wait for page load
        """
        if not url.startswith("http"):
            url = f"https://{url}"
        result = self._post("/api/navigate", {"url": url})
        if wait > 0:
            time.sleep(wait)
        return result
    
    # === AI Commands ===
    
    def ai(self, command: str, wait: bool = True, timeout: int = 120) -> Dict:
        """
        Run an AI command - describe what you want in plain English.
        
        Args:
            command: What you want the AI to do
            wait: Wait for completion (default: True)
            timeout: Max seconds to wait
        
        Examples:
            browser.ai("fill out the contact form with name John Doe")
            browser.ai("click the Submit button")
            browser.ai("search for weather in Boston")
        """
        result = self._post("/api/run", {"command": command})
        
        if result.get("error"):
            print(f"  ✗ Error: {result['error']}")
            return result
        
        if result.get("accepted"):
            print(f"  → Running: {command[:50]}...")
            
            if wait:
                return self._wait_for_completion(timeout)
        
        return result
    
    def _wait_for_completion(self, timeout: int) -> Dict:
        """Wait for AI task to complete."""
        start = time.time()
        last_step = 0
        
        while time.time() - start < timeout:
            status = self.status()
            
            history = status.get("historyLength", 0)
            if history > last_step:
                last_step = history
                print(f"  Step {last_step}...")
            
            if not status.get("isRunning") and last_step > 0:
                print("  ✓ Complete")
                return {"success": True, "steps": last_step}
            
            time.sleep(1.5)
        
        return {"success": False, "error": "Timeout", "steps": last_step}
    
    def stop(self) -> Dict:
        """Stop the current AI task."""
        return self._post("/api/stop")
    
    # === Convenience Methods ===
    
    def wait(self, seconds: float):
        """Wait for specified seconds."""
        time.sleep(seconds)
    
    def is_running(self) -> bool:
        """Check if AI is currently running a task."""
        return self.status().get("isRunning", False)


class CongressCampaign:
    """Helper for contacting Congress members."""
    
    def __init__(self, browser: Browser):
        self.browser = browser
        self.user_info = {
            "name": "Bo Shang",
            "address": "10 McCafferty Way",
            "city": "Burlington",
            "state": "MA", 
            "zip": "01803",
            "phone": "508-260-0326",
            "email": "bo@shang.software"
        }
    
    def set_user_info(self, **kwargs):
        """Update user info for forms."""
        self.user_info.update(kwargs)
    
    def contact_member(self, name: str, topic: str = "impeachment") -> Dict:
        """Contact a Congress member about a topic."""
        lastname = name.lower().split()[-1]
        
        # Try House then Senate
        for site in [f"{lastname}.house.gov", f"{lastname}.senate.gov"]:
            url = f"https://{site}/contact"
            print(f"  Trying {url}...")
            
            self.browser.navigate(url, wait=3)
            page = self.browser.get_page()
            
            if page.get("url") and "not found" not in page.get("title", "").lower():
                # Found it - use AI to fill
                cmd = f"""Fill out this contact form:
                - Name: {self.user_info['name']}
                - Address: {self.user_info['address']}, {self.user_info['city']} {self.user_info['state']} {self.user_info['zip']}
                - Email: {self.user_info['email']}
                - Phone: {self.user_info['phone']}
                - Subject/Topic: {topic}
                - Message: Write a compelling message about {topic}
                Then click Submit."""
                
                return self.browser.ai(cmd)
        
        return {"success": False, "error": f"Could not find {name}'s contact page"}


# Test when run directly
if __name__ == "__main__":
    print("EroSolar Browser SDK Test")
    print("=" * 40)
    
    try:
        b = Browser()
        print("\nStatus:", b.status())
        print("\nPage:", b.get_page())
        print("\n✓ SDK working!")
    except ConnectionError as e:
        print(f"\n✗ {e}")
