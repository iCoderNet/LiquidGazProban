# import bot
# import func

# # Initialize bot
# Ebot = bot.EGazBot()
# print(Ebot.get_subscriber("01000084867"))

import base64

id_str = "1995203"
encoded = base64.b64encode(id_str.encode()).decode()
print(encoded)

# MTk5NTIwMw==
# MTk5NTIwMw==
# MTk5NTIwMyA=