#!/usr/bin/env python3
"""
Enhanced URL Shortener
Adds URL validation, config file support, and better error handling
"""

import requests
import json
import sys
import re
from urllib.parse import urlparse
from pathlib import Path


class URLShortener:
    """URL shortener with validation and configuration support"""
    
    def __init__(self, config_path='config.json'):
        """Initialize with configuration"""
        self.config = self.load_config(config_path)
        self.api_key = self.config.get('bitly_api_key')
        
        if not self.api_key or self.api_key == 'YOUR_API_KEY_HERE':
            print("⚠️  Error: Please set your Bitly API key in config.json")
            print("   Get your API key from: https://bitly.com/a/settings/api")
            sys.exit(1)
    
    def load_config(self, config_path):
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  Config file '{config_path}' not found!")
            print("   Creating config.example.json - please rename and add your API key")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"⚠️  Invalid JSON in '{config_path}'")
            sys.exit(1)
    
    def validate_url(self, url):
        """
        Validate URL format and structure
        
        Args:
            url (str): URL to validate
            
        Returns:
            tuple: (is_valid, error_message)
        """
        # Check if empty
        if not url or not url.strip():
            return False, "URL cannot be empty"
        
        url = url.strip()
        
        # Add scheme if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Parse URL
        try:
            parsed = urlparse(url)
            
            # Check for valid scheme
            if parsed.scheme not in ['http', 'https']:
                return False, "URL must use http or https protocol"
            
            # Check for valid domain
            if not parsed.netloc:
                return False, "URL must have a valid domain"
            
            # Basic domain validation (has at least one dot)
            if '.' not in parsed.netloc:
                return False, "URL must have a valid domain (e.g., example.com)"
            
            # Check domain doesn't have invalid characters
            domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$'
            domain = parsed.netloc.split(':')[0]  # Remove port if present
            
            if not re.match(domain_pattern, domain):
                return False, "Invalid domain format"
            
            return True, url
            
        except Exception as e:
            return False, f"Invalid URL format: {str(e)}"
    
    def shorten_url(self, long_url):
        """
        Shorten a URL using Bitly API
        
        Args:
            long_url (str): URL to shorten
            
        Returns:
            tuple: (success, result_or_error_message)
        """
        # Validate URL first
        is_valid, result = self.validate_url(long_url)
        if not is_valid:
            return False, result
        
        # Use the validated/normalized URL
        validated_url = result
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        
        data = {"long_url": validated_url}
        
        # Try up to 3 times
        for attempt in range(3):
            try:
                response = requests.post(
                    "https://api-ssl.bitly.com/v4/shorten",
                    headers=headers,
                    data=json.dumps(data),
                    timeout=10
                )
                
                if response.status_code == 200:
                    link = response.json()['link']
                    return True, link
                elif response.status_code == 403:
                    return False, "Invalid API key. Please check your config.json"
                elif response.status_code == 400:
                    error_msg = response.json().get('message', 'Bad request')
                    return False, f"Invalid request: {error_msg}"
                else:
                    if attempt == 2:  # Last attempt
                        return False, f"API error (HTTP {response.status_code})"
                    
            except requests.exceptions.Timeout:
                if attempt == 2:
                    return False, "Request timed out after 3 attempts"
            except requests.exceptions.ConnectionError:
                if attempt == 2:
                    return False, "Connection error. Check your internet connection"
            except Exception as e:
                if attempt == 2:
                    return False, f"Unexpected error: {str(e)}"
        
        return False, "Failed after 3 attempts"


def main():
    """Main function to run the URL shortener"""
    print("=" * 50)
    print("🔗  Enhanced URL Shortener")
    print("=" * 50)
    
    # Initialize shortener
    shortener = URLShortener()
    
    # Get user input
    long_url = input("\n📎 Enter the long URL: ").strip()
    
    if not long_url:
        print("❌ No URL provided!")
        return
    
    print("\n⏳ Shortening URL...")
    
    # Shorten the URL
    success, result = shortener.shorten_url(long_url)
    
    if success:
        print(f"\n✅ Success!")
        print(f"📋 Shortened URL: {result}")
        print(f"\n💡 Copy and share: {result}")
    else:
        print(f"\n❌ Error: {result}")
        sys.exit(1)


if __name__ == "__main__":
    main()
