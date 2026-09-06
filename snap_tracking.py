import asyncio
from playwright.async_api import async_playwright

async def test_tracking():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        # desktop
        page = await b.new_page(viewport={'width': 1280, 'height': 900})
        await page.goto('http://localhost:8080/order-tracking.html')
        await page.wait_for_timeout(600)
        await page.screenshot(path='tracking_desktop_adjusted.png', full_page=True)
        
        # Test interactive tracking lookup
        await page.fill('#tracking-input', 'MNP-98421098')
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(600)
        await page.screenshot(path='tracking_desktop_lookup_result.png', full_page=True)
        
        # mobile
        mob_page = await b.new_page(viewport={'width': 375, 'height': 812})
        await mob_page.goto('http://localhost:8080/order-tracking.html')
        await mob_page.wait_for_timeout(600)
        await mob_page.screenshot(path='tracking_mobile_adjusted.png', full_page=True)
        
        await b.close()
        print('DONE')

if __name__ == '__main__':
    asyncio.run(test_tracking())
