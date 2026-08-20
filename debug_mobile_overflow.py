from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 390, "height": 844})
    
    # 1. Inspect index.html
    page.goto("http://localhost:8080/index.html")
    scroll_height = page.evaluate("() => document.documentElement.scrollHeight")
    body_height = page.evaluate("() => document.body.scrollHeight")
    client_height = page.evaluate("() => document.documentElement.clientHeight")
    print(f"Index -> scrollHeight: {scroll_height}, bodyHeight: {body_height}, clientHeight: {client_height}")
    
    # Scroll to bottom
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.screenshot(path="verification_screenshots/debug_mobile_index_bottom.png")
    
    # 2. Inspect cart.html
    page.goto("http://localhost:8080/cart.html")
    scroll_height_cart = page.evaluate("() => document.documentElement.scrollHeight")
    body_height_cart = page.evaluate("() => document.body.scrollHeight")
    print(f"Cart -> scrollHeight: {scroll_height_cart}, bodyHeight: {body_height_cart}")
    
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.screenshot(path="verification_screenshots/debug_mobile_cart_bottom.png")
    
    # 3. Inspect order-tracking.html
    page.goto("http://localhost:8080/order-tracking.html")
    page.screenshot(path="verification_screenshots/debug_mobile_order_tracking.png")
    
    browser.close()
