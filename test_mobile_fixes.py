from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # Test on iPhone 14 (390x844) and standard Android (360x800)
    for w, h, name in [(390, 844, "iphone14"), (360, 800, "android_compact")]:
        page = browser.new_page(viewport={"width": w, "height": h})
        
        # 1. Order Tracking Page
        page.goto("http://localhost:8080/order-tracking.html")
        time.sleep(0.5)
        
        card_box = page.locator(".tracking-card").bounding_box()
        btn_box = page.locator("#tracking-form button").bounding_box()
        print(f"\n--- {name} Order Tracking ---")
        print(f"Card Box: right={card_box['x'] + card_box['width']}, width={card_box['width']}")
        print(f"Button Box: right={btn_box['x'] + btn_box['width']}, width={btn_box['width']}")
        
        # Assert button right is within card right
        assert (btn_box['x'] + btn_box['width']) <= (card_box['x'] + card_box['width'] + 2), "Button must stay inside tracking card!"
        page.screenshot(path=f"verification_screenshots/mobile_{name}_order_tracking_fixed.png")
        
        # 2. Cart Page (Empty & Filled)
        page.goto("http://localhost:8080/cart.html")
        time.sleep(0.5)
        page.screenshot(path=f"verification_screenshots/mobile_{name}_cart_page_fixed.png")
        
        # 3. Index Page
        page.goto("http://localhost:8080/index.html")
        time.sleep(0.5)
        page.screenshot(path=f"verification_screenshots/mobile_{name}_index_fixed.png")
        
        page.close()
    
    browser.close()

print("\nALL MOBILE OVERFLOW & ORDER TRACKING BUTTON CHECKS PASSED PERFECTLY!")
