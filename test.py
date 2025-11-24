# pip install beautifulsoup4 lxml
from bs4 import BeautifulSoup

def extract_td_a(html, encoding="utf-8"):
    """
    index.html faylidan <td><a>...</a></td> elementlarini topib
    list of dict qaytaradi: [{"href":..., "text":..., "attrs": {...}}, ...]
    """
    html = html.encode(encoding) if isinstance(html, str) else html

    # parser sifatida 'lxml' yoki 'html.parser' ishlatish mumkin
    soup = BeautifulSoup(html, "lxml")

    # CSS selector orqali: faqat td ichidagi to'g'ridan-to'g'ri <a> lar
    anchors = soup.select("td > a")

    results = []
    for a in anchors:
        href = a.get("href", "")
        text = a.get_text(strip=True).replace('✅','')
        jsn=dict()
        attrs = dict(a.attrs)
        if not text in ['❌','✅', ''] and text.startswith('8800') :
            jsn['balon_id'] = text
        if text.startswith('01'):
            jsn['kod'] = text
        results.append(jsn)

    return results
tana=extract_td_a


