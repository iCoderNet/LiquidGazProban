from bs4 import BeautifulSoup
import requests
import os

def extract_td_a(html, kod, encoding="utf-8"):
    """
    get_detail() HTMLidan sotilmagan balonlar va sotib olmagan foydalanuvchilarni ajratib oladi
    
    Args:
        html: get_detail() dan qaytgan HTML
        kod: Asosiy request kod (filtrlash uchun)
        encoding: Encoding (default: utf-8)
    
    Returns:
        {
            'balon_id': [unsold balloon codes],
            'codes': [subscriber codes who haven't purchased yet]
        }
    """
    
    soup = BeautifulSoup(html, "lxml")
    
    # tab_01 ichidagi jadvalni topish (РЕАЛИЗОВАННЫЕ БАЛЛОНЫ)
    tab_01 = soup.find("div", {"id": "tab_01"})
    
    balon_id = []
    sold_subscriber_codes = set()  # Sotib olgan abonentlar kodlari
    
    if tab_01:
        table = tab_01.find("table")
        if table:
            rows = table.find_all("tr")[1:]  # Skip header
            
            for row in rows:
                cols = row.find_all("td")
                if len(cols) > 6:
                    # Column 4: Balloon code
                    balloon_code = ""
                    if len(cols) > 4:
                        balloon_link = cols[4].find("a")
                        if balloon_link:
                            balloon_code = balloon_link.text.strip()
                    
                    # Column 6: Subscriber code
                    subscriber_code = ""
                    subscriber_link = cols[6].find("a")
                    if subscriber_link:
                        subscriber_code = subscriber_link.text.strip()
                        if subscriber_code:  # Agar mavjud bo'lsa - sotib olgan
                            sold_subscriber_codes.add(subscriber_code)
                    
                    # Agar subscriber code bo'sh bo'lsa - balon sotilmagan
                    if not subscriber_code and balloon_code:
                        balon_id.append(balloon_code)
    
    # tab_06 ichidagi jadvalni topish (ПРЕДЛОЖЕННЫЕ - suggested subscribers)
    # MUHIM: Faqat sotilmagan balonlar soniga teng miqdorda abonent qaytaramiz
    tab_06 = soup.find("div", {"id": "tab_06"})
    
    codes = []
    unsold_balloon_count = len(balon_id)  # Sotilmagan balonlar soni
    
    if tab_06:
        table = tab_06.find("table")
        if table:
            rows = table.find_all("tr")[1:]  # Skip header
            
            for row in rows:
                cols = row.find_all("td")
                if len(cols) > 3:  # Kod ustuni 4-chi (index 3)
                    # Column 3: Kod
                    kod_link = cols[3].find("a")
                    if kod_link:
                        subscriber_code = kod_link.text.strip()
                        # Faqat sotib olmagan abonentlarni qo'shamiz
                        if subscriber_code and subscriber_code not in sold_subscriber_codes:
                            codes.append(subscriber_code)
                            
                            # Faqat sotilmagan balonlar soniga teng miqdorda qaytaramiz
                            if len(codes) >= unsold_balloon_count:
                                break
    
    return {'balon_id': balon_id, 'codes': codes}

def generate_path(start_lat, start_lng, stop_lat, stop_lng, steps):
    path = []

    lat_step = (stop_lat - start_lat) / (steps - 1)
    lng_step = (stop_lng - start_lng) / (steps - 1)

    for i in range(steps):
        lat = start_lat + lat_step * i
        lng = start_lng + lng_step * i
        path.append((round(lat, 7), round(lng, 7)))

    return path

def get_pic_url(seria, db):
    if os.path.exists(f"passport_{seria}.jpg"):
        return f"passport_{seria}.jpg"
    url = "http://176.96.243.106:8000/get-passport-info"   # Lokaldagi server
    payload = {
        "passport": seria,
        "date_birthday": db,
        "max_attempts": 7
    }

    try:
        resp = requests.post(url, json=payload,timeout=60)
        resp.raise_for_status()   # HTTP xatolarni ushlash
        data = resp.json()
        print("Server javobi:", data)
        picurl= f"https://api.5tashabbus.uz/FileManage/Get?id={data['result']['photo']['attachmentfileid']}"
        headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}
        
        resp = requests.get(picurl, headers=headers)
        if resp.status_code == 200:
            with open(f"passport_{seria}.jpg", "wb") as f:
                f.write(resp.content)
            return f"passport_{seria}.jpg"
        else:
            return None
    except requests.exceptions.RequestException as e:
        print("So'rov xatosi:", e)
        return None

    except ValueError:
        print("JSON format xatosi. Server noto'g'ri javob qaytardi.")
        return None
