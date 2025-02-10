import pytest
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    report_dir= "tests/reports"
    now= datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    config.option.htmlpath=f"{report_dir}/report_{now}.html"

@pytest.fixture
def base_url():
    """Fixture to provide the base URL for the API"""
    return os.getenv("BASE_URL","http://localhost:5000")

@pytest.fixture
def headers():
    """Fixture to provide common headers"""
    return {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
@pytest.fixture
def api_client(headers):
    """Fixture to provide a requests session"""
    session = requests.Session()
    session.headers.update(headers)
    yield session
    session.close()

@pytest.fixture(scope="session", autouse=True)
def setup_teardown():
    print("\nSetting up resources...")
    yield
    print("\nTearing down resources...")