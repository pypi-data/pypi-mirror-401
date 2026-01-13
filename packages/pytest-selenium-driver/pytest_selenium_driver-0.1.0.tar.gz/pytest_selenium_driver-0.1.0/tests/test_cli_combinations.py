"""Test CLI argument combinations for pytest-selenium-driver."""

import pytest
import subprocess
import sys
from pathlib import Path


class TestCLICombinations:
    """Test various CLI argument combinations."""
    
    def setup_method(self):
        """Set up test environment."""
        self.base_cmd = [sys.executable, "-m", "pytest", "--collect-only", "-q"]
        self.cwd = Path(__file__).parent.parent
    
    def run_pytest_command(self, args, expect_success=True):
        """Run pytest command with given arguments."""
        cmd = self.base_cmd + args
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,
            cwd=self.cwd
        )
        
        if expect_success:
            assert result.returncode == 0, f"Command failed: {' '.join(cmd)}\nStderr: {result.stderr}"
        else:
            assert result.returncode != 0, f"Command should have failed: {' '.join(cmd)}"
        
        return result
    
    def test_default_configuration(self):
        """Test default configuration (Chrome, GUI mode, local)."""
        result = self.run_pytest_command([])
        assert "browser=chrome" in result.stdout
        assert "headless=False" in result.stdout
        assert "remote=False" in result.stdout
    
    def test_chrome_browser(self):
        """Test Chrome browser selection."""
        result = self.run_pytest_command(["--browser=chrome"])
        assert "browser=chrome" in result.stdout
    
    def test_firefox_browser(self):
        """Test Firefox browser selection."""
        result = self.run_pytest_command(["--browser=firefox"])
        assert "browser=firefox" in result.stdout
    
    def test_headless_mode(self):
        """Test headless mode activation."""
        result = self.run_pytest_command(["--headless"])
        assert "headless=True" in result.stdout
    
    def test_chrome_headless_combination(self):
        """Test Chrome with headless mode."""
        result = self.run_pytest_command(["--browser=chrome", "--headless"])
        assert "browser=chrome" in result.stdout
        assert "headless=True" in result.stdout
    
    def test_firefox_headless_combination(self):
        """Test Firefox with headless mode."""
        result = self.run_pytest_command(["--browser=firefox", "--headless"])
        assert "browser=firefox" in result.stdout
        assert "headless=True" in result.stdout
    
    def test_remote_with_grid_url(self):
        """Test remote execution with grid URL."""
        result = self.run_pytest_command([
            "--remote", 
            "--grid-url=http://selenium-grid:4444/wd/hub"
        ])
        assert "remote=True" in result.stdout
        assert "grid-url=http://selenium-grid:4444/wd/hub" in result.stdout
    
    def test_remote_chrome_headless_combination(self):
        """Test remote Chrome with headless mode."""
        result = self.run_pytest_command([
            "--browser=chrome",
            "--headless",
            "--remote",
            "--grid-url=http://selenium-grid:4444/wd/hub"
        ])
        assert "browser=chrome" in result.stdout
        assert "headless=True" in result.stdout
        assert "remote=True" in result.stdout
    
    def test_remote_firefox_combination(self):
        """Test remote Firefox execution."""
        result = self.run_pytest_command([
            "--browser=firefox",
            "--remote",
            "--grid-url=https://selenium-hub.example.com/wd/hub"
        ])
        assert "browser=firefox" in result.stdout
        assert "remote=True" in result.stdout
        assert "grid-url=https://selenium-hub.example.com/wd/hub" in result.stdout


class TestInvalidCombinations:
    """Test invalid CLI argument combinations."""
    
    def setup_method(self):
        """Set up test environment."""
        self.base_cmd = [sys.executable, "-m", "pytest", "--collect-only", "-q"]
        self.cwd = Path(__file__).parent.parent
    
    def run_pytest_command_expect_failure(self, args):
        """Run pytest command expecting failure."""
        cmd = self.base_cmd + args
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10,
            cwd=self.cwd
        )
        
        assert result.returncode != 0, f"Command should have failed: {' '.join(cmd)}"
        return result
    
    def test_invalid_browser(self):
        """Test invalid browser name."""
        result = self.run_pytest_command_expect_failure(["--browser=safari"])
        assert "Unsupported browser 'safari'" in result.stderr
        assert "Supported browsers: chrome, firefox" in result.stderr
    
    def test_remote_without_grid_url(self):
        """Test remote flag without grid URL."""
        result = self.run_pytest_command_expect_failure(["--remote"])
        assert "Grid URL is required for remote execution" in result.stderr
    
    def test_invalid_grid_url_format(self):
        """Test invalid grid URL format."""
        result = self.run_pytest_command_expect_failure([
            "--remote", 
            "--grid-url=invalid-url-format"
        ])
        assert "Invalid grid URL" in result.stderr
    
    def test_empty_grid_url(self):
        """Test empty grid URL."""
        result = self.run_pytest_command_expect_failure([
            "--remote", 
            "--grid-url="
        ])
        # Should fail due to empty grid URL
        assert result.returncode != 0
    
    def test_malformed_browser_option(self):
        """Test malformed browser option."""
        result = self.run_pytest_command_expect_failure(["--browser="])
        # Should fail due to empty browser name
        assert result.returncode != 0


class TestPluginDiscovery:
    """Test plugin discovery and registration."""
    
    def test_help_shows_selenium_options(self):
        """Test that --help shows selenium driver options."""
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--help"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        assert result.returncode == 0
        assert "Selenium WebDriver options" in result.stdout
        assert "--browser" in result.stdout
        assert "--headless" in result.stdout
        assert "--remote" in result.stdout
        assert "--grid-url" in result.stdout
    
    def test_plugin_listed_in_version(self):
        """Test that plugin is listed in version output."""
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        assert result.returncode == 0
        # Plugin should be discoverable
        assert "selenium-driver" in result.stdout or "pytest" in result.stdout


if __name__ == "__main__":
    pytest.main([__file__, "-v"])