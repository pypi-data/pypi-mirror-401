"""pytest-selenium-driver: A zero-boilerplate Selenium WebDriver fixture for pytest."""

__version__ = "0.1.0"
__author__ = "Shubham Singh"

# Export main components for easy importing
from .config import DriverConfig, BrowserCapabilities
from .driver_factory import DriverFactory
from .parallel import ParallelDriverManager

__all__ = [
    "DriverConfig",
    "BrowserCapabilities", 
    "DriverFactory",
    "ParallelDriverManager",
]