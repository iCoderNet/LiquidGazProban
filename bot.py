# egaz_bot.py
import requests
import json
import re
from bs4 import BeautifulSoup
from login import refresh_cookies  # sizda bor

import base64


def to_base64(text: str) -> str:
    return base64.b64encode(text.encode()).decode()

EGAZ_HOME = "https://egaz.uz"

class EGazBot:
    def __init__(self):
        self.session = requests.Session()
        self.csrf_token = None
        self.load_cookies()
        self.update_csrf_token()  # dastlabki token

    def load_cookies(self):
        try:
            cookies = json.load(open("cookies.json"))
            for c in cookies:
                self.session.cookies.set(c["name"], c["value"], domain="egaz.uz", path="/")
            print("Cookie yuklandi")
        except:
            print("Cookie yo‘q → yangi cookie olinadi...")
            refresh_cookies()
            self.load_cookies()

    def save_cookies(self):
        cookie_list = []
        for c in self.session.cookies:
            if c.domain.endswith("egaz.uz"):
                cookie_list.append({"name": c.name, "value": c.value})
        json.dump(cookie_list, open("cookies.json", "w"), indent=4, ensure_ascii=False)

    def update_csrf_token(self):
        """Har safar yangi CSRF tokenni olish"""
        resp = self.session.get(f"{EGAZ_HOME}/admin/subscribers")
        if resp.status_code != 200:
            print("CSRF olishda xato, qayta login...")
            refresh_cookies()
            self.load_cookies()
            resp = self.session.get(f"{EGAZ_HOME}/admin/subscribers")

        soup = BeautifulSoup(resp.text, 'html.parser')
        token = soup.find("meta", {"name": "csrf-token"})
        if token:
            self.csrf_token = token["content"]
            print("CSRF token olindi")
            # print(f"CSRF token yangilandi: {self.csrf_token[:20]}...")
        else:
            raise Exception("CSRF token topilmadi!")
        

    def get(self, url, allow_redirects=True):
        response = self.session.get(url, allow_redirects=allow_redirects)

        # Agar login sahifasiga yo‘naltirsa → cookie eskirgan
        if response.status_code in [301, 302, 303] or "id.egov.uz" in response.url or "login" in response.url.lower():
            print("Sessiya eskirgan → qayta login qilinmoqda...")
            refresh_cookies()
            self.load_cookies()
            self.update_csrf_token()
            response = self.session.get(url, allow_redirects=allow_redirects)

        return response

    def post(self, url, data=None, json=None):
        response = self.session.post(url, data=data, json=json)

        if response.status_code in [301, 302, 303] or "id.egov.uz" in response.url or "login" in response.url.lower():
            print("POST: Sessiya eskirgan → qayta login...")
            refresh_cookies()
            self.load_cookies()
            self.update_csrf_token()
            response = self.session.post(url, data=data, json=json)

        return response

    # =============================
    # ASOSIY FUNKSIYA: ABONENT QIDIRISH
    # =============================
    def get_subscriber(self, code: str):
        """
        Abonent kod bo'yicha to'liq ma'lumot qaytaradi
        Misol: bot.get_subscriber("01000100089")
        """
        if not self.csrf_token:
            self.update_csrf_token()

        url = f"{EGAZ_HOME}/admin/subscribers/seek-subscriber"
        payload = {
            "_token": self.csrf_token,
            "code": str(code).strip()
        }

        resp = self.post(url, data=payload)
        
        with open("response.txt", "w", encoding="utf-8") as f:
            f.write(resp.text)
        if resp.status_code != 200:
            return {"error": "Server xato berdi", "status_code": resp.status_code}

        html = resp.text.strip()

        # Agar hech narsa topilmasa
        if len(html) < 100 or "не найдено" in html.lower() or "topilmadi" in html.lower():
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
            "region": "Андижанская область",
            'ps':"",
            'birth_date':"",
            'jshshir':""
            
        }
        #ID 
        id_tag =  soup.select('tr td b')[0]
        

        if id_tag :
            result["ID"] = id_tag.text
            # print("ID topildi:", result["ID"])
        # FIO
        ind=0
        h1_titles  = soup.find_all('td')
        if h1_titles:
            for h1 in h1_titles:
                ind+=1
                if h1.text=='Ф.И.О':
                    fio_tag = h1_titles[ind].text
                    result["fio"] = fio_tag
                if h1.text=='ОРГАНИЗАЦИЯ':
                    org_tag = h1_titles[ind].text
                    result["organization"] = org_tag
                if h1.text=='МАХАЛЛЯ: ':
                    addr_tag = h1_titles[ind].text  
                    result["address"] = addr_tag
                if h1.text=='ТЕЛЕФОН':  
                    phone_tag = h1_titles[ind].text
                    result["phone"] = phone_tag
                if h1.text=='КОНТРАКТ.№':
                    contract_tag = h1_titles[ind].text
                    result["contract"] = contract_tag
                if h1.text=='Статус':
                    status_tag = h1_titles[ind].text.replace('\n','').replace('  ','')
                    result["status"] = status_tag
                if h1.text=='ДЕПОЗИТ':
                    balance_tag = h1_titles[ind].text
                    result["balance"] = balance_tag.replace('\n','').replace('  ','')[1:]
                if "Паспорт серия" in h1.text:
                    ps_tag = h1_titles[ind].text
                    result['ps']=ps_tag
                if h1.text== "Дата рождения":
                    bd_tag = h1_titles[ind].text.replace('\n','').replace('  ','')
                    nind=bd_tag.find(' /')
                    result['birth_date']=bd_tag[:nind]
                if "ИНН / ПИНФЛ" in h1.text:
                    jshshir_tag = h1_titles[ind].text
                    nind=jshshir_tag.find(' /')
                    result['jshshir']=jshshir_tag[:nind]

       
            
    
       

       

      
        
        
        payment_tag = soup.find("b", string=re.compile("Последний платеж|Охирги тўлов", re.I))
        if payment_tag and payment_tag.next_sibling:
            result["last_payment"] = payment_tag.next_sibling.strip()

        # Gaz ballonlari jadvali
        table = soup.find("table")
        if table:
            rows = table.find_all("tr")[1:]  # headerni o'tkazib yuborish
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

        return result
    
    def get_detail(self, encoded_id):
        """
        Ma'lum bir gaz so'rovi tafsilotlarini olish uchun funksiya
        encoded_id - bazadagi ID Base64 ko'rinishida
        """
        url = f"{EGAZ_HOME}/admin/gas_requests/detail/{ to_base64( encoded_id)}"
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,uz;q=0.8",
            "Connection": "keep-alive",
            "Host": "egaz.uz",
            "Referer": f"{EGAZ_HOME}/admin/gas_requests",
            "User-Agent": "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 CrKey/1.54.250320",
            "X-CSRF-TOKEN": self.csrf_token,
            "X-Requested-With": "XMLHttpRequest",
            "Cache-Control": "no-cache, private"
        }

        response = self.session.get(url, headers=headers, timeout=5)

        # Agar login sahifasiga yo‘naltirsa → cookie eskirgan
        if response.status_code in [301, 302, 303] or "login" in response.url.lower():
            print("Sessiya eskirgan → qayta login qilinmoqda...")
            refresh_cookies()
            self.load_cookies()
            self.update_csrf_token()
            headers["X-CSRF-TOKEN"] = self.csrf_token
            response = self.session.get(url, headers=headers, timeout=5)

        if response.status_code == 200:
            return response.text
        else:
            print(f"Xato: {response.status_code}")
            return None



# =============================
# FOYDALANISH MISOLI
# =============================

# if __name__ == "__main__":
    # bot = EGazBot()
    # info = bot.get_subscriber("01000099813")

#     # Bitta abonent
#     
#     print(json.dumps(info, ensure_ascii=False, indent=2))

    # Bir nechta
    # codes = ["01000100089", "02000200123", "03000300456"]
    # for code in codes:
    #     print(f"\n→ {code}")
    #     print(bot.get_subscriber(code))