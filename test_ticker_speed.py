from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 390, "height": 844})
    page.goto("http://localhost:8080/index.html")
    
    anim_duration = page.evaluate("""() => {
        const el = document.querySelector('.announcement-bar__ticker');
        return window.getComputedStyle(el).animationDuration;
    }""")
    print("Computed animation duration on mobile:", anim_duration)
    assert anim_duration in ["55s", "55000ms"], f"Expected 55s, got {anim_duration}"
    
    browser.close()

print("Ticker speed successfully decreased for mobile!")
