from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1400, 'height': 900})
    
    page.goto('file:///e:/Work/Al-Deewan%20Website/index.html')
    page.wait_for_load_state('domcontentloaded')
    time.sleep(0.5)
    
    # Check transform at t=0
    pos1 = page.evaluate('''() => {
        const el = document.querySelector('.brands-ticker');
        const style = window.getComputedStyle(el);
        const matrix = new DOMMatrix(style.transform);
        return matrix.m41;
    }''')
    
    time.sleep(1.5)
    
    # Check transform at t=1.5s
    pos2 = page.evaluate('''() => {
        const el = document.querySelector('.brands-ticker');
        const style = window.getComputedStyle(el);
        const matrix = new DOMMatrix(style.transform);
        return matrix.m41;
    }''')
    
    print(f'Initial X position: {pos1}, Position after 1.5s: {pos2}')
    if pos2 > pos1:
        print('SUCCESS: Brand ticker is moving from LEFT to RIGHT (X position is increasing)!')
    else:
        print('FAILURE: X position did not increase')
    
    page.locator('.brands-section-wrapper').screenshot(path='screenshot_brand_ticker_left_to_right.png')
    print('Captured screenshot_brand_ticker_left_to_right.png')
    
    browser.close()
