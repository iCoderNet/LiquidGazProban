from bs4 import BeautifulSoup
import sys

# Set UTF-8 encoding for output
sys.stdout.reconfigure(encoding='utf-8')

# Read the HTML file
with open(r"c:\Users\Banda\Desktop\egaz\LiquidGazProban\raygaz.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "lxml")

# Find tab_06
tab_06 = soup.find("div", {"id": "tab_06"})

if tab_06:
    print("=== TAB_06 TOPILDI ===\n")
    table = tab_06.find("table")
    
    if table:
        # Get header
        header = table.find("thead")
        if header:
            header_cols = header.find_all("th")
            print(f"Ustunlar soni: {len(header_cols)}")
            print("Ustunlar:")
            for i, col in enumerate(header_cols):
                print(f"  {i}: {col.text.strip()}")
        
        # Get rows
        rows = table.find_all("tr")[1:]  # Skip header
        print(f"\nJami qatorlar: {len(rows)}")
        
        if rows:
            print(f"\nBirinchi 3 qator:")
            for i, row in enumerate(rows[:3]):
                cols = row.find_all("td")
                print(f"\n  Qator {i+1} ({len(cols)} ustun):")
                
                # Try to find links in each column
                for j, col in enumerate(cols):
                    links = col.find_all("a")
                    if links:
                        for link in links:
                            text = link.text.strip()
                            if text:
                                print(f"    Ustun {j}: {text}")
                    else:
                        text = col.text.strip()
                        if text:
                            print(f"    Ustun {j}: {text[:50]}")
else:
    print("TAB_06 TOPILMADI!")
