"""
Playwright-based login automation for egaz.uz
Handles cookie refresh and authentication
"""
import json
from playwright.sync_api import sync_playwright
from config import LoginConfig, DevConfig
from logger import get_logger

logger = get_logger('Login')

def refresh_cookies():
    """
    Refresh authentication cookies using Playwright
    
    Returns:
        bool: True if successful, False otherwise
    
    Raises:
        ValueError: If credentials are not configured
        Exception: If login fails
    """
    # Validate credentials
    if not LoginConfig.EGov_LOGIN or not LoginConfig.EGov_PASSWORD:
        logger.error("Login credentials not configured. Check .env file.")
        raise ValueError("EGov credentials are not set. Please configure .env file.")
    
    logger.info("Starting cookie refresh process...")
    
    try:
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=DevConfig.PLAYWRIGHT_HEADLESS)
            context = browser.new_context()
            page = context.new_page()
            
            logger.debug(f"Navigating to {LoginConfig.LOGIN_URL}")
            page.goto(LoginConfig.LOGIN_URL)
            
            # Fill credentials
            logger.debug("Filling login credentials")
            page.fill('input[name="login"]', LoginConfig.EGov_LOGIN)
            page.fill('input[name="password"]', LoginConfig.EGov_PASSWORD)
            
            # Submit form
            logger.debug("Submitting login form")
            page.click('button[type="submit"]')
            
            # Wait for redirect to admin panel
            logger.debug(f"Waiting for redirect to {LoginConfig.ADMIN_URL}")
            page.wait_for_url(LoginConfig.ADMIN_URL, timeout=20000)
            
            # Get cookies
            cookies = context.cookies()
            logger.info(f"Successfully obtained {len(cookies)} cookies")
            
            # Save cookies
            with open(LoginConfig.COOKIE_FILE, "w", encoding='utf-8') as f:
                json.dump(cookies, f, indent=4, ensure_ascii=False)
            
            logger.info(f"Cookies saved to {LoginConfig.COOKIE_FILE}")
            
            browser.close()
            return True
            
    except Exception as e:
        logger.error(f"Cookie refresh failed: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    try:
        refresh_cookies()
        logger.info("✅ Cookie refresh completed successfully")
    except Exception as e:
        logger.error(f"❌ Cookie refresh failed: {e}")
