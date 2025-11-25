import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional
import logging
import bot
import base64

# Logging sozlamalari
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class EGAZFormHandler:
    """EGAZ.uz tizimida abonent ma'lumotlarini boshqarish uchun sinf"""
    
    def __init__(self, session_cookie: str, csrf_token: str):
        """
        Args:
            session_cookie: Sessiya cookie qiymati
            csrf_token: CSRF token qiymati
        """
        self.base_url = "https://egaz.uz"
        self.session = requests.Session()
        
        # Cookie'larni o'rnatish
        self.session.cookies.set('e_gaz_billing_session', session_cookie)
        self.session.cookies.set('XSRF-TOKEN', csrf_token)
        
        # Headerlarni sozlash
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en,ru;q=0.9,uz;q=0.8',
            'X-CSRF-TOKEN': csrf_token,
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': f'{self.base_url}/admin/subscribers',
            'Origin': self.base_url
        })
    
    def get_subscriber_form(self, subscriber_id: str) -> Optional[BeautifulSoup]:
        """
        Abonent formini olish
        
        Args:
            subscriber_id: Abonent ID (base64 formatda, masalan: MTc4NzI1MQ==)
        
        Returns:
            BeautifulSoup obyekti yoki None
        """
        try:
            url = f"{self.base_url}/admin/subscribers/edit-data/{subscriber_id}"
            logger.info(f"Form olinmoqda: {url}")
            
            response = self.session.get(url)
            response.raise_for_status()
            
            logger.info("Form muvaffaqiyatli olindi")
            return BeautifulSoup(response.text, 'html.parser')
            
        except requests.RequestException as e:
            logger.error(f"Formni olishda xatolik: {e}")
            return None
    
    def modify_form_data(self, soup: BeautifulSoup) -> Dict[str, str]:
        """
        Form ma'lumotlarini o'zgartirish (is_need qiymatini o'zgartirish)
        
        Args:
            soup: BeautifulSoup obyekti
        
        Returns:
            Form ma'lumotlari dictionary
        """
        form_data = {}
        
        # Formni topish
        form = soup.find('form', {'id': 'form-subscriber'})
        if not form:
            logger.error("Form topilmadi!")
            return form_data
        
        # Barcha input elementlarini olish
        for input_elem in form.find_all(['input', 'select', 'textarea']):
            name = input_elem.get('name')
            if not name:
                continue
            
            input_type = input_elem.get('type', '').lower()
            
            # Radio buttonlar uchun
            if input_type == 'radio':
                # "is_need" ni o'zgartirish - "НЕ НУЖДАЕТСЯ" ni tanlash
                if name == 'is_need':
                    if input_elem.get('value') == '2':
                        form_data[name] = '2'
                        logger.info("is_need qiymati '2' (НЕ НУЖДАЕТСЯ) ga o'zgartirildi")
                # Boshqa radio buttonlar uchun checked atributini tekshirish
                elif input_elem.get('checked') is not None:
                    form_data[name] = input_elem.get('value', '')
            
            # Checkbox uchun
            elif input_type == 'checkbox':
                if input_elem.get('checked') is not None:
                    form_data[name] = input_elem.get('value', 'on')
            
            # Hidden, text, date, number va boshqalar uchun
            elif input_type in ['hidden', 'text', 'date', 'number', 'password', 'file']:
                value = input_elem.get('value', '')
                if value:  # Bo'sh bo'lmagan qiymatlarni qo'shish
                    form_data[name] = value
            
            # Select elementlar uchun
            elif input_elem.name == 'select':
                selected = input_elem.find('option', selected=True)
                if selected:
                    form_data[name] = selected.get('value', '')
            
            # Textarea uchun
            elif input_elem.name == 'textarea':
                form_data[name] = input_elem.get_text(strip=True)
        
        logger.info(f"Jami {len(form_data)} ta form maydoni topildi")
        return form_data
    
    def submit_form(self, form_data: Dict[str, str]) -> bool:
        """
        Formni yuborish
        
        Args:
            form_data: Form ma'lumotlari
        
        Returns:
            Muvaffaqiyatli yuborilsa True, aks holda False
        """
        try:
            url = f"{self.base_url}/admin/subscribers/update-save"
            logger.info(f"Form yuborilmoqda: {url}")
            
            response = self.session.post(url, data=form_data)
            response.raise_for_status()
            
            logger.info("Form muvaffaqiyatli yuborildi")
            logger.info(f"Response status: {response.status_code}")
            
            return True
            
        except requests.RequestException as e:
            logger.error(f"Formni yuborishda xatolik: {e}")
            return False
    
    def process_subscriber(self, subscriber_id: str) -> bool:
        """
        Abonent ma'lumotlarini to'liq qayta ishlash
        
        Args:
            subscriber_id: Abonent ID
        
        Returns:
            Muvaffaqiyatli bajarilsa True
        """
        logger.info(f"Abonent qayta ishlanmoqda: {subscriber_id}")
        
        # 1. Formni olish
        soup = self.get_subscriber_form(subscriber_id)
        if not soup:
            return False
        
        # 2. Form ma'lumotlarini o'zgartirish
        form_data = self.modify_form_data(soup)
        if not form_data:
            logger.error("Form ma'lumotlari bo'sh!")
            return False
        
        # 3. Formni yuborish
        success = self.submit_form(form_data)
        
        if success:
            logger.info(f"Abonent {subscriber_id} muvaffaqiyatli yangilandi")
        else:
            logger.error(f"Abonent {subscriber_id} yangilanmadi")
        
        return success


def main():
    """Asosiy funksiya - ishlatish namunasi"""
    
    # Cookie va CSRF token qiymatlarini kiriting
    SESSION_COOKIE = "eyJpdiI6Im43aHU5UjNwNjJnYVZEQWVpcUJQb1E9PSIsInZhbHVlIjoiZGlmalo5UFkxVEhwUUwwTFlkVzBqVlFYMjBDYU9WSldySjlQS29CSG1jUXhNbmUrd1Vhc24wc1hJTHlIRzNZWWlDSE82N2ZmRnE5ZWU2MDRxQmVVRjVCcWhkQ0hmOEV3VTZKRXFqdk9DWU9RV0xhZ1JDcHN5NkFNdERqaTNtODUiLCJtYWMiOiI1ZDRlMzY0YmJiZTIyM2RjMzQyMWNhOTViNjdlZTVkOGViODk1Nzc3MGQ3YTFlYjQ1NGM5YzQzYzlkY2Y5NGFkIn0%3D"
    CSRF_TOKEN = "XgN6R7JGKf2ZMy3QronmFb3887WOnhoDlZpR1aiI"
    
    # Handler obyektini yaratish
    handler = EGAZFormHandler(SESSION_COOKIE, CSRF_TOKEN)
    
    Ebot = bot.EGazBot()
    print(Ebot.get_subscriber("01000367953"))
    
    # Abonent ID (base64 formatda)
    # subscriber_id = base64.b64encode(b"1781729").decode('utf-8')
    
    # # Abonentni qayta ishlash
    # success = handler.process_subscriber(subscriber_id)
    
    # if success:
    #     print("✅ Abonent ma'lumotlari muvaffaqiyatli yangilandi!")
    # else:
    #     print("❌ Xatolik yuz berdi!")


if __name__ == "__main__":
    main()