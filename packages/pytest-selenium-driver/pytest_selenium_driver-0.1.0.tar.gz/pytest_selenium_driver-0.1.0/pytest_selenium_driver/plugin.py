"""pytest plugin entry point for selenium-driver fixture."""

import logging
import sys
from typing import Generator
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from .config import DriverConfig
from .driver_factory import DriverFactory
from .parallel import _parallel_manager

# Set up logging for debugging
logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    """Add command-line options for the selenium-driver plugin.
    
    This hook registers all CLI arguments that the plugin supports,
    providing users with control over WebDriver configuration.
    
    Args:
        parser: pytest argument parser
    """
    group = parser.getgroup("selenium-driver", "Selenium WebDriver options")
    
    group.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to use for testing (chrome, firefox). Default: chrome"
    )
    
    group.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode"
    )
    
    group.addoption(
        "--remote",
        action="store_true", 
        default=False,
        help="Use remote WebDriver (requires --grid-url)"
    )
    
    group.addoption(
        "--grid-url",
        action="store",
        default=None,
        help="Selenium Grid URL for remote execution (e.g., http://selenium-grid:4444/wd/hub)"
    )


def pytest_configure(config):
    """Validate plugin configuration during pytest startup.
    
    This hook runs early in pytest initialization to validate
    configuration and fail fast if there are issues.
    
    Args:
        config: pytest configuration object
        
    Raises:
        pytest.UsageError: When configuration is invalid
    """
    # Extract configuration values
    browser = config.getoption("--browser")
    remote = config.getoption("--remote")
    grid_url = config.getoption("--grid-url")
    headless = config.getoption("--headless")
    
    # Create and validate configuration
    driver_config = DriverConfig(
        browser=browser,
        headless=headless,
        remote=remote,
        grid_url=grid_url
    )
    
    try:
        driver_config.validate()
        
        # Additional validation for factory support
        factory = DriverFactory()
        if not factory.is_browser_supported(browser):
            supported = ", ".join(factory.get_supported_browsers())
            raise ValueError(
                f"pytest-selenium-driver: Unsupported browser '{browser}'. "
                f"Supported browsers: {supported}"
            )
            
    except ValueError as e:
        # Use pytest.UsageError for better CLI error reporting
        raise pytest.UsageError(str(e))
    
    # Check for parallel execution and log accordingly
    is_parallel = _parallel_manager.is_parallel_execution()
    worker_id = _parallel_manager.get_worker_id()
    
    # Log configuration for debugging (Requirements 4.1, 2.4)
    logger.info(f"pytest-selenium-driver configured: browser={browser}, headless={headless}, remote={remote}")
    logger.info(f"Worker ID: {worker_id}, Parallel execution: {is_parallel}")
    
    if remote and grid_url:
        logger.info(f"Remote execution enabled with grid URL: {grid_url}")
    else:
        logger.info("Local WebDriver execution enabled")
    
    if is_parallel:
        logger.info("Parallel execution detected - using thread-safe WebDriver creation")
    
    # Store configuration in pytest config for access by fixtures
    config._selenium_driver_config = driver_config


def pytest_sessionfinish(session, exitstatus):
    """Clean up any remaining WebDriver instances at session end.
    
    This hook ensures that no WebDriver instances are left running
    after the test session completes, especially important for parallel execution.
    
    Args:
        session: pytest session object
        exitstatus: exit status of the test session
    """
    logger.info("Performing final WebDriver cleanup")
    _parallel_manager.cleanup_all_drivers()
    logger.info("Session cleanup completed")


def pytest_report_header(config):
    """Add selenium-driver configuration to pytest report header.
    
    Args:
        config: pytest configuration object
        
    Returns:
        List of header lines to display
    """
    if hasattr(config, '_selenium_driver_config'):
        driver_config = config._selenium_driver_config
        is_parallel = _parallel_manager.is_parallel_execution()
        worker_id = _parallel_manager.get_worker_id()
        
        lines = [
            f"selenium-driver: browser={driver_config.browser}, "
            f"headless={driver_config.headless}, remote={driver_config.remote}"
        ]
        if driver_config.remote and driver_config.grid_url:
            lines.append(f"selenium-driver: grid-url={driver_config.grid_url}")
        
        if is_parallel:
            lines.append(f"selenium-driver: parallel execution enabled, worker={worker_id}")
        
        return lines
    return []


