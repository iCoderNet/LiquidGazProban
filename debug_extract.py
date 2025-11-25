import bot
import func
from bs4 import BeautifulSoup

# Initialize bot
Ebot = bot.EGazBot()

# Test request ID
request_id = '1270887'

print(f"Debugging Request ID: {request_id}")
print("=" * 70)

# Get HTML from get_detail
html = Ebot.get_detail(request_id)

soup = BeautifulSoup(html, "lxml")

# Check tab_01 structure - FULL ANALYSIS
print("\n[TAB_01 - SOLD BALLOONS - FULL ANALYSIS]")
tab_01 = soup.find("div", {"id": "tab_01"})
if tab_01:
    table = tab_01.find("table")
    if table:
        rows = table.find_all("tr")[1:]
        print(f"Total rows: {len(rows)}")
        
        sold_count = 0
        unsold_count = 0
        sold_subscribers = set()
        
        # Analyze all rows
        for row in rows:
            cols = row.find_all("td")
            if len(cols) > 6:
                balloon_link = cols[4].find("a")
                subscriber_link = cols[6].find("a")
                
                balloon_code = balloon_link.text.strip() if balloon_link else ""
                subscriber_code = subscriber_link.text.strip() if subscriber_link else ""
                
                if subscriber_code:
                    sold_count += 1
                    sold_subscribers.add(subscriber_code)
                else:
                    unsold_count += 1
        
        print(f"Sold balloons: {sold_count}")
        print(f"Unsold balloons: {unsold_count}")
        print(f"Unique sold subscribers: {len(sold_subscribers)}")
        print(f"Sold subscriber codes: {sorted(sold_subscribers)}")

# Check tab_06 structure
print("\n[TAB_06 - SUGGESTED SUBSCRIBERS]")
tab_06 = soup.find("div", {"id": "tab_06"})
if tab_06:
    table = tab_06.find("table")
    if table:
        rows = table.find_all("tr")[1:]
        print(f"Total suggested subscribers: {len(rows)}")
        
        all_suggested = []
        for row in rows:
            cols = row.find_all("td")
            if len(cols) > 3:
                kod_link = cols[3].find("a")
                subscriber_code = kod_link.text.strip() if kod_link else ""
                if subscriber_code:
                    all_suggested.append(subscriber_code)
        
        print(f"All suggested codes: {all_suggested}")

# Now run the full extraction
print("\n[FULL EXTRACTION]")
result = func.extract_td_a(html, kod="00620440803")
print(f"Unsold balloons: {len(result['balon_id'])}")
print(f"Users without purchases: {len(result['codes'])}")
print(f"Users without purchases (first 10): {result['codes'][:10]}")
