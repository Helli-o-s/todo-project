# conftest.py

import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="module")
def driver():
    """Fixture for Selenium WebDriver UI tests."""
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def requests_session():
    """Fixture for API tests that creates a single requests session."""
    # Using a session object is efficient as it can reuse underlying TCP connections.
    return requests.Session()