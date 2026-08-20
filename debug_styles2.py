from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://localhost:8080/collections.html")
    page.check("input[name='category'][value='Menswear']")
    
    css_rules = page.evaluate("""() => {
        const main = document.querySelector('main.container');
        const body = document.body;
        return {
            bodyDisplay: getComputedStyle(body).display,
            bodyFlex: getComputedStyle(body).flexDirection,
            bodyAlign: getComputedStyle(body).alignItems,
            mainWidth: getComputedStyle(main).width,
            mainMargin: getComputedStyle(main).margin
        };
    }""")
    print("CSS Rules on body & main:", css_rules)
    browser.close()