@pytest.fixture(scope="function")
def driver(request) -> Generator[WebDriver, None, None]:
    """Pytest fixture providing configured WebDriver instances.
    
    This fixture creates a fresh WebDriver instance for each test function,
    automatically handling setup and cleanup. It ensures proper isolation
    between tests and comprehensive error handling, with full support for
    parallel execution via pytest-xdist.
    
    Args:
        request: pytest fixture request object
        
    Yields:
        WebDriver: Configured WebDriver instance
        
    Raises:
        Exception: When WebDriver creation fails with descriptive error message
    """
    # Get configuration from pytest config (stored during pytest_configure)
    if hasattr(request.config, '_selenium_driver_config'):
        config = request.config._selenium_driver_config
    else:
        # Fallback: extract configuration from pytest options
        config = DriverConfig(
            browser=request.config.getoption("--browser"),
            headless=request.config.getoption("--headless"),
            remote=request.config.getoption("--remote"),
            grid_url=request.config.getoption("--grid-url")
        )
    
    # Get test information
    test_name = request.node.name
    worker_id = _parallel_manager.get_worker_id()
    is_parallel = _parallel_manager.is_parallel_execution()
    
    # Log driver creation for debugging (Requirement 2.4)
    logger.info(f"Creating WebDriver for test '{test_name}' (worker: {worker_id})")
    
    if config.headless:
        logger.info(f"Creating headless {config.browser} WebDriver")
    else:
        logger.info(f"Creating {config.browser} WebDriver in GUI mode")
    
    if config.remote:
        logger.info(f"Using remote execution with grid URL: {config.grid_url}")
    else:
        logger.info("Using local WebDriver execution")
    
    if is_parallel:
        logger.info(f"Parallel execution mode - ensuring worker isolation")
    
    # Create WebDriver instance with parallel support (Requirements 8.1, 8.2, 8.4)
    driver_instance = None
    
    try:
        if is_parallel:
            # Use parallel manager for thread-safe creation
            driver_instance = _parallel_manager.create_isolated_driver(config, test_name)
        else:
            # Use regular factory for single-threaded execution
            factory = DriverFactory()
            driver_instance = factory.create_driver(config)
        
        logger.info(f"WebDriver created successfully for test '{test_name}' (worker: {worker_id})")
        
        # Yield the driver instance to the test (Requirements 4.1, 4.3)
        yield driver_instance
        
    except Exception as e:
        # Provide informative error message (Requirement 4.4, 6.4)
        error_msg = (
            f"pytest-selenium-driver: Failed to create WebDriver instance for test '{test_name}'. "
            f"Worker: {worker_id}, Configuration: browser={config.browser}, headless={config.headless}, "
            f"remote={config.remote}, parallel={is_parallel}. Error: {str(e)}"
        )
        logger.error(error_msg)
        raise Exception(error_msg) from e
        
    finally:
        # Automatic cleanup with parallel support (Requirement 4.2, 8.3)
        if driver_instance:
            try:
                logger.info(f"Cleaning up WebDriver for test '{test_name}' (worker: {worker_id})")
                
                if is_parallel:
                    # Use parallel manager for thread-safe cleanup
                    _parallel_manager.cleanup_worker_driver(driver_instance, worker_id, test_name)
                else:
                    # Regular cleanup for single-threaded execution
                    driver_instance.quit()
                
                logger.info(f"WebDriver cleaned up successfully for test '{test_name}' (worker: {worker_id})")
            except Exception as cleanup_error:
                logger.warning(f"Error during WebDriver cleanup for test '{test_name}' (worker: {worker_id}): {cleanup_error}")


# Alternative fixture scopes for different use cases
@pytest.fixture(scope="class")
def class_scoped_driver(request) -> Generator[WebDriver, None, None]:
    """Class-scoped WebDriver fixture for sharing driver across test methods.
    
    Use this fixture when you want to share a WebDriver instance across
    all test methods in a test class for performance optimization.
    
    Warning: Shared drivers may have state pollution between tests.
    """
    # Reuse the same logic as function-scoped driver
    yield from driver(request)


@pytest.fixture(scope="session") 
def session_scoped_driver(request) -> Generator[WebDriver, None, None]:
    """Session-scoped WebDriver fixture for sharing driver across entire test session.
    
    Use this fixture when you want to share a WebDriver instance across
    all tests in the session for maximum performance optimization.
    
    Warning: Shared drivers will have significant state pollution between tests.
    """
    # Reuse the same logic as function-scoped driver
    yield from driver(request)