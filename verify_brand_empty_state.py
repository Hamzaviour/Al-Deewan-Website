import os
from playwright.sync_api import sync_playwright

def verify():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        print("\n--- TEST 1: Direct navigation to collections.html?brand=Kayseria ---", flush=True)
        page.goto("http://localhost:8080/collections.html?brand=Kayseria", wait_until="networkidle")
        
        # Check title and count
        title = page.locator("#catalog-title").inner_text()
        count = page.locator("#catalog-count-desc").inner_text()
        status = page.locator("#pagination-status").inner_text()
        cards_count = page.locator("#catalog-products-grid .product-card").count()
        empty_state = page.locator(".no-products-found").is_visible()
        empty_heading = page.locator(".no-products-found h3").inner_text() if empty_state else ""
        
        print(f"Title: {title}", flush=True)
        print(f"Count: {count}", flush=True)
        print(f"Status: {status}", flush=True)
        print(f"Product cards count: {cards_count}", flush=True)
        print(f"Empty state visible: {empty_state}", flush=True)
        print(f"Empty state heading: {empty_heading}", flush=True)
        
        page.screenshot(path="brand_kayseria_empty_state.png", full_page=True)
        assert cards_count == 0, f"Expected 0 cards, got {cards_count}"
        assert empty_state, "Expected empty state to be visible"
        assert "KAYSERIA" in empty_heading.upper(), f"Expected Kayseria in heading, got {empty_heading}"
        assert "Found 0 products in Kayseria" in count, f"Expected 'Found 0 products in Kayseria', got {count}"
        print(">>> TEST 1 PASSED: Kayseria correctly shows 0 products & empty state!")

        print("\n--- TEST 2: Reset All Filters button from Empty State ---")
        reset_btn = page.locator(".no-products-found button:has-text('VIEW ALL PRODUCTS')")
        assert reset_btn.is_visible(), "Expected VIEW ALL PRODUCTS button"
        reset_btn.click()
        page.wait_for_timeout(500)
        
        cards_after_reset = page.locator("#catalog-products-grid .product-card").count()
        count_after_reset = page.locator("#catalog-count-desc").inner_text()
        print(f"Cards after reset: {cards_after_reset}")
        print(f"Count after reset: {count_after_reset}")
        assert cards_after_reset > 0, "Expected products to show after reset"
        print(">>> TEST 2 PASSED: Reset All Filters button works smoothly!")

        print("\n--- TEST 3: Direct navigation to collections.html?brand=Nishat+Linen ---")
        page.goto("http://localhost:8080/collections.html?brand=Nishat+Linen", wait_until="networkidle")
        nishat_count = page.locator("#catalog-count-desc").inner_text()
        nishat_cards = page.locator("#catalog-products-grid .product-card").count()
        print(f"Nishat Linen Count: {nishat_count}")
        print(f"Nishat Linen Cards: {nishat_cards}")
        assert nishat_cards > 0, "Expected Nishat Linen cards to be visible"
        print(">>> TEST 3 PASSED: Nishat Linen correctly shows products!")

        print("\n--- TEST 4: shop-by-brand.html click on Kayseria ---")
        page.goto("http://localhost:8080/shop-by-brand.html", wait_until="networkidle")
        page.screenshot(path="shop_by_brand_page.png")
        
        # Click on Kayseria in featured grid
        page.locator(".featured-brands-grid a:has-text('Kayseria')").click()
        page.wait_for_load_state("networkidle")
        
        brand_page_url = page.url
        brand_title = page.locator("#catalog-title").inner_text()
        brand_count = page.locator("#catalog-count-desc").inner_text()
        brand_cards = page.locator("#catalog-products-grid .product-card").count()
        brand_empty = page.locator(".no-products-found").is_visible()
        
        print(f"Navigated URL: {brand_page_url}", flush=True)
        print(f"Title: {brand_title}", flush=True)
        print(f"Count: {brand_count}", flush=True)
        print(f"Cards: {brand_cards}", flush=True)
        print(f"Empty state visible: {brand_empty}", flush=True)
        
        assert brand_cards == 0, f"Expected 0 cards, got {brand_cards}"
        assert brand_empty, "Expected empty state"
        print(">>> TEST 4 PASSED: Clicking Kayseria from shop-by-brand shows 0 products & empty state!", flush=True)

        print("\n--- TEST 5: Homepage Brand Ticker click on Agha Noor ---", flush=True)
        page.goto("http://localhost:8080/index.html", wait_until="networkidle")
        
        # Click on Agha Noor in ticker via evaluate (handles continuous horizontal marquee animation)
        agha_link = page.locator(".brands-ticker a[title='Agha Noor']").first
        agha_link.evaluate("el => el.click()")
        page.wait_for_load_state("networkidle")
        
        ticker_url = page.url
        ticker_title = page.locator("#catalog-title").inner_text()
        ticker_count = page.locator("#catalog-count-desc").inner_text()
        ticker_cards = page.locator("#catalog-products-grid .product-card").count()
        ticker_empty = page.locator(".no-products-found").is_visible()
        
        print(f"Navigated URL: {ticker_url}", flush=True)
        print(f"Title: {ticker_title}", flush=True)
        print(f"Count: {ticker_count}", flush=True)
        print(f"Cards: {ticker_cards}", flush=True)
        print(f"Empty state: {ticker_empty}", flush=True)
        
        page.screenshot(path="agha_noor_ticker_empty_state.png")
        assert ticker_cards == 0, f"Expected 0 cards, got {ticker_cards}"
        assert ticker_empty, "Expected empty state"
        print(">>> TEST 5 PASSED: Clicking Agha Noor from homepage ticker shows 0 products & empty state!", flush=True)

        print("\n--- TEST 6: Homepage Brand Ticker click on Sapphire (has products) ---", flush=True)
        page.goto("http://localhost:8080/index.html", wait_until="networkidle")
        
        sapphire_link = page.locator(".brands-ticker a[title='Sapphire']").first
        sapphire_link.evaluate("el => el.click()")
        page.wait_for_load_state("networkidle")
        
        sapphire_cards = page.locator("#catalog-products-grid .product-card").count()
        sapphire_count = page.locator("#catalog-count-desc").inner_text()
        print(f"Sapphire Count: {sapphire_count}", flush=True)
        print(f"Sapphire Cards: {sapphire_cards}", flush=True)
        assert sapphire_cards > 0, "Expected Sapphire cards to be visible"
        print(">>> TEST 6 PASSED: Clicking Sapphire from homepage ticker shows products!", flush=True)

        browser.close()
        print("\nALL 6 TESTS PASSED PERFECTLY!", flush=True)

if __name__ == "__main__":
    verify()
