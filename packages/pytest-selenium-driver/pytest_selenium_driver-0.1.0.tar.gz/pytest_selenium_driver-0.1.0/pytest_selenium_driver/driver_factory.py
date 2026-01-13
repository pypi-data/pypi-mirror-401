"""WebDriver factory for creating local and remote WebDriver instances."""

import logging
from typing import Dict, Any, Optional, Type, List
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebDriver
from selenium.common.exceptions import WebDriverException

from .config import DriverConfig, BrowserCapabilities
from .options import ChromeOptionsBuilder, FirefoxOptionsBuilder, OptionsBuilder

# Set up logging
logger = logging.getLogger(__name__)


class DriverFactory:
    """Factory class for creating WebDriver instances based on configuration.
    
    This factory abstracts the complexity of WebDriver creation and provides
    a consistent interface for both local and remote WebDriver instantiation.
    It implements proper browser-to-WebDriver type mapping and comprehensive
    error handling for unsupported browsers.
    """
    
    # Browser-to-WebDriver type mapping (Requirements 1.1, 1.2)
    _BROWSER_MAPPING = {
        "chrome": ChromeWebDriver,
        "firefox": FirefoxWebDriver,
    }
    
    # Browser-to-OptionsBuilder mapping
    _OPTIONS_BUILDERS = {
        "chrome": ChromeOptionsBuilder,
        "firefox": FirefoxOptionsBuilder,
    }
    
    def __init__(self):
        """Initialize the DriverFactory."""
        self._supported_browsers = list(self._BROWSER_MAPPING.keys())
    
    def get_supported_browsers(self) -> List[str]:
        """Get list of supported browsers.
        
        Returns:
            List of supported browser names
        """
        return self._supported_browsers.copy()
    
    def is_browser_supported(self, browser: str) -> bool:
        """Check if a browser is supported.
        
        Args:
            browser: Browser name to check
            
        Returns:
            True if browser is supported, False otherwise
        """
        return browser in self._BROWSER_MAPPING
    
    def get_webdriver_type(self, browser: str) -> Type[WebDriver]:
        """Get the WebDriver type for a given browser.
        
        Args:
            browser: Browser name
            
        Returns:
            WebDriver class type for the browser
            
        Raises:
            ValueError: When browser is not supported
        """
        if not self.is_browser_supported(browser):
            raise ValueError(
                f"pytest-selenium-driver: Unsupported browser '{browser}'. "
                f"Supported browsers: {', '.join(self._supported_browsers)}"
            )
        return self._BROWSER_MAPPING[browser]
    
    def create_driver(self, config: DriverConfig) -> WebDriver:
        """Create a WebDriver instance based on the provided configuration.
        
        Args:
            config: DriverConfig instance containing all necessary settings
            
        Returns:
            WebDriver instance configured according to the provided settings
            
        Raises:
            ValueError: When configuration is invalid
            Exception: When WebDriver creation fails
        """
        # Validate configuration before proceeding
        config.validate()
        
        # Log driver creation attempt
        logger.info(f"Creating WebDriver: browser={config.browser}, headless={config.headless}, remote={config.remote}")
        
        try:
            if config.remote:
                return self.create_remote_driver(config)
            else:
                return self.create_local_driver(config)
        except WebDriverException as e:
            # Handle Selenium-specific errors
            raise Exception(
                f"pytest-selenium-driver: WebDriver creation failed - {str(e)}. "
                f"Please ensure the browser is installed and accessible."
            ) from e
        except Exception as e:
            # Handle general errors
            raise Exception(
                f"pytest-selenium-driver: Failed to create WebDriver - {str(e)}"
            ) from e
    
    def create_local_driver(self, config: DriverConfig) -> WebDriver:
        """Create a local WebDriver instance.
        
        Args:
            config: DriverConfig with local execution settings
            
        Returns:
            Local WebDriver instance
            
        Raises:
            ValueError: When browser is not supported
            Exception: When WebDriver creation fails
        """
        # Validate browser support (Requirements 1.3, 1.5)
        if not self.is_browser_supported(config.browser):
            raise ValueError(
                f"pytest-selenium-driver: Unsupported browser '{config.browser}' "
                f"for local execution. Supported browsers: {', '.join(self._supported_browsers)}"
            )
        
        # Get appropriate options builder
        options_builder_class = self._OPTIONS_BUILDERS[config.browser]
        options_builder = options_builder_class()
        
        # Build browser options
        options = options_builder.build_options(config.headless, {})
        
        # Create WebDriver instance based on browser type
        try:
            if config.browser == "chrome":
                logger.debug("Creating Chrome WebDriver with options")
                return webdriver.Chrome(options=options)
            elif config.browser == "firefox":
                logger.debug("Creating Firefox WebDriver with options")
                return webdriver.Firefox(options=options)
        except WebDriverException as e:
            # Provide browser-specific error guidance
            if config.browser == "chrome":
                error_msg = (
                    f"pytest-selenium-driver: Failed to create Chrome WebDriver. "
                    f"Please ensure Chrome browser is installed. "
                    f"Selenium Manager will handle ChromeDriver automatically. "
                    f"Error: {str(e)}"
                )
            elif config.browser == "firefox":
                error_msg = (
                    f"pytest-selenium-driver: Failed to create Firefox WebDriver. "
                    f"Please ensure Firefox browser is installed. "
                    f"Selenium Manager will handle GeckoDriver automatically. "
                    f"Error: {str(e)}"
                )
            else:
                error_msg = f"pytest-selenium-driver: WebDriver creation failed - {str(e)}"
            
            raise Exception(error_msg) from e
    
    def create_remote_driver(self, config: DriverConfig) -> WebDriver:
        """Create a remote WebDriver instance for Selenium Grid execution.
        
        Args:
            config: DriverConfig with remote execution settings
            
        Returns:
            Remote WebDriver instance
            
        Raises:
            ValueError: When grid URL is invalid or browser not supported
            Exception: When connection to grid fails
        """
        if not config.grid_url:
            raise ValueError(
                "pytest-selenium-driver: Grid URL is required for remote execution"
            )
        
        # Validate browser support for remote execution
        if not self.is_browser_supported(config.browser):
            raise ValueError(
                f"pytest-selenium-driver: Unsupported browser '{config.browser}' "
                f"for remote execution. Supported browsers: {', '.join(self._supported_browsers)}"
            )
        
        # Create browser capabilities
        capabilities = BrowserCapabilities(
            browser_name=config.browser
        )
        capabilities.validate()
        
        # Get browser options for remote execution
        options_builder_class = self._OPTIONS_BUILDERS[config.browser]
        options_builder = options_builder_class()
        options = options_builder.build_options(config.headless, {})
        
        logger.debug(f"Creating remote WebDriver for {config.browser} at {config.grid_url}")
        
        try:
            # Create remote WebDriver with capabilities and options
            if config.browser == "chrome":
                return webdriver.Remote(
                    command_executor=config.grid_url,
                    options=options
                )
            elif config.browser == "firefox":
                return webdriver.Remote(
                    command_executor=config.grid_url,
                    options=options
                )
        except WebDriverException as e:
            # Handle connection and WebDriver-specific errors
            if "Connection refused" in str(e) or "Failed to connect" in str(e):
                raise Exception(
                    f"pytest-selenium-driver: Failed to connect to Selenium Grid at "
                    f"'{config.grid_url}'. Please verify:\n"
                    f"  1. The grid is running and accessible\n"
                    f"  2. The URL is correct (should include /wd/hub for Selenium Grid)\n"
                    f"  3. Network connectivity is available\n"
                    f"Connection error: {str(e)}"
                ) from e
            else:
                raise Exception(
                    f"pytest-selenium-driver: Remote WebDriver creation failed. "
                    f"Grid URL: {config.grid_url}, Browser: {config.browser}. "
                    f"Error: {str(e)}"
                ) from e
        except Exception as e:
            raise Exception(
                f"pytest-selenium-driver: Failed to connect to Selenium Grid at "
                f"'{config.grid_url}'. Please verify the grid is running and "
                f"accessible. Connection error: {str(e)}"
            ) from e