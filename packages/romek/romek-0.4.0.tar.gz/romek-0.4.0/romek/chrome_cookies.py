"""Chrome cookie decryption utilities."""

import os
import sys
import browser_cookie3
from typing import Dict, List


def _get_chrome_profiles_dir() -> str:
    """Get the Chrome profiles directory based on OS.
    
    Returns:
        Path to Chrome profiles directory
    """
    if sys.platform == "darwin":  # Mac
        return os.path.expanduser("~/Library/Application Support/Google/Chrome/")
    elif sys.platform == "win32":  # Windows
        return os.path.expandvars("%LOCALAPPDATA%\\Google\\Chrome\\User Data\\")
    else:  # Linux
        return os.path.expanduser("~/.config/google-chrome/")


def _list_available_profiles() -> List[str]:
    """List available Chrome profiles.
    
    Returns:
        List of available profile names
    """
    profiles_dir = _get_chrome_profiles_dir()
    if not os.path.exists(profiles_dir):
        return []
    
    profiles = []
    try:
        for item in os.listdir(profiles_dir):
            item_path = os.path.join(profiles_dir, item)
            if os.path.isdir(item_path) and (item == "Default" or item.startswith("Profile")):
                profiles.append(item)
    except OSError:
        pass
    
    return sorted(profiles)


def grab_chrome_cookies(domain: str, profile: str = "Default") -> Dict[str, str]:
    """Grab cookies from Chrome for a specific domain.
    
    Args:
        domain: The domain to get cookies for
        profile: Chrome profile name to use (default: "Default")
        
    Returns:
        Dictionary of cookie name-value pairs
        
    Raises:
        RuntimeError: If unable to access Chrome cookies
    """
    try:
        # Normalize domain (remove protocol)
        domain_normalized = domain.strip().lower()
        domain_normalized = domain_normalized.replace('https://', '').replace('http://', '').split('/')[0]
        
        # Get profiles directory
        profiles_dir = _get_chrome_profiles_dir()
        
        # Check if Chrome is installed (profiles directory exists)
        if not os.path.exists(profiles_dir):
            raise RuntimeError("Chrome not detected. Is Chrome installed?")
        
        # Build profile directory path
        profile_dir = os.path.join(profiles_dir, profile)
        
        # Check if profile directory exists
        if not os.path.exists(profile_dir):
            available_profiles = _list_available_profiles()
            if available_profiles:
                profiles_str = ", ".join(available_profiles)
                raise RuntimeError(f"Profile '{profile}' not found. Available profiles: {profiles_str}")
            else:
                raise RuntimeError(f"Profile '{profile}' not found. No profiles available.")
        
        # Build Chrome cookie file path based on OS and profile
        if sys.platform == "darwin":  # Mac
            cookie_file = os.path.join(profile_dir, "Cookies")
        elif sys.platform == "win32":  # Windows
            cookie_file = os.path.join(profile_dir, "Network", "Cookies")
        else:  # Linux
            cookie_file = os.path.join(profile_dir, "Cookies")
        
        # Check if cookie file exists
        if not os.path.exists(cookie_file):
            raise RuntimeError("Chrome not detected. Is Chrome installed?")
        
        # Use browser-cookie3 to get cookies from Chrome
        try:
            cj = browser_cookie3.chrome(cookie_file=cookie_file, domain_name=domain_normalized)
        except Exception as e:
            # Check if it's a database lock error (Chrome is open)
            error_str = str(e).lower()
            if "locked" in error_str or "database is locked" in error_str or "sqlite" in error_str:
                raise RuntimeError("Chrome is open. Close Chrome and try again.")
            # Re-raise other errors
            raise
        
        # Convert CookieJar to dictionary format
        cookies = {}
        for cookie in cj:
            cookies[cookie.name] = cookie.value
        
        # Check if no cookies were found
        if not cookies:
            raise RuntimeError(f"No session found for {domain}. Are you logged in on Chrome?")
        
        return cookies
    except RuntimeError:
        # Re-raise RuntimeError as-is (our custom errors)
        raise
    except Exception as e:
        # Check if it's a database lock error (Chrome is open)
        error_str = str(e).lower()
        if "locked" in error_str or "database is locked" in error_str:
            raise RuntimeError("Chrome is open. Close Chrome and try again.")
        # Generic error
        raise RuntimeError(f"Failed to get cookies from Chrome: {e}")
