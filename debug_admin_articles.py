from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 390, "height": 844})
    
    page.goto("http://localhost:8080/admin.html")
    page.fill("#admin-passcode-input", "deewan2026")
    page.click("button[type='submit']")
    page.wait_for_timeout(500)
    
    # Switch to Products tab
    page.click(".quick-tab-pill:has-text('Articles')")
    page.wait_for_timeout(500)
    
    # Check width, overflow, and element sizes
    res = page.evaluate("""() => {
        const docWidth = document.documentElement.clientWidth;
        const scrollWidth = document.documentElement.scrollWidth;
        const tab = document.getElementById('tab-products');
        const card = tab.querySelector('.admin-card');
        const tableWrap = tab.querySelector('.admin-table-wrap');
        const table = tab.querySelector('.admin-table');
        const tableControls = tab.querySelector('.table-controls');
        
        const wideElements = [];
        document.querySelectorAll('*').forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.right > docWidth + 2) {
                wideElements.push({
                    tag: el.tagName,
                    id: el.id,
                    className: el.className,
                    right: rect.right,
                    width: rect.width
                });
            }
        });
        
        return {
            docWidth,
            scrollWidth,
            cardWidth: card ? card.getBoundingClientRect().width : null,
            tableWrapWidth: tableWrap ? tableWrap.getBoundingClientRect().width : null,
            tableWidth: table ? table.getBoundingClientRect().width : null,
            wideElements: wideElements.slice(0, 10)
        };
    }""")
    
    print("Inspection Results:", res)
    page.screenshot(path="verification_screenshots/debug_admin_articles_overflow.png", full_page=True)
    
    browser.close()
