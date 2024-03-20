import pytest
from selenium import webdriver
GRID_HUB_URL = "http://localhost:4444/wd/hub"

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(command_executor=GRID_HUB_URL, options=options)
    yield driver
    driver.quit()

def test_google_search(driver):
    driver.get("https://www.google.com")
    assert "Google" in driver.title
