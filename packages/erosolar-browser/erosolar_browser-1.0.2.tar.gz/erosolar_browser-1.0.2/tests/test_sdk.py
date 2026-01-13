"""Tests for EroSolar Browser SDK"""
import pytest
from unittest.mock import patch, MagicMock
import json

# Test imports
def test_import():
    """Test that SDK can be imported"""
    from erosolar_browser import Browser, CongressCampaign
    assert Browser is not None
    assert CongressCampaign is not None

def test_browser_init_no_connection():
    """Test Browser raises error when browser not running"""
    from erosolar_browser import Browser
    with pytest.raises(ConnectionError):
        Browser(port=19999)  # Port that won't have browser

@patch('erosolar_browser.requests.get')
@patch('erosolar_browser.requests.post')
def test_browser_navigate(mock_post, mock_get):
    """Test navigation with mocked API"""
    from erosolar_browser import Browser
    
    # Mock status check
    mock_get.return_value.json.return_value = {'hasWindow': True, 'hasApiKey': True}
    
    # Mock navigate
    mock_post.return_value.json.return_value = {'success': True}
    
    browser = Browser.__new__(Browser)
    browser.base_url = "http://localhost:9222"
    browser.timeout = 30
    
    result = browser.navigate("https://example.com")
    assert result.get('success') == True

@patch('erosolar_browser.requests.get')
@patch('erosolar_browser.requests.post')  
def test_browser_ai_command(mock_post, mock_get):
    """Test AI command with mocked API"""
    from erosolar_browser import Browser
    
    mock_get.return_value.json.return_value = {'hasWindow': True, 'hasApiKey': True, 'isRunning': False, 'historyLength': 5}
    mock_post.return_value.json.return_value = {'accepted': True}
    
    browser = Browser.__new__(Browser)
    browser.base_url = "http://localhost:9222"
    browser.timeout = 30
    
    # Test without waiting
    result = browser.ai("test command", wait=False)
    assert result.get('accepted') == True

def test_congress_campaign_init():
    """Test CongressCampaign initialization"""
    from erosolar_browser import Browser, CongressCampaign
    
    # Create mock browser
    mock_browser = MagicMock()
    
    campaign = CongressCampaign(mock_browser)
    assert campaign.browser == mock_browser
    assert 'name' in campaign.user_info
    assert 'email' in campaign.user_info

def test_congress_campaign_set_user_info():
    """Test setting user info"""
    from erosolar_browser import CongressCampaign
    
    mock_browser = MagicMock()
    campaign = CongressCampaign(mock_browser)
    
    campaign.set_user_info(name="Test User", email="test@test.com")
    
    assert campaign.user_info['name'] == "Test User"
    assert campaign.user_info['email'] == "test@test.com"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
