# LiquidGazProban

**Professional Desktop Application for Gas Cylinder Management**

## 📋 Overview

LiquidGazProban - bu suyuq gaz ballonlarini boshqarish va sotish jarayonini avtomatlashtiruvchi professional desktop dastur. Egaz.uz tizimi bilan integratsiyalangan.

## ✨ Features

- 🔐 **Secure Authentication** - Inspector authentication with session management
- 📦 **Order Management** - View and manage gas cylinder orders
- 🛒 **Sales Processing** - Automated sales workflow with GPS tracking
- 👥 **Subscriber Management** - Search and manage subscriber information
- 📊 **Dashboard** - Comprehensive overview of operations
- 🔄 **Real-time Updates** - Live data synchronization with egaz.uz
- 📝 **Logging System** - Comprehensive activity logging

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Windows OS
- Internet connection

### Step 1: Clone Repository

```bash
git clone <repository_url>
cd LiquidGazProban
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Install Playwright Browsers

```bash
playwright install chromium
```

### Step 4: Configure Environment

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` file and add your credentials:
   ```
   EGOV_LOGIN=your_username
   EGOV_PASSWORD=your_password
   ```

## 🎯 Usage

### Running the Application

```bash
python main.py
```

### First Time Setup

1. Launch the application
2. Enter your inspector credentials
3. Wait for authentication
4. Access the dashboard

## 📁 Project Structure

```
LiquidGazProban/
├── api/
│   └── inspector_login.py    # API client for egaz.uz
├── bot.py                      # Web scraping bot
├── main.py                     # Login window
├── profile.py                  # Dashboard
├── product.py                  # Orders management
├── sotuv.py                    # Sales window
├── func.py                     # Helper functions
├── login.py                    # Cookie management
├── xtokens.py                  # Token generation
├── config.py                   # Configuration management
├── logger.py                   # Logging system
├── data/                       # Data files (auto-created)
├── logs/                       # Log files (auto-created)
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
└── requirements.txt            # Python dependencies
```

## 🔧 Configuration

All configuration is managed through `config.py` and environment variables:

- **APIConfig**: API endpoints and settings
- **LoginConfig**: Authentication credentials
- **UIConfig**: UI colors and fonts
- **FilePaths**: File locations
- **LogConfig**: Logging settings

## 📝 Logging

Logs are automatically saved to `logs/app.log` with rotation (10MB max):

- INFO: General operational messages
- DEBUG: Detailed diagnostic information
- WARNING: Warning messages
- ERROR: Error messages with stack traces

## 🔒 Security

- ✅ Credentials stored in `.env` file (not in code)
- ✅ `.env` file excluded from git
- ✅ Session management with automatic refresh
- ✅ Secure token generation
- ✅ CSRF protection

## 🛠️ Development

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings to functions/classes
- Keep functions focused and concise

### Testing

```bash
# Test token generation
python xtokens.py

# Test configuration
python config.py

# Test logging
python logger.py

# Test bot
python bot.py
```

## 📊 Features in Detail

### Authentication
- Inspector login with egaz.uz credentials
- Automatic session management
- Cookie-based authentication

### Dashboard
- User profile information
- Organization details
- Quick access to main features

### Order Management
- View accepted orders
- Filter by inspector
- Real-time statistics
- Sales tracking

### Sales Processing
- GPS coordinate tracking
- Automated path generation
- Subscriber validation
- Photo upload
- Balance verification

## ⚠️ Troubleshooting

### Common Issues

**Issue**: Cookie refresh fails
```
Solution: Check your EGov credentials in .env file
```

**Issue**: API requests fail
```
Solution: Check internet connection and API token
```

**Issue**: Import errors
```
Solution: Install all dependencies: pip install -r requirements.txt
```

## 📞 Support

For support and questions:
- Check logs in `logs/app.log`
- Review configuration in `config.py`
- Contact system administrator

## 📜 License

Internal use only. Proprietary software.

## 🔄 Version

**v1.0.0** - Initial professional release

---

**Created by**: Professional Development Team  
**Last Updated**: 2025-11-24
