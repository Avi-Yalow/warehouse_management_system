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


@pytest.fixture(scope="session", autouse=True)
def setup_teardown():
    print("\nSetting up resources...")
    yield
    print("\nTearing down resources...")