import bot
import func

# Initialize bot
Ebot = bot.EGazBot()

# Test request ID
request_id = '1270896'

print(f"Testing with Request ID: {request_id}")
print("=" * 50)

# Get HTML from get_detail
html = Ebot.get_detail(request_id)

# Extract unsold balloons
result = func.extract_td_a(html, kod="00000000371")

print(f"\nResults:")
print(f"  Unsold balloons: {len(result['balon_id'])}")
print(f"  Users without purchases: {len(result['codes'])}")

if result['balon_id']:
    print(f"\n  First 5 unsold balloons:")
    for i, balloon in enumerate(result['balon_id'][:5], 1):
        print(f"    {i}. {balloon}")
    
    if len(result['balon_id']) > 5:
        print(f"    ... and {len(result['balon_id']) - 5} more")

if result['codes']:
    print(f"\n  First 5 users without purchases:")
    for i, code in enumerate(result['codes'][:5], 1):
        print(f"    {i}. {code}")
    
    if len(result['codes']) > 5:
        print(f"    ... and {len(result['codes']) - 5} more")

print(f"\n[OK] Test completed successfully!")