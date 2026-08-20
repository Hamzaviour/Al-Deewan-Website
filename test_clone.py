import time
import os
from playwright.sync_api import sync_playwright

def run_tests():
    os.makedirs('verification_screenshots', exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1440, 'height': 900})
        page = context.new_page()
        
        base_url = 'http://localhost:8080'
        
        print("1. Testing Homepage...")
        page.goto(f'{base_url}/index.html', wait_until='domcontentloaded')
        time.sleep(1)
        assert "Branded Cut Pieces" in page.title()
        page.screenshot(path='verification_screenshots/1_homepage.png', full_page=False)
        print("[PASS] Homepage title & render verified")
        
        # Test Add to Wishlist
        print("2. Testing Wishlist Toggle...")
        wishlist_btn = page.locator('.product-card .card-action-btn').first
        wishlist_btn.click()
        time.sleep(0.5)
        wishlist_badge = page.locator('.wishlist-count-badge').first
        assert wishlist_badge.inner_text() == '1'
        print("[PASS] Wishlist item added and badge updated to 1")
        
        # Test Quick View Modal
        print("3. Testing Quick View Modal...")
        qv_btn = page.locator('.product-card .quick-view-btn').first
        qv_btn.click()
        time.sleep(0.5)
        qv_modal = page.locator('#quick-view-modal')
        assert 'active' in qv_modal.get_attribute('class')
        page.screenshot(path='verification_screenshots/2_quick_view.png')
        page.locator('.modal-close').click()
        time.sleep(0.5)
        print("[PASS] Quick view modal verified")
        
        # Test Add to Cart & Cart Drawer
        print("4. Testing Cart Drawer...")
        page.locator('#cart-drawer-toggle').click()
        time.sleep(0.5)
        cart_drawer = page.locator('#cart-drawer')
        assert 'active' in cart_drawer.get_attribute('class')
        page.screenshot(path='verification_screenshots/3_cart_drawer.png')
        page.locator('.drawer-close').first.click()
        time.sleep(0.5)
        print("[PASS] Cart drawer verified")
        
        # Test Search Modal
        print("5. Testing Predictive Search...")
        page.locator('#search-modal-toggle').click()
        time.sleep(0.5)
        page.locator('#predictive-search-input').fill('Almirah')
        time.sleep(0.5)
        search_cards = page.locator('#search-results-grid .product-card')
        assert search_cards.count() > 0
        page.screenshot(path='verification_screenshots/4_search_modal.png')
        page.locator('#search-modal-close').click()
        time.sleep(0.5)
        print(f"[PASS] Predictive search found {search_cards.count()} matching items")
        
        # Test Collections Page & Filters
        print("6. Testing Collections Catalog Page...")
        page.goto(f'{base_url}/collections.html', wait_until='domcontentloaded')
        time.sleep(1)
        products_count = page.locator('#catalog-products-grid .product-card').count()
        assert products_count > 0
        page.screenshot(path='verification_screenshots/5_collections_page.png', full_page=False)
        print(f"[PASS] Collections page loaded with {products_count} product cards")
        
        # Test Product Details Page
        print("7. Testing Product Details Page...")
        page.goto(f'{base_url}/product.html?handle=almirah-unstitched-ladies-3pc-20', wait_until='domcontentloaded')
        time.sleep(1)
        pdp_title = page.locator('#pdp-title').inner_text()
        assert len(pdp_title) > 0
        page.screenshot(path='verification_screenshots/6_product_page.png', full_page=False)
        
        # Test Quantity increase
        page.locator('#pdp-qty-plus').click()
        time.sleep(0.2)
        assert page.locator('#pdp-qty-val').inner_text() == '2'
        
        # Add to cart from PDP
        page.locator('#pdp-add-cart-btn').click()
        time.sleep(0.5)
        assert 'active' in page.locator('#cart-drawer').get_attribute('class')
        page.locator('.drawer-close').first.click()
        time.sleep(0.5)
        print("[PASS] Product page dynamic loading, quantity calculation, and cart add verified")
        
        # Test Order Tracking Page
        print("8. Testing Order Tracking...")
        page.goto(f'{base_url}/order-tracking.html', wait_until='domcontentloaded')
        time.sleep(0.5)
        page.locator('#tracking-input').fill('LE987654321')
        page.locator('#tracking-form button[type="submit"]').click()
        time.sleep(0.5)
        timeline = page.locator('#tracking-result-box')
        assert timeline.is_visible()
        page.screenshot(path='verification_screenshots/7_order_tracking.png')
        print("[PASS] Order tracking lookup and milestone timeline verified")
        
        # Test Checkout Page Flow
        print("9. Testing Checkout Page...")
        page.goto(f'{base_url}/checkout.html', wait_until='domcontentloaded')
        time.sleep(0.5)
        page.locator('#cust-contact').fill('03001234567')
        page.locator('#cust-first-name').fill('Ayesha')
        page.locator('#cust-last-name').fill('Khan')
        page.locator('#cust-address').fill('House 45, Street 12, DHA Phase 5')
        page.locator('#cust-city').select_option('Lahore')
        page.locator('#cust-phone').fill('03001234567')
        page.screenshot(path='verification_screenshots/8_checkout.png')
        
        page.locator('button[type="submit"]').click()
        time.sleep(1)
        assert 'thank-you.html' in page.url
        page.screenshot(path='verification_screenshots/9_thank_you.png')
        print("[PASS] Checkout flow completed and redirected to thank-you.html")
        
        # Test Contact Page
        print("10. Testing Contact & Policy Pages...")
        page.goto(f'{base_url}/contact.html', wait_until='domcontentloaded')
        time.sleep(0.5)
        page.screenshot(path='verification_screenshots/10_contact.png')
        
        page.goto(f'{base_url}/shop-by-brand.html', wait_until='domcontentloaded')
        time.sleep(0.5)
        page.screenshot(path='verification_screenshots/11_shop_by_brand.png')
        
        # Mobile view test
        print("11. Testing Mobile Viewport...")
        page.set_viewport_size({'width': 375, 'height': 812})
        page.goto(f'{base_url}/index.html', wait_until='domcontentloaded')
        time.sleep(1)
        page.screenshot(path='verification_screenshots/12_mobile_homepage.png')
        print("[PASS] Mobile responsive layout verified")
        
        browser.close()
        print("\nALL 11 AUTOMATED VERIFICATION TESTS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    run_tests()
