"""Configuration data models for pytest-selenium-driver."""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class DriverConfig:
    """Configuration for WebDriver creation and management.
    
    This dataclass holds all configuration options for creating WebDriver instances,
    including browser selection, execution mode, and display settings.
    """
    browser: str = "chrome"
    headless: bool = False
    remote: bool = False
    grid_url: Optional[str] = None
    window_width: int = 1920
    window_height: int = 1080
    
    def validate(self) -> None:
        """Validate configuration consistency and raise clear error messages.
        
        Raises:
            ValueError: When configuration is invalid with descriptive error message
                       prefixed with "pytest-selenium-driver:"
        """
        # Validate browser selection (Requirements 1.3, 6.1)
        supported_browsers = ["chrome", "firefox"]
        if self.browser not in supported_browsers:
            raise ValueError(
                f"pytest-selenium-driver: Unsupported browser '{self.browser}'. "
                f"Supported browsers: {', '.join(supported_browsers)}"
            )
        
        # Validate remote configuration (Requirements 6.2)
        if self.remote and not self.grid_url:
            raise ValueError(
                "pytest-selenium-driver: Grid URL is required for remote execution. "
                "Please provide --grid-url when using --remote flag."
            )
        
        # Validate grid URL format when provided
        if self.grid_url and not self.grid_url.startswith(('http://', 'https://')):
            raise ValueError(
                f"pytest-selenium-driver: Invalid grid URL '{self.grid_url}'. "
                "Grid URL must start with 'http://' or 'https://'"
            )
        
        # Validate window dimensions
        if self.window_width <= 0 or self.window_height <= 0:
            raise ValueError(
                "pytest-selenium-driver: Window dimensions must be positive integers. "
                f"Got width={self.window_width}, height={self.window_height}"
            )


@dataclass
class BrowserCapabilities:
    """Browser-specific capabilities and settings for WebDriver creation.
    
    This dataclass encapsulates browser-specific configuration options
    that are passed to WebDriver instances during creation.
    """
    browser_name: str
    browser_version: Optional[str] = None
    platform_name: Optional[str] = None
    additional_options: Dict[str, Any] = field(default_factory=dict)
    
    def validate(self) -> None:
        """Validate browser capabilities configuration.
        
        Raises:
            ValueError: When capabilities configuration is invalid
        """
        if not self.browser_name:
            raise ValueError(
                "pytest-selenium-driver: Browser name cannot be empty"
            )
        
        # Validate browser name matches supported browsers
        supported_browsers = ["chrome", "firefox"]
        if self.browser_name not in supported_browsers:
            raise ValueError(
                f"pytest-selenium-driver: Unsupported browser name '{self.browser_name}'. "
                f"Supported browsers: {', '.join(supported_browsers)}"
            )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert capabilities to dictionary format for Selenium.
        
        Returns:
            Dict containing browser capabilities in Selenium-compatible format
        """
        caps = {
            "browserName": self.browser_name,
        }
        
        if self.browser_version:
            caps["browserVersion"] = self.browser_version
            
        if self.platform_name:
            caps["platformName"] = self.platform_name
            
        # Merge additional options
        caps.update(self.additional_options)
        
        return caps