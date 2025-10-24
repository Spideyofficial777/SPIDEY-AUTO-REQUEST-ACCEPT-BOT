#!/bin/bash

# Spider-Man Auto Request Accept Bot - Deployment Script
# 🕷️ Advanced Telegram Bot with Multi-FSub Support

echo "🕸️ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🕸️"
echo "   SPIDER-MAN AUTO REQUEST ACCEPT BOT"
echo "🕸️ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🕸️"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed! Please install Python 3.8+"
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed! Please install pip3"
    exit 1
fi

echo "✅ pip3 found: $(pip3 --version)"

# Clone repository
echo ""
echo "📥 Cloning Spider-Man Bot repository..."
git clone https://github.com/Spideyofficial777/SPIDEY-AUTO-REQUEST-ACCEPT-BOT.git
cd SPIDEY-AUTO-REQUEST-ACCEPT-BOT

# Create virtual environment
echo ""
echo "🐍 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install requirements
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Create config file if it doesn't exist
if [ ! -f "configs.py" ]; then
    echo ""
    echo "⚙️  Creating config file..."
    cat > configs.py << EOL
# Spider-Man Bot Configuration
# Get these values from my.telegram.org

API_ID = "YOUR_API_ID"           # Get from https://my.telegram.org
API_HASH = "YOUR_API_HASH"       # Get from https://my.telegram.org
BOT_TOKEN = "YOUR_BOT_TOKEN"     # Get from @BotFather
ADMINS = [123456789]             # Your Telegram ID
LOG_CHANNEL = -1001234567890     # Private channel ID for logs
CHANNEL_IDS = [-1001234567890]   # Force subscribe channels
DATABASE_URI = "mongodb://localhost:27017"  # MongoDB URI

# Optional Configurations
CAPTCHA_ENABLED = True           # Enable CAPTCHA verification
WELCOME_MESSAGE = True           # Send welcome messages
USER_LOGGING = True              # Log user activities
EOL
    echo "✅ configs.py created! Please edit it with your credentials."
fi

echo ""
echo "🎯 Deployment Methods Available:"
echo "1. Bot Hosting Net"
echo "2. VPS/Local Deployment"
echo "3. Koyeb Cloud"
echo "4. Railway"
echo "5. Heroku"

echo ""
echo "🚀 Quick Start:"
echo "1. Edit configs.py with your credentials"
echo "2. Run: python3 bot.py"
echo "3. Your bot will start automatically!"

echo ""
echo "📋 Required Environment Variables:"
echo "   API_ID        - From my.telegram.org"
echo "   API_HASH      - From my.telegram.org" 
echo "   BOT_TOKEN     - From @BotFather"
echo "   ADMINS        - Your Telegram ID"
echo "   LOG_CHANNEL   - Private channel ID"
echo "   CHANNEL_IDS   - Force sub channels"
echo "   DATABASE_URI  - MongoDB connection string"

echo ""
echo "🛠️  Features Included:"
echo "   ✓ Auto Join Request Accept"
echo "   ✓ Multi Force Subscribe"
echo "   ✓ CAPTCHA Verification"
echo "   ✓ Welcome Messages"
echo "   ✓ User Logging"
echo "   ✓ Admin Commands"
echo "   ✓ Stats Tracking"
echo "   ✓ Database Integration"

echo ""
echo "📞 Support:"
echo "   Group: @spideyofficial_777"
echo "   Channel: @spidey_updates"
echo "   Developer: @spideyofficial_777"

echo ""
echo "🕸️ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🕸️"
echo "   Ready to deploy your Spider-Man Bot!"
echo "   Edit configs.py and run: python3 bot.py"
echo "🕸️ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━🕸️"

# Make bot executable
chmod +x bot.py
