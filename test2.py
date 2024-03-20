import pytest
from selenium import webdriver
GRID_HUB_URL = "http://localhost:4444/wd/hub"

@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(command_executor=GRID_HUB_URL, options=options)
    request.addfinalizer(driver.quit)
    return driver

def test_example(driver):
    driver.get("https://www.example.com")
    assert "Example Domain" in driver.title
