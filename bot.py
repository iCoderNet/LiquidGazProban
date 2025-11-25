""" 
Egaz.uz Web Scraping Bot
Handles web scraping operations for egaz.uz website
"""
import requests
import json
import re
import base64
from bs4 import BeautifulSoup
from typing import Dict, Any
from login import refresh_cookies
from config import APIConfig, FilePaths, AppConstants
from logger import get_logger

logger = get_logger('EGazBot')


def to_base64(text: str) -> str:
    """Convert text to base64 encoding"""
    return base64.b64encode(text.encode()).decode()


class EGazBot:
    """Web scraping bot for egaz.uz website"""
    
    def __init__(self):
        """Initialize bot with session and cookies"""
        self.session = requests.Session()
        self.csrf_token = None
        self.base_url = APIConfig.WEB_BASE_URL
        logger.info("Initializing EGazBot")
        self.load_cookies()
        self.update_csrf_token()

    def load_cookies(self) -> None:
        """Load authentication cookies from file"""
        try:
            with open(FilePaths.COOKIES_FILE, 'r', encoding='utf-8') as f:
                cookies = json.load(f)
            
            for c in cookies:
                self.session.cookies.set(c["name"], c["value"], domain="egaz.uz", path="/")
            
            logger.info(f"Loaded {len(cookies)} cookies successfully")
        except FileNotFoundError:
            logger.warning("Cookie file not found, refreshing cookies...")
            refresh_cookies()
            self.load_cookies()
        except Exception as e:
            logger.error(f"Error loading cookies: {e}", exc_info=True)
            refresh_cookies()
            self.load_cookies()

    def save_cookies(self) -> None:
        """Save current cookies to file"""
        try:
            cookie_list = []
            for c in self.session.cookies:
                if c.domain.endswith("egaz.uz"):
                    cookie_list.append({"name": c.name, "value": c.value})
            
            with open(FilePaths.COOKIES_FILE, "w", encoding='utf-8') as f:
                json.dump(cookie_list, f, indent=4, ensure_ascii=False)
            
            logger.debug(f"Saved {len(cookie_list)} cookies")
        except Exception as e:
            logger.error(f"Error saving cookies: {e}", exc_info=True)

    def update_csrf_token(self) -> None:
        """Update CSRF token from website"""
        try:
            logger.debug("Fetching new CSRF token")
            resp = self.session.get(f"{self.base_url}/admin/subscribers")
            
            if resp.status_code != 200:
                logger.warning("Failed to get CSRF token, refreshing cookies...")
                refresh_cookies()
                self.load_cookies()
                resp = self.session.get(f"{self.base_url}/admin/subscribers")

            soup = BeautifulSoup(resp.text, 'html.parser')
            token = soup.find("meta", {"name": "csrf-token"})
            
            if token:
                self.csrf_token = token["content"]
                logger.info("CSRF token obtained successfully")
            else:
                logger.error("CSRF token not found in page")
                raise Exception("CSRF token topilmadi!")
        except Exception as e:
            logger.error(f"Error updating CSRF token: {e}", exc_info=True)
            raise

    def get(self, url: str, allow_redirects: bool = True) -> requests.Response:
        """Make GET request with session management"""
        try:
            response = self.session.get(url, allow_redirects=allow_redirects)

            # Check for session expiration
            if response.status_code in [301, 302, 303] or "id.egov.uz" in response.url or "login" in response.url.lower():
                logger.warning("Session expired, refreshing...")
                refresh_cookies()
                self.load_cookies()
                self.update_csrf_token()
                response = self.session.get(url, allow_redirects=allow_redirects)

            return response
        except Exception as e:
            logger.error(f"GET request failed for {url}: {e}", exc_info=True)
            raise

    def post(self, url: str, data: Any = None, json: Any = None) -> requests.Response:
        """Make POST request with session management"""
        try:
            response = self.session.post(url, data=data, json=json)

            # Check for session expiration
            if response.status_code in [301, 302, 303] or "id.egov.uz" in response.url or "login" in response.url.lower():
                logger.warning("POST: Session expired, refreshing...")
                refresh_cookies()
                self.load_cookies()
                self.update_csrf_token()
                response = self.session.post(url, data=data, json=json)

            return response
        except Exception as e:
            logger.error(f"POST request failed for {url}: {e}", exc_info=True)
            raise

    def get_subscriber(self, code: str) -> Dict[str, Any]:
        """
        Get subscriber information by code
        
        Args:
            code: Subscriber code (e.g., '01000100089')
        
        Returns:
            Dictionary with subscriber information
        """
        logger.debug(f"Searching for subscriber: {code}")
        
        if not self.csrf_token:
            self.update_csrf_token()

        url = f"{self.base_url}/admin/subscribers/seek-subscriber"
        payload = {
            "_token": self.csrf_token,
            "code": str(code).strip()
        }

        resp = self.post(url, data=payload)
        
        # Save response for debugging
        try:
            with open(FilePaths.RESPONSE_FILE, "w", encoding="utf-8") as f:
                f.write(resp.text)
            logger.debug(f"Response saved to {FilePaths.RESPONSE_FILE}")
        except Exception as e:
            logger.warning(f"Could not save response: {e}")
        
        if resp.status_code != 200:
            logger.error(f"Server error: {resp.status_code}")
            return {"error": "Server xato berdi", "status_code": resp.status_code}

        html = resp.text.strip()

        # Check if not found
        if len(html) < 100 or "не найдено" in html.lower() or "topilmadi" in html.lower():
            logger.warning(f"Subscriber not found: {code}")
            return {"error": "Abonent topilmadi", "code": code}

        soup = BeautifulSoup(html, 'html.parser')

        result = {
            "code": code,
            'ID': '',
            "fio": "Topilmadi",
            "address": "",
            "organization": "",
            "phone": "",
            "contract": "",
            "status": "",
            "balance": "",
            "last_payment": "",
            "gas_cylinders": [],
            "region": AppConstants.REGION_NAME,
            'ps': "",
            'birth_date': "",
            'jshshir': ""
        }
        
        # Extract ID
        try:
            id_tag = soup.select('tr td b')[0]
            if id_tag:
                result["ID"] = id_tag.text
                logger.debug(f"Found ID: {result['ID']}")
        except (IndexError, AttributeError) as e:
            logger.warning(f"Could not extract ID: {e}")
        
        # Extract subscriber details
        try:
            ind = 0
            h1_titles = soup.find_all('td')
            
            if h1_titles:
                for h1 in h1_titles:
                    ind += 1
                    text = h1.text
                    
                    if text == 'Ф.И.О':
                        result["fio"] = h1_titles[ind].text
                    elif text == 'ОРГАНИЗАЦИЯ':
                        result["organization"] = h1_titles[ind].text
                    elif text == 'МАХАЛЛЯ: ':
                        result["address"] = h1_titles[ind].text
                    elif text == 'ТЕЛЕФОН':
                        result["phone"] = h1_titles[ind].text
                    elif text == 'КОНТРАКТ.№':
                        result["contract"] = h1_titles[ind].text
                    elif text == 'Статус':
                        result["status"] = h1_titles[ind].text.replace('\n', '').replace('  ', '')
                    elif text == 'ДЕПОЗИТ':
                        balance_text = h1_titles[ind].text.replace('\n', '').replace('  ', '')
                        result["balance"] = balance_text[1:] if balance_text else ""
                    elif "Паспорт серия" in text:
                        result['ps'] = h1_titles[ind].text
                    elif text == "Дата рождения":
                        bd_tag = h1_titles[ind].text.replace('\n', '').replace('  ', '')
                        nind = bd_tag.find(' /')
                        result['birth_date'] = bd_tag[:nind] if nind > 0 else bd_tag
                    elif "ИНН / ПИНФЛ" in text:
                        jshshir_tag = h1_titles[ind].text
                        nind = jshshir_tag.find(' /')
                        result['jshshir'] = jshshir_tag[:nind] if nind > 0 else jshshir_tag
            
            logger.info(f"Successfully parsed subscriber data for {code}")
            table = soup.find("table")
            if table:
                rows = table.find_all("tr")[1:]  # Skip header
                for row in rows:
                    cols = row.find_all("td")
                    if len(cols) >= 4:
                        result["gas_cylinders"].append({
                            "contract": cols[0].text.strip(),
                            "date": cols[1].text.strip(),
                            "own": cols[2].text.strip(),
                            "hgt": cols[3].text.strip(),
                            "status": cols[4].text.strip() if len(cols) > 4 else ""
                        })
        except Exception as e:
            logger.debug(f"Could not extract gas cylinders: {e}")

        return result
    
    def get_detail(self, encoded_id: str) -> str:
        """
        Get gas request details
        
        Args:
            encoded_id: Request ID (will be base64 encoded)
        
        Returns:
            HTML response text or None
        """
        logger.debug(f"Getting details for request ID: {encoded_id}")
        
        url = f"{self.base_url}/admin/gas_requests/detail/{to_base64(encoded_id)}"
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,uz;q=0.8",
            "Connection": "keep-alive",
            "Host": "egaz.uz",
            "Referer": f"{self.base_url}/admin/gas_requests",
            "User-Agent": "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 CrKey/1.54.250320",
            "X-CSRF-TOKEN": self.csrf_token,
            "X-Requested-With": "XMLHttpRequest",
            "Cache-Control": "no-cache, private"
        }

        try:
            response = self.session.get(url, headers=headers, timeout=10)

            # Check for session expiration
            if response.status_code in [301, 302, 303] or "login" in response.url.lower():
                logger.warning("Session expired, refreshing...")
                refresh_cookies()
                self.load_cookies()
                self.update_csrf_token()
                headers["X-CSRF-TOKEN"] = self.csrf_token
                response = self.session.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                logger.info(f"Successfully retrieved details for request {encoded_id}")
                return response.text
            else:
                logger.error(f"Error response code: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Error getting request details: {e}", exc_info=True)
            return None


if __name__ == "__main__":
    # Test bot functionality
    bot = EGazBot()
    info = bot.get_subscriber("01000099813")
    print(json.dumps(info, ensure_ascii=False, indent=2))