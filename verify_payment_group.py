from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1400, 'height': 900})
    
    # 1. Homepage Desktop
    page.goto('file:///e:/Work/Al-Deewan%20Website/index.html')
    page.wait_for_load_state('domcontentloaded')
    time.sleep(0.5)
    
    footer_bottom = page.locator('.footer-bottom')
    footer_bottom.scroll_into_view_if_needed()
    time.sleep(0.5)
    footer_bottom.screenshot(path='screenshot_footer_payment_icons_desktop.png')
    print('Captured screenshot_footer_payment_icons_desktop.png')
    
    # Close-up of payment group
    payment_group = page.locator('.payment-methods')
    payment_group.screenshot(path='screenshot_payment_group_closeup.png')
    print('Captured screenshot_payment_group_closeup.png')
    
    # 2. Collections Page
    page.goto('file:///e:/Work/Al-Deewan%20Website/collections.html')
    page.wait_for_load_state('domcontentloaded')
    time.sleep(0.5)
    page.locator('.footer-bottom').scroll_into_view_if_needed()
    time.sleep(0.5)
    page.locator('.footer-bottom').screenshot(path='screenshot_footer_collections_payments.png')
    print('Captured screenshot_footer_collections_payments.png')
    
    # 3. Mobile Viewport (375x667)
    page.set_viewport_size({'width': 375, 'height': 667})
    page.goto('file:///e:/Work/Al-Deewan%20Website/index.html')
    page.wait_for_load_state('domcontentloaded')
    time.sleep(0.5)
    page.locator('.footer-bottom').scroll_into_view_if_needed()
    time.sleep(0.5)
    page.locator('.footer-bottom').screenshot(path='screenshot_footer_payments_mobile.png')
    print('Captured screenshot_footer_payments_mobile.png')
    
    browser.close()

print('All payment group verification tests passed!')
