from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("http://localhost:8080/index.html", wait_until="domcontentloaded")
    time.sleep(1)
    
    # 1. Check Email
    footer_text = page.locator(".site-footer").text_content()
    print("Email present:", "aldewanbrandedcollection@gmail.com" in footer_text)
    assert "aldewanbrandedcollection@gmail.com" in footer_text
    
    # 2. Check Social Links
    fb_link = page.locator(".footer-social a[aria-label='Facebook']").get_attribute("href")
    insta_link = page.locator(".footer-social a[aria-label='Instagram']").get_attribute("href")
    tiktok_link = page.locator(".footer-social a[aria-label='TikTok']").get_attribute("href")
    yt_link = page.locator(".footer-social a[aria-label='YouTube']").get_attribute("href")
    
    print("FB:", fb_link)
    print("Insta:", insta_link)
    print("TikTok:", tiktok_link)
    print("YouTube:", yt_link)
    
    assert fb_link == "https://www.facebook.com/profile.php?id=61592005074273"
    assert insta_link == "https://www.instagram.com/aldewanbrandedcollection1/"
    assert tiktok_link == "https://www.tiktok.com/@al.dewan.branded"
    assert yt_link == "https://www.youtube.com/channel/UCC8WRZg3dNGdAvlRoow4Szw"
    
    page.locator(".site-footer").scroll_into_view_if_needed()
    time.sleep(0.5)
    page.screenshot(path="verification_screenshots/footer_email_and_socials_verified.png")
    
    browser.close()

print("Email and all 4 social channels verified successfully!")
