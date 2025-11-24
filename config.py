"""
Configuration Management for LiquidGazProban
Manages all application settings and constants
"""
import os
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# API Configuration
class APIConfig:
    """API related configuration"""
    BASE_URL = 'https://egaz.uz/api'
    WEB_BASE_URL = 'https://egaz.uz'
    
    # Token configuration - должны быть загружены из переменных окружения
    AUTH_KEY = os.getenv('EGAZ_AUTH_KEY', 'deQyICqU78pu43zHrM1KM0jWLYxV8r4iNLF6qbVLnlbm90')
    DEVICE_MODEL = os.getenv('EGAZ_DEVICE_MODEL', '2201117TG')
    VERSION_CODE = os.getenv('EGAZ_VERSION_CODE', '259')
    
    # Default values
    DEFAULT_LOCATION = "41.311081,69.240562"
    DEFAULT_IP = "10.52.79.219"
    DEFAULT_DEVICE = f'Device:spes Model:{DEVICE_MODEL}'
    
    # Timeouts
    REQUEST_TIMEOUT = 30
    DEFAULT_TIMEOUT = 10

# Login Configuration
class LoginConfig:
    """Login credentials configuration"""
    # IMPORTANT: These should be loaded from environment variables
    EGov_LOGIN = os.getenv('EGOV_LOGIN', '')
    EGov_PASSWORD = os.getenv('EGOV_PASSWORD', '')
    LOGIN_URL = "https://egaz.uz/user/socialize/egov"
    ADMIN_URL = "http://egaz.uz/admin"
    
    # Cookie management
    COOKIE_FILE = str(DATA_DIR / "cookies.json")

# UI Configuration
class UIConfig:
    """UI related settings"""
    # Colors
    PRIMARY_COLOR = "#667eea"
    SECONDARY_COLOR = "#764ba2"
    SUCCESS_COLOR = "#43cea2"
    DANGER_COLOR = "#e74c3c"
    WARNING_COLOR = "#f39c12"
    INFO_COLOR = "#3498db"
    
    # Fonts
    FONT_FAMILY = "Arial"
    TITLE_FONT_SIZE = 24
    HEADING_FONT_SIZE = 16
    NORMAL_FONT_SIZE = 11
    SMALL_FONT_SIZE = 9
    
    # Window sizes
    LOGIN_WINDOW_SIZE = "400x550"
    DASHBOARD_WINDOW_SIZE = "900x600"
    ORDERS_WINDOW_SIZE = "1000x700"
    SELL_WINDOW_SIZE = "700x800"

# File paths
class FilePaths:
    """Application file paths"""
    COOKIES_FILE = str(DATA_DIR / "cookies.json")
    RESPONSE_FILE = str(DATA_DIR / "response.txt")
    ORDER_DETAIL_FILE = str(DATA_DIR / "order_detail.html")
    DEFAULT_PHOTO = str(BASE_DIR / "rasm.jpg")
    
    # JSON data files
    NEXT_JSON = str(BASE_DIR / "nxt.json")
    PR_JSON = str(BASE_DIR / "pr.json")

# Logging Configuration
class LogConfig:
    """Logging configuration"""
    LOG_FILE = str(LOGS_DIR / "app.log")
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB
    BACKUP_COUNT = 5

# Application Constants
class AppConstants:
    """Application-wide constants"""
    APP_NAME = "LiquidGazProban"
    APP_VERSION = "1.0.0"
    REGION_NAME = "Андижанская область"
    
    # Pagination
    DEFAULT_TAKE = 100
    DEFAULT_OFFSET = 0
    
    # GPS path generation
    DEFAULT_GPS_STEPS = 120

# Development settings
class DevConfig:
    """Development-specific settings"""
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    PLAYWRIGHT_HEADLESS = os.getenv('PLAYWRIGHT_HEADLESS', 'False').lower() == 'true'

# Export all configs
def get_config(config_name: str) -> object:
    """Get configuration by name"""
    configs = {
        'api': APIConfig,
        'login': LoginConfig,
        'ui': UIConfig,
        'files': FilePaths,
        'log': LogConfig,
        'app': AppConstants,
        'dev': DevConfig
    }
    return configs.get(config_name.lower())

# Validation
def validate_config() -> bool:
    """Validate critical configuration settings"""
    errors = []
    
    if not LoginConfig.EGov_LOGIN:
        errors.append("EGOV_LOGIN environment variable is not set")
    
    if not LoginConfig.EGov_PASSWORD:
        errors.append("EGOV_PASSWORD environment variable is not set")
    
    if errors:
        print("Configuration Errors:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    return True

if __name__ == "__main__":
    # Test configuration
    print(f"🔧 {AppConstants.APP_NAME} v{AppConstants.APP_VERSION}")
    print(f"📁 Base Directory: {BASE_DIR}")
    print(f"📁 Data Directory: {DATA_DIR}")
    print(f"📁 Logs Directory: {LOGS_DIR}")
    print(f"🌐 API Base URL: {APIConfig.BASE_URL}")
    print(f"🔐 Config Validation: {'✅ Passed' if validate_config() else '❌ Failed'}")
