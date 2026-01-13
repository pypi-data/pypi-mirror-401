"""Parallel execution support for pytest-selenium-driver."""

import os
import threading
import logging
from typing import Dict, Any, Optional
from selenium.webdriver.remote.webdriver import WebDriver

from .config import DriverConfig
from .driver_factory import DriverFactory

logger = logging.getLogger(__name__)


class ParallelDriverManager:
    """Manager for thread-safe WebDriver creation in parallel execution scenarios.
    
    This class ensures that WebDriver instances are properly isolated between
    worker processes and threads, preventing conflicts during parallel test execution.
    """
    
    def __init__(self):
        """Initialize the parallel driver manager."""
        self._lock = threading.Lock()
        self._worker_drivers: Dict[str, WebDriver] = {}
        self._factory = DriverFactory()
    
    def get_worker_id(self) -> str:
        """Get a unique identifier for the current worker process/thread.
        
        Returns:
            Unique worker identifier combining process ID and thread ID
        """
        process_id = os.getpid()
        thread_id = threading.get_ident()
        return f"worker_{process_id}_{thread_id}"
    
    def is_parallel_execution(self) -> bool:
        """Detect if running in parallel execution mode.
        
        Returns:
            True if pytest-xdist parallel execution is detected
        """
        # Check for pytest-xdist environment variables
        xdist_indicators = [
            "PYTEST_XDIST_WORKER",
            "PYTEST_XDIST_WORKER_COUNT", 
            "PYTEST_CURRENT_TEST"
        ]
        
        # Check if any xdist environment variables are present
        has_xdist = any(os.getenv(indicator) for indicator in xdist_indicators)
        
        # Also check for multiple processes (basic heuristic)
        worker_id = self.get_worker_id()
        
        logger.debug(f"Parallel execution check: worker_id={worker_id}, xdist_detected={has_xdist}")
        
        return has_xdist
    
    def create_isolated_driver(self, config: DriverConfig, test_name: str = "") -> WebDriver:
        """Create a WebDriver instance with proper isolation for parallel execution.
        
        Args:
            config: Driver configuration
            test_name: Name of the test requesting the driver
            
        Returns:
            WebDriver instance isolated for this worker
            
        Raises:
            Exception: When driver creation fails with parallel-specific guidance
        """
        worker_id = self.get_worker_id()
        
        # Thread-safe driver creation (Requirement 8.4)
        with self._lock:
            logger.info(f"Creating isolated WebDriver for worker {worker_id}, test: {test_name}")
            
            try:
                # Create driver with worker-specific configuration
                isolated_config = self._create_worker_config(config, worker_id)
                driver = self._factory.create_driver(isolated_config)
                
                # Store driver reference for cleanup tracking
                driver_key = f"{worker_id}_{test_name}_{id(driver)}"
                self._worker_drivers[driver_key] = driver
                
                logger.info(f"WebDriver created successfully for worker {worker_id}")
                return driver
                
            except Exception as e:
                # Provide parallel-specific error guidance (Requirement 8.5)
                if self.is_parallel_execution():
                    error_msg = (
                        f"pytest-selenium-driver: Failed to create WebDriver in parallel execution. "
                        f"Worker: {worker_id}, Test: {test_name}. "
                        f"Parallel execution troubleshooting:\n"
                        f"  1. Ensure sufficient system resources for multiple browsers\n"
                        f"  2. Consider using headless mode (--headless) to reduce resource usage\n"
                        f"  3. Limit parallel workers with -n option (e.g., -n 2)\n"
                        f"  4. For remote execution, ensure grid can handle concurrent sessions\n"
                        f"Original error: {str(e)}"
                    )
                else:
                    error_msg = f"pytest-selenium-driver: WebDriver creation failed - {str(e)}"
                
                logger.error(error_msg)
                raise Exception(error_msg) from e
    
    def cleanup_worker_driver(self, driver: WebDriver, worker_id: Optional[str] = None, test_name: str = "") -> None:
        """Clean up a WebDriver instance with parallel execution safety.
        
        Args:
            driver: WebDriver instance to clean up
            worker_id: Worker ID (auto-detected if not provided)
            test_name: Name of the test that used the driver
        """
        if worker_id is None:
            worker_id = self.get_worker_id()
        
        # Thread-safe cleanup (Requirement 8.3)
        with self._lock:
            try:
                logger.info(f"Cleaning up WebDriver for worker {worker_id}, test: {test_name}")
                
                # Remove from tracking
                driver_key = f"{worker_id}_{test_name}_{id(driver)}"
                if driver_key in self._worker_drivers:
                    del self._worker_drivers[driver_key]
                
                # Quit the driver
                driver.quit()
                logger.info(f"WebDriver cleanup successful for worker {worker_id}")
                
            except Exception as cleanup_error:
                logger.warning(f"Error during WebDriver cleanup for worker {worker_id}: {cleanup_error}")
    
    def _create_worker_config(self, base_config: DriverConfig, worker_id: str) -> DriverConfig:
        """Create worker-specific configuration to avoid conflicts.
        
        Args:
            base_config: Base configuration
            worker_id: Unique worker identifier
            
        Returns:
            Modified configuration for worker isolation
        """
        # Create a copy of the configuration
        worker_config = DriverConfig(
            browser=base_config.browser,
            headless=base_config.headless,
            remote=base_config.remote,
            grid_url=base_config.grid_url,
            window_width=base_config.window_width,
            window_height=base_config.window_height
        )
        
        # For local execution, we don't need to modify ports since Selenium Manager handles this
        # For remote execution, the grid handles session isolation
        
        logger.debug(f"Created worker config for {worker_id}: {worker_config}")
        return worker_config
    
    def get_active_drivers_count(self) -> int:
        """Get the number of active WebDriver instances.
        
        Returns:
            Number of currently tracked WebDriver instances
        """
        with self._lock:
            return len(self._worker_drivers)
    
    def cleanup_all_drivers(self) -> None:
        """Emergency cleanup of all tracked WebDriver instances.
        
        This method should be called during test session teardown
        to ensure no WebDriver instances are left running.
        """
        with self._lock:
            if self._worker_drivers:
                logger.warning(f"Emergency cleanup of {len(self._worker_drivers)} remaining WebDriver instances")
                
                for driver_key, driver in list(self._worker_drivers.items()):
                    try:
                        driver.quit()
                        logger.info(f"Emergency cleanup successful for {driver_key}")
                    except Exception as e:
                        logger.error(f"Emergency cleanup failed for {driver_key}: {e}")
                
                self._worker_drivers.clear()


# Global instance for the session
_parallel_manager = ParallelDriverManager()