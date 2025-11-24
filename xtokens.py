import hashlib
import time




def generate_token(authKey, timestamp, model, versionCode):
    userAgent = f"ANDROID/{model}/{versionCode}"
    raw = authKey + timestamp + userAgent
    md5_hash = hashlib.md5(raw.encode()).hexdigest()
    return md5_hash


authKey = "deQyICqU78pu43zHrM1KM0jWLYxV8r4iNLF6qbVLnlbm90"
timestamp = str(int(time.time()*1000))
model = "2201117TG"
versionCode = "259"

Xauthorization_token = generate_token(authKey, timestamp, model, versionCode)


import hashlib

def make_hash(email: str, user_id: str, timestamp: str) -> str:


    raw = timestamp + email + user_id
    md5_hash = hashlib.md5(raw.encode()).hexdigest()
    return md5_hash

