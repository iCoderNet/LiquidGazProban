from bs4 import BeautifulSoup
import requests
def extract_td_a(html,kod, encoding="utf-8"):
    """
    index.html faylidan <td><a>...</a></td> elementlarini topib
    list of dict qaytaradi: [{"href":..., "text":..., "attrs": {...}}, ...]
    """
    

    # parser sifatida 'lxml' yoki 'html.parser' ishlatish mumkin
    soup = BeautifulSoup(html, "lxml")

    # CSS selector orqali: faqat td ichidagi to'g'ridan-to'g'ri <a> lar
    anchors = soup.select("td > a")

    
    blonid=[]
    kods=[]
    for a in anchors:
        href = a.get("href", "")
        text = a.get_text(strip=True).replace('✅','')
        jsn=dict()
        attrs = dict(a.attrs)
        if not text in ['❌','✅', ''] and text.startswith('8800') :
            blonid.append(text)
        if text.startswith('01') and len(text)==11:
            if text != kod:
                kods.append(text)
    
    
    

    return {'balon_id':blonid,'codes':kods}
def generate_path(start_lat, start_lng, stop_lat, stop_lng, steps):
    path = []

    lat_step = (stop_lat - start_lat) / (steps - 1)
    lng_step = (stop_lng - start_lng) / (steps - 1)

    for i in range(steps):
        lat = start_lat + lat_step * i
        lng = start_lng + lng_step * i
        path.append((round(lat, 7), round(lng, 7)))

    return path
import requests

def get_pic_url(seria, db):
    url = "https://cp.bot-dev.uz/get-passport-info/"   # Lokaldagi server
    payload = {
        "passport": seria,
        "date_birthday": db,
        "max_attempts": 7
    }

    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()   # HTTP xatolarni ushlash
        data = resp.json()
        print("Server javobi:", data)
        return data

    except requests.exceptions.RequestException as e:
        print("So‘rov xatosi:", e)
        return {"error": str(e)}

    except ValueError:
        print("JSON format xatosi. Server noto‘g‘ri javob qaytardi.")
        return {"error": "invalid_json"}

