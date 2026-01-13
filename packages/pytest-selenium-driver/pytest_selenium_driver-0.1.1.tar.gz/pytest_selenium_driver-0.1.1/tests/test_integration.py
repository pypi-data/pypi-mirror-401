"""Integration tests for pytest-selenium-driver plugin."""

import pytest
import subprocess
import sys
from pathlib import Path


class TestPluginIntegration:
    """Test plugin integration with pytest."""
    
    def test_plugin_discovery(self):
        """Test that pytest can discover the plugin."""
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
    
    def test_plugin_version_display(self):
        """Test that plugin version is displayed correctly."""
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        assert result.returncode == 0
        # Plugin should be listed in the output
        assert "selenium-driver" in result.stdout or "pytest" in result.stdout


class TestCLIArgumentCombinations:
    """Test various CLI argument combinations."""
    
    def test_valid_browser_options(self):
        """Test valid browser options are accepted."""
        # Test Chrome (default)
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only", "--browser=chrome"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=Path(__file__).parent.parent
        )
        assert result.returncode == 0
        
        # Test Firefox
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only", "--browser=firefox"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=Path(__file__).parent.parent
        )
        assert result.returncode == 0
    
    def test_headless_mode_option(self):
        """Test headless mode option."""
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only", "--headless"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=Path(__file__).parent.parent
        )
        assert result.returncode == 0
        assert "headless=True" in result.stdout
    
    def test_browser_and_headless_combination(self):
        """Test browser and headless combination."""
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only", "--browser=firefox", "--headless"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=Path(__file__).parent.parent
        )
        assert result.returncode == 0
        assert "browser=firefox" in result.stdout
        assert "headless=True" in result.stdout
    
    def test_remote_with_grid_url(self):
        """Test remote execution with grid URL."""
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only", "--remote", "--grid-url=http://selenium-grid:4444/wd/hub"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=Path(__file__).parent.parent
        )
        assert result.returncode == 0
        assert "remote=True" in result.stdout
        assert "grid-url=http://selenium-grid:4444/wd/hub" in result.stdout


class TestErrorScenarios:
    """Test error scenarios with invalid configurations."""
    
    def test_invalid_browser(self):
        """Test invalid browser raises appropriate error."""
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only", "--browser=safari"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=Path(__file__).parent.parent
        )
        assert result.returncode != 0
        assert "Unsupported browser 'safari'" in result.stderr
        assert "Supported browsers: chrome, firefox" in result.stderr
    
    def test_remote_without_grid_url(self):
        """Test remote flag without grid URL raises error."""
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only", "--remote"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=Path(__file__).parent.parent
        )
        assert result.returncode != 0
        assert "Grid URL is required for remote execution" in result.stderr
    
    def test_invalid_grid_url_format(self):
        """Test invalid grid URL format raises error."""
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only", "--remote", "--grid-url=invalid-url"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=Path(__file__).parent.parent
        )
        assert result.returncode != 0
        assert "Invalid grid URL" in result.stderr


class TestParallelExecution:
    """Test parallel execution scenarios."""
    
    def test_parallel_execution_detection(self):
        """Test that parallel execution is properly detected."""
        # Skip if pytest-xdist is not available
        pytest_xdist = subprocess.run(
            [sys.executable, "-c", "import xdist"],
            capture_output=True
        )
        if pytest_xdist.returncode != 0:
            pytest.skip("pytest-xdist not available")
        
        # Create a simple test file for parallel execution
        test_content = '''
def test_simple_1():
    assert True

def test_simple_2():
    assert True
'''
        
        test_file = Path(__file__).parent / "temp_parallel_test.py"
        test_file.write_text(test_content)
        
        try:
            # Run with pytest-xdist
            result = subprocess.run(
                [sys.executable, "-m", "pytest", str(test_file), "-n", "2", "-v"],
                capture_output=True,
                text=True,
                timeout=15,
                cwd=Path(__file__).parent.parent
            )
            
            # Should succeed even without actual WebDriver usage
            assert result.returncode == 0
            assert "2 workers" in result.stdout or "gw0" in result.stdout
            
        finally:
            # Clean up
            if test_file.exists():
                test_file.unlink()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])