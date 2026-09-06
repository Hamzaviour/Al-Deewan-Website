import asyncio
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        page.on("console", lambda msg: print("CONSOLE:", msg.text))
        page.on("pageerror", lambda err: print("PAGE ERROR:", err))

        await page.goto("http://localhost:8080/admin.html")
        await page.wait_for_timeout(500)
        if await page.locator("#auth-screen").is_visible():
            await page.fill("#admin-passcode-input", "deewan2026")
            await page.click("button[type='submit']")
            await page.wait_for_timeout(600)

        await page.click("button[data-tab='tickers']")
        await page.wait_for_timeout(400)

        test_announce = "⚡ Flash Summer Sale 2026 • 100% Original Designer Lawn • Instant WhatsApp Booking ⚡"
        await page.fill("#announcement-text-input", test_announce)
        
        # Click save
        await page.click("button:has-text('Save Announcement Text')")
        await page.wait_for_timeout(500)

        saved_settings = await page.evaluate("localStorage.getItem('aldeewan_site_settings')")
        print("Saved in Admin localStorage:", saved_settings)

        # Now go to index.html
        await page.goto("http://localhost:8080/index.html")
        await page.wait_for_timeout(800)

        index_settings = await page.evaluate("localStorage.getItem('aldeewan_site_settings')")
        print("Loaded on Index localStorage:", index_settings)

        ticker_html = await page.locator(".announcement-bar__ticker").inner_html()
        print("Ticker HTML on index.html:")
        print(ticker_html)

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
