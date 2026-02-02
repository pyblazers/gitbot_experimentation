#!/bin/bash
# Setup launchd service for Mac mini

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VENV_PYTHON="$PROJECT_DIR/venv/bin/python"
CLI_PATH="$PROJECT_DIR/cli.py"
PLIST_PATH="$HOME/Library/LaunchAgents/com.user.aiagent.plist"

echo "🔧 Setting up launchd service for Mac mini"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "❌ Virtual environment not found. Run ./scripts/setup.sh first"
    exit 1
fi

# Create LaunchAgents directory if it doesn't exist
mkdir -p "$HOME/Library/LaunchAgents"

# Create plist file
echo "Creating launchd plist..."
cat > "$PLIST_PATH" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.aiagent</string>
    <key>ProgramArguments</key>
    <array>
        <string>$VENV_PYTHON</string>
        <string>$CLI_PATH</string>
        <string>server</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>WorkingDirectory</key>
    <string>$PROJECT_DIR</string>
    <key>StandardOutPath</key>
    <string>$PROJECT_DIR/logs/stdout.log</string>
    <key>StandardErrorPath</key>
    <string>$PROJECT_DIR/logs/stderr.log</string>
</dict>
</plist>
EOF

echo "✓ Created plist at $PLIST_PATH"

# Create logs directory
mkdir -p "$PROJECT_DIR/logs"
echo "✓ Created logs directory"

# Unload existing service if running
if launchctl list | grep -q "com.user.aiagent"; then
    echo "Unloading existing service..."
    launchctl unload "$PLIST_PATH"
fi

# Load the service
echo "Loading service..."
launchctl load "$PLIST_PATH"
echo "✓ Service loaded"

echo ""
echo "✅ launchd service setup complete!"
echo ""
echo "Useful commands:"
echo "  Start:   launchctl start com.user.aiagent"
echo "  Stop:    launchctl stop com.user.aiagent"
echo "  Status:  launchctl list | grep aiagent"
echo "  Logs:    tail -f $PROJECT_DIR/logs/stdout.log"
echo "  Errors:  tail -f $PROJECT_DIR/logs/stderr.log"
echo ""
echo "To remove service:"
echo "  launchctl unload $PLIST_PATH"
echo "  rm $PLIST_PATH"
