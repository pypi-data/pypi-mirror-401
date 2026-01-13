"""Browser options builders for Chrome and Firefox WebDriver configuration."""

import os
from abc import ABC, abstractmethod
from typing import Dict, Any
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


class OptionsBuilder(ABC):
    """Abstract base class for browser options builders."""
    
    @abstractmethod
    def build_options(self, headless: bool, custom_options: Dict[str, Any]):
        """Build browser-specific options.
        
        Args:
            headless: Whether to run browser in headless mode
            custom_options: Additional custom options to apply
            
        Returns:
            Browser-specific options object
        """
        pass


class ChromeOptionsBuilder(OptionsBuilder):
    """Builder for Chrome WebDriver options with sensible defaults."""
    
    def build_options(self, headless: bool, custom_options: Dict[str, Any]) -> ChromeOptions:
        """Build Chrome options with default settings and optional customizations.
        
        Args:
            headless: Whether to run Chrome in headless mode
            custom_options: Additional Chrome-specific options
            
        Returns:
            ChromeOptions configured with defaults and customizations
        """
        options = ChromeOptions()
        
        # Apply default window size (Requirement 5.1)
        options.add_argument("--window-size=1920,1080")
        
        # Disable notifications (Requirement 5.2)
        options.add_argument("--disable-notifications")
        
        # Disable GPU acceleration for stability (Requirement 5.4)
        options.add_argument("--disable-gpu")
        
        # Apply headless mode if requested (Requirement 2.1)
        if headless:
            options.add_argument("--headless")
        
        # Apply CI-safe flags when running in CI environment (Requirement 5.3)
        if self._is_ci_environment():
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-extensions")
        
        # Apply any custom options
        for key, value in custom_options.items():
            if isinstance(value, bool) and value:
                options.add_argument(f"--{key}")
            elif value is not None:
                options.add_argument(f"--{key}={value}")
        
        return options
    
    def _is_ci_environment(self) -> bool:
        """Detect if running in a CI environment.
        
        Returns:
            True if CI environment variables are detected
        """
        ci_indicators = [
            "CI", "CONTINUOUS_INTEGRATION", "GITHUB_ACTIONS", 
            "TRAVIS", "CIRCLECI", "JENKINS_URL", "BUILDKITE"
        ]
        return any(os.getenv(indicator) for indicator in ci_indicators)


class FirefoxOptionsBuilder(OptionsBuilder):
    """Builder for Firefox WebDriver options with automation-friendly defaults."""
    
    def build_options(self, headless: bool, custom_options: Dict[str, Any]) -> FirefoxOptions:
        """Build Firefox options with default settings and optional customizations.
        
        Args:
            headless: Whether to run Firefox in headless mode
            custom_options: Additional Firefox-specific options
            
        Returns:
            FirefoxOptions configured with defaults and customizations
        """
        options = FirefoxOptions()
        
        # Apply headless mode if requested (Requirement 2.1)
        if headless:
            options.add_argument("--headless")
        
        # Set automation preferences (Requirement 5.5)
        options.set_preference("dom.webnotifications.enabled", False)  # Disable notifications
        options.set_preference("media.navigator.permission.disabled", True)  # Disable media permissions
        options.set_preference("geo.enabled", False)  # Disable geolocation
        
        # Apply window size through preferences (Requirement 5.1)
        options.set_preference("browser.window.width", 1920)
        options.set_preference("browser.window.height", 1080)
        
        # Apply any custom preferences
        for key, value in custom_options.items():
            if key.startswith("pref:"):
                pref_name = key[5:]  # Remove "pref:" prefix
                options.set_preference(pref_name, value)
            else:
                options.add_argument(f"--{key}")
        
        return options