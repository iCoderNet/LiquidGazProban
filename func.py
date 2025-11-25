from bs4 import BeautifulSoup
import requests
import os
from logger import get_logger

# Initialize logger for utility functions
logger = get_logger('func')

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
    logger.info(f"🔍 HTML parsing boshlandi - Request kod: {kod}")
    
    soup = BeautifulSoup(html, "lxml")
    logger.debug("BeautifulSoup obyekti yaratildi")
    
    # tab_01 ichidagi jadvalni topish (РЕАЛИЗОВАННЫЕ БАЛЛОНЫ)
    tab_01 = soup.find("div", {"id": "tab_01"})
    
    balon_id = []
    sold_subscriber_codes = set()  # Sotib olgan abonentlar kodlari
    
    logger.debug("Tab_01 (РЕАЛИЗОВАННЫЕ БАЛЛОНЫ) qidirilmoqda...")
    
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
                        logger.debug(f"Sotilmagan balon topildi: {balloon_code}")
    
    logger.info(f"✅ Tab_01 parsing tugadi - Sotilmagan balonlar: {len(balon_id)} ta, Sotib olgan abonentlar: {len(sold_subscriber_codes)} ta")
    
    # tab_06 ichidagi jadvalni topish (ПРЕДЛОЖЕННЫЕ - suggested subscribers)
    # MUHIM: Faqat sotilmagan balonlar soniga teng miqdorda abonent qaytaramiz
    tab_06 = soup.find("div", {"id": "tab_06"})
    
    codes = []
    unsold_balloon_count = len(balon_id)  # Sotilmagan balonlar soni
    
    logger.debug(f"Tab_06 (ПРЕДЛОЖЕННЫЕ) qidirilmoqda - Kerakli abonentlar: {unsold_balloon_count} ta")
    
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
                                logger.debug(f"Yetarli abonent topildi: {len(codes)} ta")
                                break
    
    logger.info(f"🎯 Parsing yakunlandi - Balonlar: {len(balon_id)} ta, Abonentlar: {len(codes)} ta")
    logger.debug(f"Balonlar: {balon_id[:3]}..." if len(balon_id) > 3 else f"Balonlar: {balon_id}")
    logger.debug(f"Abonentlar: {codes[:3]}..." if len(codes) > 3 else f"Abonentlar: {codes}")
    
    return {'balon_id': balon_id, 'codes': codes}

def generate_path(start_lat, start_lng, stop_lat, stop_lng, steps):
    logger.info(f"🗺️ GPS yo'nalish yaratilmoqda: ({start_lat}, {start_lng}) → ({stop_lat}, {stop_lng})")
    logger.debug(f"Qadamlar soni: {steps}")
    
    path = []

    lat_step = (stop_lat - start_lat) / (steps - 1)
    lng_step = (stop_lng - start_lng) / (steps - 1)

    for i in range(steps):
        lat = start_lat + lat_step * i
        lng = start_lng + lng_step * i
        path.append((round(lat, 7), round(lng, 7)))
    
    logger.info(f"✅ GPS yo'nalish yaratildi - {len(path)} ta nuqta")
    logger.debug(f"Birinchi nuqta: {path[0]}, Oxirgi nuqta: {path[-1]}")

    return path

def get_pic_url(seria, db):
    logger.info(f"📸 Passport rasmi so'ralmoqda - Seria: {seria}, Tug'ilgan sana: {db}")
    
    # Check if file already exists
    filename = f"passport_{seria}.jpg"
    if os.path.exists(filename):
        logger.info(f"✅ Rasm allaqachon mavjud: {filename}")
        return filename
    url = "http://176.96.243.106:8000/get-passport-info"   # Lokaldagi server
    payload = {
        "passport": seria.replace(" ", "") ,
        "date_birthday": db.replace(" ", "") ,
        "max_attempts": 7
    }
    
    logger.debug(f"API so'rov yuborilmoqda: {url}")
    logger.debug(f"Payload: passport={seria}, date_birthday={db}")

    try:
        resp = requests.post(url, json=payload, timeout=60)
        print(resp.json())
        logger.debug(f"API so'rov yuborildi: {resp}")
        resp.raise_for_status()   # HTTP xatolarni ushlash
        data = resp.json()
        
        logger.debug(f"Server javobi olindi: {data.get('result', {}).get('photo', {}).get('attachmentfileid', 'N/A')}")
        picurl = f"https://api.5tashabbus.uz/FileManage/Get?id={data['result']['photo']['attachmentfileid']}"
        logger.debug(f"Rasm URL: {picurl}")
        
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            )
        }
        
        logger.debug("Rasm yuklab olinmoqda...")
        resp = requests.get(picurl, headers=headers)
        
        if resp.status_code == 200:
            with open(filename, "wb") as f:
                f.write(resp.content)
            logger.info(f"✅ Rasm muvaffaqiyatli saqlandi: {filename} ({len(resp.content)} bytes)")
            return filename
        else:
            logger.error(f"❌ Rasm yuklab olishda xatolik: HTTP {resp.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ API so'rov xatosi: {str(e)}", exc_info=True)
        return None
    except KeyError as e:
        logger.error(f"❌ JSON ma'lumot xatosi - Kalit topilmadi: {str(e)}", exc_info=True)
        return None
    except ValueError as e:
        logger.error(f"❌ JSON format xatosi: {str(e)}", exc_info=True)
        return None
    except Exception as e:
        logger.error(f"❌ Kutilmagan xatolik: {str(e)}", exc_info=True)
        return None
