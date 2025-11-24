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

