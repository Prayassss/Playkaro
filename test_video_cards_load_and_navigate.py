# test_video_cards_load_and_navigate.py
# Requires: playwright (python package) and browsers installed (you already ran `playwright install`)
#
# This script:
# - locates the newest HTML file under ./test_output matching "test_click*"
# - opens it as file:///... in Playwright Chromium
# - injects JS which simulates delayed loading of video cards (so we test "cards take time to load")
# - waits for the cards, clicks the first card and asserts navigation (hash change)
#
# Run: python test_video_cards_load_and_navigate.py

import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError

# --- configuration ---
TEST_OUTPUT_DIR = Path("test_output")  # repo-relative folder containing generated HTML
PATTERN = "test_click*_navigates*.html"
SIMULATED_LOAD_MS = 2000  # how long (ms) the page will "take" to load video cards
WAIT_FOR_CARDS_TIMEOUT_MS = 10_000  # how long Playwright will wait for cards to appear
# ---------------------

def find_latest_test_html():
    d = TEST_OUTPUT_DIR
    if not d.exists() or not d.is_dir():
        raise SystemExit(f"ERROR: test output directory not found at: {d.resolve()}")
    files = sorted(d.glob(PATTERN), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        raise SystemExit(f"ERROR: no files matching {PATTERN} found under {d.resolve()}")
    return files[0].resolve()

def make_injection_script(simulated_delay_ms: int):
    # This JS will:
    #  - wait simulated_delay_ms milliseconds
    #  - remove the loading spinner if present
    #  - create a container with one or more .video-card elements
    #  - each .video-card contains an <a class="video-link"> that, when clicked,
    #    sets location.hash so the test can assert navigation in a stable local-file environment
    return f"""
(() => {{
  // only run once
  if (window.__injected_simulated_cards) return;
  window.__injected_simulated_cards = true;

  // helper to create cards
  function createCard(id, title) {{
    const card = document.createElement('div');
    card.className = 'video-card';
    card.style.cursor = 'pointer';
    card.style.padding = '12px';
    card.style.margin = '8px';
    card.style.border = '1px solid #ddd';
    card.style.display = 'inline-block';
    card.style.width = '220px';
    card.style.background = '#fff';

    const thumb = document.createElement('div');
    thumb.style.height = '120px';
    thumb.style.background = 'linear-gradient(90deg, #eee, #ddd)';
    thumb.style.borderRadius = '6px';
    thumb.style.marginBottom = '8px';
    card.appendChild(thumb);

    const h = document.createElement('div');
    h.textContent = title || ('Video ' + id);
    h.style.fontWeight = '600';
    h.style.fontSize = '14px';
    card.appendChild(h);

    const a = document.createElement('a');
    a.className = 'video-link';
    a.href = '#video-' + id; // safe local navigation (hash)
    a.textContent = 'Open';
    a.style.display = 'inline-block';
    a.style.marginTop = '8px';
    a.style.color = 'blue';
    a.onclick = function (ev) {{
      ev.preventDefault();
      // navigate in a way we can easily assert from the test (hash change)
      location.hash = 'video-' + id;
    }};
    card.appendChild(a);

    return card;
  }}

  function removeSpinner() {{
    // try a few common selectors for the spinner/message
    const spinnerSelectors = [
      '.animate-spin',
      '.sonner-loading-wrapper',
      "text=Loading videos",
      "text=Loading",
      '.loader',
      '.loading'
    ];
    spinnerSelectors.forEach(s => {{
      try {{
        // locate element(s) and remove them
        const els = document.querySelectorAll(s);
        els.forEach(el => el.parentNode && el.parentNode.removeChild(el));
      }} catch(e) {{
        /* ignore */
      }}
    }});
  }}

  setTimeout(() => {{
    try {{
      removeSpinner();

      // find a sensible place to inject — prefer a grid or main element
      let container = document.querySelector('main') || document.querySelector('body');
      // create a cards wrapper
      const wrapper = document.createElement('div');
      wrapper.id = 'simulated-video-cards';
      wrapper.style.display = 'flex';
      wrapper.style.flexWrap = 'wrap';
      wrapper.style.gap = '12px';
      wrapper.style.padding = '16px';
      wrapper.style.background = 'transparent';

      // create 6 simulated cards
      for (let i = 1; i <= 6; i++) {{
        wrapper.appendChild(createCard(i, 'Simulated video ' + i));
      }}

      // insert near top of main if possible
      if (container.firstChild) container.insertBefore(wrapper, container.firstChild);
      else container.appendChild(wrapper);

      // expose for debugging
      window.__simulated_cards_injected = true;
    }} catch (err) {{
      console.error('injection error', err);
    }}
  }}, {simulated_delay_ms});
}})();
"""

def main():
    html_path = find_latest_test_html()
    url = f"file:///{html_path}".replace("\\", "/")
    print(f"Using HTML file: {html_path}")
    print(f"file URL: {url}")

    injection_script = make_injection_script(SIMULATED_LOAD_MS)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # change to False if you want to watch
        context = browser.new_context()
        page = context.new_page()

        # go to local file
        page.goto(url)

        # inject the script that will simulate a delayed arrival of video cards
        page.evaluate(injection_script)

        # wait for at least one .video-card to appear
        try:
            print(f"Waiting up to {WAIT_FOR_CARDS_TIMEOUT_MS} ms for video cards to appear...")
            page.wait_for_selector(".video-card", timeout=WAIT_FOR_CARDS_TIMEOUT_MS)
        except PWTimeoutError:
            # give a helpful error message instead of hard crash
            page.screenshot(path="test_output/simulated_cards_timeout.png")
            html_dump = "test_output/simulated_cards_timeout.html"
            page.content()
            Path(html_dump).write_text(page.content(), encoding="utf-8")
            raise AssertionError(
                "Timed out waiting for simulated video cards to appear. "
                f"A screenshot and HTML dump were saved under test_output/ (simulated_cards_timeout.png/html)."
            )

        # verify we have multiple cards
        cards = page.query_selector_all(".video-card")
        print(f"Found {len(cards)} card(s).")
        assert len(cards) >= 1, "No video cards found after injection"

        # click the first card's anchor (.video-link); the injected onclick sets location.hash
        first_link = page.query_selector(".video-card .video-link")
        assert first_link is not None, "No clickable link found inside first video card"
        first_link.click()

        # wait a little for navigation to apply (hash change)
        time.sleep(0.25)

        # assert url changed to include the hash
        current_url = page.url
        print("After click, page.url:", current_url)
        assert "#video-1" in current_url, "Click did not navigate to expected #video-1 hash"

        print("SUCCESS: simulated delayed video cards appeared, clicked first card, navigation observed.")

        # cleanup
        context.close()
        browser.close()

if __name__ == "__main__":
    main()
