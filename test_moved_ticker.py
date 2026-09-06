import http.server
import socketserver
import threading
import time
import os
from playwright.sync_api import sync_playwright

PORT = 8092

os.makedirs("verification_screenshots", exist_ok=True)

Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(('', PORT), Handler)
server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
server_thread.start()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 1200})
    page.goto(f'http://localhost:{PORT}/index.html')
    time.sleep(1)

    # Check order of elements in DOM
    measurements = page.evaluate('''() => {
        const header = document.querySelector('.site-header');
        const hero = document.querySelector('.hero-banner-section');
        const ticker = document.querySelector('.announcement-bar');
        
        const headerRect = header.getBoundingClientRect();
        const heroRect = hero.getBoundingClientRect();
        const tickerRect = ticker.getBoundingClientRect();

        const isTickerInsideHero = hero.contains(ticker);

        const heroImg = hero.querySelector('img');
        const tickerComputed = window.getComputedStyle(ticker);
        return {
            headerTop: headerRect.top,
            headerBottom: headerRect.bottom,
            heroTop: heroRect.top,
            heroBottom: heroRect.bottom,
            heroImgNaturalWidth: heroImg ? heroImg.naturalWidth : 0,
            heroImgSrc: heroImg ? heroImg.src : '',
            tickerTop: tickerRect.top,
            tickerBottom: tickerRect.bottom,
            tickerHeight: tickerRect.height,
            tickerFontSize: tickerComputed.fontSize,
            tickerWidth: tickerRect.width,
            windowWidth: window.innerWidth,
            gapBetweenHeroAndTicker: tickerRect.top - heroRect.bottom,
            isTickerInsideHero: isTickerInsideHero
        };
    }''')
    print("DOM & Layout measurements:", measurements)
    
    assert measurements['headerTop'] >= 0, "Header should be at the top"
    assert measurements['heroTop'] >= measurements['headerBottom'], "Hero should be below header"
    assert measurements['heroImgNaturalWidth'] > 0, f"Hero image must be loaded, got naturalWidth={measurements['heroImgNaturalWidth']}"
    assert not measurements['isTickerInsideHero'], "Ticker must NOT be inside hero section"
    assert abs(measurements['gapBetweenHeroAndTicker']) <= 0.5, f"Gap should be 0, got {measurements['gapBetweenHeroAndTicker']}"
    assert measurements['tickerWidth'] == measurements['windowWidth'], "Ticker must span full width"
    assert measurements['tickerHeight'] == 56, f"Expected height 56px, got {measurements['tickerHeight']}"
    assert measurements['tickerFontSize'] == "17px", f"Expected font-size 17px, got {measurements['tickerFontSize']}"

    page.screenshot(path='verification_screenshots/moved_ticker_desktop.png')
    print("Desktop screenshot saved to verification_screenshots/moved_ticker_desktop.png")

    # Mobile viewport test
    page.set_viewport_size({'width': 390, 'height': 844})
    time.sleep(0.5)
    mobile_measurements = page.evaluate('''() => {
        const header = document.querySelector('.site-header');
        const hero = document.querySelector('.hero-banner-section');
        const ticker = document.querySelector('.announcement-bar');
        const headerRect = header.getBoundingClientRect();
        const heroRect = hero.getBoundingClientRect();
        const tickerRect = ticker.getBoundingClientRect();
        return {
            gap: tickerRect.top - heroRect.bottom,
            tickerWidth: tickerRect.width,
            windowWidth: window.innerWidth,
            headerBottom: headerRect.bottom,
            heroTop: heroRect.top
        };
    }''')
    print("Mobile measurements:", mobile_measurements)
    assert abs(mobile_measurements['gap']) <= 0.5, f"Mobile gap should be 0, got {mobile_measurements['gap']}"
    assert mobile_measurements['tickerWidth'] == mobile_measurements['windowWidth'], "Mobile ticker must span full width"
    page.screenshot(path='verification_screenshots/moved_ticker_mobile.png')
    print("Mobile screenshot saved to verification_screenshots/moved_ticker_mobile.png")

    browser.close()

httpd.shutdown()
print("ALL VERIFICATION TESTS PASSED PERFECTLY!")
