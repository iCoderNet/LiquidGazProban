import bot
import func

# Initialize bot
Ebot = bot.EGazBot()
st = Ebot.get_detail("1270465")
sa=func.extract_td_a(st, "1270465")
print(len(sa['codes']),len(sa['balon_id']))

