from bs4 import BeautifulSoup

# Read the HTML file
with open(r"c:\Users\Banda\Desktop\egaz\LiquidGazProban\raygaz.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "lxml")

# Find tab_01 (РЕАЛИЗОВАННЫЕ БАЛЛОНЫ)
tab_01 = soup.find("div", {"id": "tab_01"})

sold_count = 0
unsold_count = 0

if tab_01:
    table = tab_01.find("table")
    if table:
        rows = table.find_all("tr")[1:]  # Skip header
        
        print(f"=== TAB_01 ANALYSIS ===")
        print(f"Total rows in tab_01: {len(rows)}")
        
        for row in rows:
            cols = row.find_all("td")
            
            if len(cols) > 6:
                # Column 6: Subscriber code
                subscriber_link = cols[6].find("a")
                if subscriber_link and subscriber_link.text.strip():
                    sold_count += 1
                else:
                    unsold_count += 1
        
        print(f"Sold balloons (with subscriber): {sold_count}")
        print(f"Unsold balloons (no subscriber): {unsold_count}")

# Check for tab_06
print(f"\n=== TAB_06 ANALYSIS ===")
tab_06 = soup.find("div", {"id": "tab_06"})
print(f"tab_06 exists: {tab_06 is not None}")

if tab_06:
    table = tab_06.find("table")
    print(f"tab_06 has table: {table is not None}")
    
    if table:
        # Get header to understand column structure
        header = table.find("thead")
        if header:
            header_cols = header.find_all("th")
            print(f"\nHeader columns ({len(header_cols)}):")
            for i, col in enumerate(header_cols):
                print(f"  Column {i}: {col.text.strip()}")
        
        # Get rows
        rows = table.find_all("tr")[1:]  # Skip header
        print(f"\nTotal rows in tab_06: {len(rows)}")
        
        if rows:
            print(f"\nFirst 3 rows analysis:")
            for i, row in enumerate(rows[:3]):
                cols = row.find_all("td")
                print(f"\nRow {i+1}:")
                print(f"  Total columns: {len(cols)}")
                for j, col in enumerate(cols):
                    link = col.find("a")
                    if link:
                        print(f"  Column {j}: {link.text.strip()}")
                    else:
                        print(f"  Column {j}: {col.text.strip()[:50]}")
