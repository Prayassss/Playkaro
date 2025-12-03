# test_video_cards_load_and_navigate.py
import os
import glob
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

def find_latest_test_html(folder="test_output", pattern="test_click_first_video_card_navigates*.html"):
    path = os.path.join(os.getcwd(), folder)
    files = glob.glob(os.path.join(path, pattern))
    if not files:
        # try any test_*.html
        files = glob.glob(os.path.join(path, "test_*.html"))
    if not files:
        return None
    return max(files, key=os.path.getmtime)

if __name__ == "__main__":
    html = find_latest_test_html()
    if not html:
        print("ERROR: local HTML not found in test_output. Make sure pytest saved the artifact HTML there.")
        raise SystemExit(1)

    file_url = "file:///" + os.path.abspath(html).replace("\\", "/")
    print("Opening local file:", file_url)

    chrome_options = Options()
    # remove headless if you want to see the browser while debugging
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        driver.get(file_url)
        time.sleep(1)  # allow some JS render
        # basic check: is spinner present
        spinners = driver.find_elements("css selector", ".animate-spin, .sonner-loading-wrapper, .loading")
        if spinners:
            print("Spinner found, content likely loading.")
        cards = driver.find_elements("css selector", ".video-card, [data-video-card], .card, .media-card")
        print(f"Found {len(cards)} video card(s)")
    finally:
        driver.quit()
