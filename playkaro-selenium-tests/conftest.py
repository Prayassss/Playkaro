# conftest.py
import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "test_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)


@pytest.fixture
def driver(request):
    chrome_options = Options()
    # COMMENT OUT headless while debugging to watch the browser
    # chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_window_size(1400, 900)

    yield driver

    # if test failed, take a screenshot and save page source
    # pytest stores the test outcome on request.node in a report object
    # but we can inspect the last call via request.node.rep_call if hook is used.
    driver.quit()


# Hook to add a failure artifact automatically
def pytest_runtest_makereport(item, call):
    # this hook runs for setup/call/teardown; we only want call phase
    if call.when == "call":
        outcome = call.excinfo
        if outcome is not None:
            # test failed during execution
            try:
                driver = item.funcargs.get("driver")
                if driver:
                    timestamp = int(time.time())
                    safe_test_name = item.name.replace("/", "_").replace(":", "_")
                    png = os.path.join(OUTPUT_DIR, f"{safe_test_name}-{timestamp}.png")
                    html = os.path.join(OUTPUT_DIR, f"{safe_test_name}-{timestamp}.html")
                    driver.save_screenshot(png)
                    with open(html, "w", encoding="utf-8") as fh:
                        fh.write(driver.page_source)
                    print(f"\nSaved failure artifacts:\n  {png}\n  {html}\n")
            except Exception as e:
                print("Could not save screenshot/page_source:", e)
