from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"c:\Users\Banda\Desktop\egaz\LiquidGazProban\raygaz.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "lxml")

# Find tab_01
tab_01 = soup.find("div", {"id": "tab_01"})

if tab_01:
    table = tab_01.find("table")
    if table:
        rows = table.find_all("tr")[1:]  # Skip header
        
        print(f"=== TAB_01 TAHLILI ===")
        print(f"Jami qatorlar: {len(rows)}\n")
        
        sold_count = 0
        unsold_count = 0
        
        print("Birinchi 5 qator:")
        for i, row in enumerate(rows[:5]):
            cols = row.find_all("td")
            
            if len(cols) > 6:
                # Column 4: Balloon code
                balloon_code = ""
                balloon_link = cols[4].find("a")
                if balloon_link:
                    balloon_code = balloon_link.text.strip()
                
                # Column 6: Subscriber code - bu yerda link ichida bo'lishi mumkin
                subscriber_code = ""
                col6 = cols[6]
                
                # Try to find all links in column 6
                links = col6.find_all("a")
                for link in links:
                    text = link.text.strip()
                    # Abonent kodi raqamlardan iborat va 01 bilan boshlanadi
                    if text and text.startswith("01") and len(text) >= 10:
                        subscriber_code = text
                        break
                
                has_subscriber = bool(subscriber_code)
                
                abonent_text = subscriber_code if subscriber_code else "YO'Q"
                
                print(f"\n  Qator {i+1}:")
                print(f"    Balon: {balloon_code}")
                print(f"    Abonent: {abonent_text}")
                print(f"    Sotilgan: {'HA' if has_subscriber else 'YOQ'}")
                
                if has_subscriber:
                    sold_count += 1
                else:
                    unsold_count += 1
        
        # Count all rows
        for row in rows[5:]:
            cols = row.find_all("td")
            if len(cols) > 6:
                col6 = cols[6]
                links = col6.find_all("a")
                has_subscriber = False
                for link in links:
                    text = link.text.strip()
                    if text and text.startswith("01") and len(text) >= 10:
                        has_subscriber = True
                        break
                
                if has_subscriber:
                    sold_count += 1
                else:
                    unsold_count += 1
        
        print(f"\n\n=== NATIJA ===")
        print(f"Sotilgan balonlar: {sold_count}")
        print(f"Sotilmagan balonlar: {unsold_count}")
