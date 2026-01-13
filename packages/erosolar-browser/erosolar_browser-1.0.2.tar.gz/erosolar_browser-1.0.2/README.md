# EroSolar AI Browser SDK

Control the EroSolar AI Browser from Python. Unlike Selenium/Playwright, you see everything happening in real-time in a visible browser window, powered by GPT-5.2.

## Installation

```bash
pip install erosolar-browser
```

## Quick Start

1. **Download and run the EroSolar AI Browser** from [americaisfinallyback.com/downloads](https://americaisfinallyback.com/downloads)

2. **Write your automation script:**

```python
from erosolar_browser import Browser

# Connect to the running browser
browser = Browser()

# Navigate to a page
browser.navigate("https://example.com")

# Use AI to do anything - just describe what you want
browser.ai("fill out the contact form with my info and submit it")

# Or use direct commands
browser.click("Submit")
browser.fill("email", "me@example.com")
```

## Features

- **Visual Automation**: See everything the browser does in real-time
- **AI-Powered**: Just describe what you want in plain English
- **Simple API**: Navigate, click, fill, scroll - all with one line
- **Congress Campaign**: Built-in tools for civic engagement

## API Reference

### Browser Class

```python
from erosolar_browser import Browser

browser = Browser(host="localhost", port=9222)

# Navigation
browser.navigate("https://example.com")
browser.back()
browser.forward()
browser.reload()

# Page Info
status = browser.status()
page = browser.get_page()  # Returns URL, title, text, forms, buttons

# Interactions
browser.click("Button Text")
browser.fill("field_name", "value")
browser.select("dropdown", "option")
browser.scroll("down")

# AI Commands - describe what you want
browser.ai("search for weather in Boston")
browser.ai("fill out this form with name John Doe, email john@example.com")
browser.ai("click the login button and enter credentials")

# Control
browser.stop()  # Stop current AI task
browser.wait(5)  # Wait 5 seconds
```

### Congress Campaign

```python
from erosolar_browser import Browser, CongressCampaign

browser = Browser()
campaign = CongressCampaign(browser)

# Set your info
campaign.set_user_info(
    name="Your Name",
    address="123 Main St",
    city="Boston",
    state="MA",
    zip="02134",
    phone="555-1234",
    email="you@example.com"
)

# Contact a single member
campaign.contact_member("Seth Moulton", topic="climate change")

# Or run a full campaign
members = ["Seth Moulton", "Elizabeth Warren", "Ed Markey"]
results = campaign.run_campaign(members, topic="healthcare", delay=30)
```

## How It Works

The SDK connects to the EroSolar AI Browser's API server (runs on port 9222 by default). The browser uses GPT-5.2 to understand your commands and execute them visually.

Unlike headless automation:
- You see everything happening
- The AI can handle complex forms and CAPTCHAs
- Natural language commands - no need to find CSS selectors

## Requirements

- Python 3.8+
- EroSolar AI Browser running (download from website)
- OpenAI API key configured in the browser

## License

MIT License - Use freely for civic engagement and automation.
