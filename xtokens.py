"""
Token and Hash Generation Module
Handles authentication token and hash generation for egaz.uz API
"""
import hashlib
import time
from config import APIConfig
from logger import get_logger

logger = get_logger('Tokens')


def generate_token(auth_key: str, timestamp: str, model: str, version_code: str) -> str:
    """
    Generate authorization token for API requests
    
    Args:
        auth_key: Authentication key
        timestamp: Current timestamp in milliseconds
        model: Device model
        version_code: App version code
    
    Returns:
        MD5 hash token
    """
    user_agent = f"ANDROID/{model}/{version_code}"
    raw = auth_key + timestamp + user_agent
    md5_hash = hashlib.md5(raw.encode()).hexdigest()
    logger.debug(f"Generated token for model {model}")
    return md5_hash


def make_hash(email: str, user_id: str, timestamp: str) -> str:
    """
    Generate authentication hash for API requests
    
    Args:
        email: User email
        user_id: User ID
        timestamp: Current timestamp
    
    Returns:
        MD5 hash for authentication
    """
    raw = timestamp + email + user_id
    md5_hash = hashlib.md5(raw.encode()).hexdigest()
    logger.debug(f"Generated hash for user {user_id}")
    return md5_hash


def get_current_token() -> tuple[str, str]:
    """
    Get current authorization token and timestamp
    
    Returns:
        Tuple of (token, timestamp)
    """
    timestamp = str(int(time.time() * 1000))
    token = generate_token(
        APIConfig.AUTH_KEY,
        timestamp,
        APIConfig.DEVICE_MODEL,
        APIConfig.VERSION_CODE
    )
    logger.info("Generated new authorization token")
    return token, timestamp


# Generate current token for backward compatibility
timestamp = str(int(time.time() * 1000))
Xauthorization_token = generate_token(
    APIConfig.AUTH_KEY,
    timestamp,
    APIConfig.DEVICE_MODEL,
    APIConfig.VERSION_CODE
)


if __name__ == "__main__":
    # Test token generation
    token, ts = get_current_token()
    print(f"🔑 Token: {token[:20]}...")
    print(f"⏰ Timestamp: {ts}")
    
    # Test hash generation
    test_hash = make_hash("test@example.com", "12345", ts)
    print(f"🔐 Hash: {test_hash[:20]}...")

2025-11-26 00:47:35,352 - INFO - Form olinmoqda: https://egaz.uz/admin/subscribers/edit-data/MTcyNTQ4NQ==
2025-11-26 00:47:35,395 - INFO - Form muvaffaqiyatli yuborildi
2025-11-26 00:47:35,690 - INFO - Response status: 256
2025-11-26 00:47:35,690 - INFO - Abonent MTc0NTk5MQ== muvaffaqiyatli yangilandi
2025-11-26 00:47:35,691 - INFO - Form muvaffaqiyatli olindi
[24644/46416] (53.1%) ✅ 01000118741: Muvaffaqiyatli yangilandi
2025-11-26 00:47:35,691 - INFO - Form muvaffaqiyatli olindi
2025-11-26 00:47:35,745 - INFO - is_need qiymati '2' (НЕ НУЖДАЕТСЯ) ga o'zgartirildi
2025-11-26 00:47:35,765 - INFO - is_need qiymati '2' (НЕ НУЖДАЕТСЯ) ga o'zgartirildi
2025-11-26 00:47:35,829 - INFO - Jami 24 ta form maydoni topildi
INFO - Successfully parsed subscriber data for 01000098175
2025-11-26 00:47:35,875 - INFO - Jami 24 ta form maydoni topildi
INFO - Successfully parsed subscriber data for 01000088293
2025-11-26 00:47:35,923 - INFO - Form yuborilmoqda: https://egaz.uz/admin/subscribers/update-save
INFO - Successfully parsed subscriber data for 01000097415
2025-11-26 00:47:35,717 - INFO - Successfully parsed subscriber data for 01000098175
INFO - Successfully parsed subscriber data for 01000119997
2025-11-26 00:47:35,755 - INFO - Successfully parsed subscriber data for 01000088293
INFO - Successfully parsed subscriber data for 01000094968
2025-11-26 00:47:35,978 - INFO - Form yuborilmoqda: https://egaz.uz/admin/subscribers/update-save
INFO - Successfully parsed subscriber data for 01000091252
2025-11-26 00:47:35,851 - INFO - Successfully parsed subscriber data for 01000097415
2025-11-26 00:47:35,980 - INFO - Abonent qayta ishlanmoqda: MTcyNTQyNQ==
2025-11-26 00:47:35,879 - INFO - Successfully parsed subscriber data for 01000119997
2025-11-26 00:47:35,981 - INFO - Abonent qayta ishlanmoqda: MTcxNTU0Mw==
2025-11-26 00:47:35,923 - INFO - Successfully parsed subscriber data for 01000094968
2025-11-26 00:47:35,978 - INFO - Successfully parsed subscriber data for 01000091252
2025-11-26 00:47:35,984 - INFO - Abonent qayta ishlanmoqda: MTcyNDY2NQ==
2025-11-26 00:47:35,984 - INFO - Form olinmoqda: https://egaz.uz/admin/subscribers/edit-data/MTcyNTQyNQ==
2025-11-26 00:47:35,985 - INFO - Abonent qayta ishlanmoqda: MTc0NzI0Nw==
2025-11-26 00:47:35,985 - INFO - Form olinmoqda: https://egaz.uz/admin/subscribers/edit-data/MTcxNTU0Mw==
2025-11-26 00:47:35,986 - INFO - Abonent qayta ishlanmoqda: MTcyMjIxOA==
2025-11-26 00:47:35,986 - INFO - Abonent qayta ishlanmoqda: MTcxODUwMg==
2025-11-26 00:47:35,986 - INFO - Form olinmoqda: https://egaz.uz/admin/subscribers/edit-data/MTcyNDY2NQ==
2025-11-26 00:47:35,987 - INFO - Form olinmoqda: https://egaz.uz/admin/subscribers/edit-data/MTc0NzI0Nw==
2025-11-26 00:47:35,988 - INFO - Form olinmoqda: https://egaz.uz/admin/subscribers/edit-data/MTcyMjIxOA==
2025-11-26 00:47:35,989 - INFO - Form olinmoqda: https://egaz.uz/admin/subscribers/edit-data/MTcxODUwMg==
2025-11-26 00:47:36,190 - INFO - Form muvaffaqiyatli yuborildi
2025-11-26 00:47:36,190 - INFO - Response status: 256
2025-11-26 00:47:36,190 - INFO - Abonent MTcyNDQ3NA== muvaffaqiyatli yangilandi
[24645/46416] (53.1%) ✅ 01000097224: Muvaffaqiyatli yangilandi
2025-11-26 00:47:36,259 - INFO - Form muvaffaqiyatli yuborildi
2025-11-26 00:47:36,259 - INFO - Response status: 256
2025-11-26 00:47:36,259 - INFO - Abonent MTczNDYxMA== muvaffaqiyatli yangilandi
[24646/46416] (53.1%) ✅ 01000107360: Muvaffaqiyatli yangilandi
2025-11-26