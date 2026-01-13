# pytest-selenium-driver

[![PyPI version](https://badge.fury.io/py/pytest-selenium-driver.svg)](https://badge.fury.io/py/pytest-selenium-driver)
[![Python versions](https://img.shields.io/pypi/pyversions/pytest-selenium-driver.svg)](https://pypi.org/project/pytest-selenium-driver/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A zero-boilerplate Selenium WebDriver fixture for pytest with support for multiple browsers, headless mode, and both local and remote execution.

## ✨ Features

- 🚀 **Zero setup** - Works out of the box with Selenium Manager
- 🌐 **Multi-browser** - Chrome and Firefox support
- 👻 **Headless mode** - Perfect for CI/CD pipelines
- 🔗 **Remote execution** - Selenium Grid compatibility
- ⚡ **Parallel testing** - pytest-xdist integration
- 🧵 **Thread-safe** - Isolated WebDriver instances
- 🎯 **Type hints** - Full typing support
- 📝 **Comprehensive logging** - Debug-friendly output

## 🚀 Quick Start

### Installation

```bash
pip install pytest-selenium-driver
```

### Basic Usage

The plugin automatically registers with pytest and provides a `driver` fixture:

```python
def test_example(driver):
    driver.get("https://example.com")
    assert "Example" in driver.title

def test_form_submission(driver):
    driver.get("https://httpbin.org/forms/post")
    driver.find_element("name", "custname").send_keys("John Doe")
    driver.find_element("css selector", "input[type='submit']").click()
    assert "John Doe" in driver.page_source
```

## 🎛️ Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--browser` | Browser to use (chrome, firefox) | `chrome` |
| `--headless` | Run browser in headless mode | `False` |
| `--remote` | Use remote WebDriver execution | `False` |
| `--grid-url` | Selenium Grid URL for remote execution | `None` |

## 📚 Usage Examples

### Local Testing
```bash
# Run tests with Chrome (default)
pytest

# Run tests with Firefox
pytest --browser=firefox

# Run in headless mode (great for CI)
pytest --browser=chrome --headless
```

### Remote Testing (Selenium Grid)
```bash
# Run tests on remote Selenium Grid
pytest --remote --grid-url=http://selenium-grid:4444/wd/hub

# Remote with specific browser and headless mode
pytest --remote --grid-url=http://selenium-grid:4444/wd/hub --browser=firefox --headless
```

### Parallel Testing
```bash
# Run tests in parallel (requires pytest-xdist)
pip install pytest-xdist
pytest -n 4 --browser=chrome --headless
```

### Integration with Other Plugins
```bash
# Generate HTML reports with pytest-html
pytest --browser=firefox --html=report.html

# Run with coverage
pytest --browser=chrome --headless --cov=myapp
```

## 🔧 Advanced Configuration

### Custom Fixture Scopes

```python
# Function-scoped (default) - fresh driver for each test
def test_with_function_driver(driver):
    pass

# Class-scoped - shared driver across test class
def test_with_class_driver(class_scoped_driver):
    pass

# Session-scoped - shared driver across entire test session
def test_with_session_driver(session_scoped_driver):
    pass
```

### Extending with Custom Arguments

Create a `conftest.py` to add custom CLI arguments:

```python
def pytest_addoption(parser):
    group = parser.getgroup("selenium-driver")
    group.addoption("--timeout", type=int, default=10, 
                   help="Default timeout for WebDriver waits")

@pytest.fixture
def wait(request, driver):
    from selenium.webdriver.support.ui import WebDriverWait
    timeout = request.config.getoption("--timeout")
    return WebDriverWait(driver, timeout)
```

## 🏗️ Requirements

- Python 3.8+
- pytest 7.0+
- selenium 4.6+

**Note:** Browser drivers are automatically managed by Selenium Manager (no manual setup required!)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Shubham Singh** - [shubham.fps@gmail.com](mailto:shubham.fps@gmail.com)

## 🙏 Acknowledgments

- Built on top of the excellent [Selenium](https://selenium.dev/) project
- Inspired by the [pytest](https://pytest.org/) testing framework
- Thanks to the Python testing community
