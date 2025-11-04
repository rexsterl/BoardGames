#!/bin/bash
# Deployment helper script for Xiangqi

set -e

echo "====================================="
echo "Xiangqi Deployment Helper"
echo "====================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (use sudo)"
    exit 1
fi

INSTALL_DIR="/var/www/xiangqi"
SERVICE_USER="www-data"

echo "This script will:"
echo "  1. Set up the application at $INSTALL_DIR"
echo "  2. Create a Python virtual environment"
echo "  3. Install dependencies"
echo "  4. Set up the systemd service"
echo "  5. Configure file permissions"
echo ""
read -p "Continue? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
fi

# Create directory
echo "Creating installation directory..."
mkdir -p "$INSTALL_DIR"

# Check if we're running from the project directory
if [ -f "deployment/deploy.sh" ]; then
    echo "Copying files..."
    rsync -av --exclude='__pycache__' --exclude='.claude' --exclude='src' \
          --exclude='.git' --exclude='*.pyc' \
          . "$INSTALL_DIR/"
else
    echo "Error: Run this script from the project root directory"
    exit 1
fi

# Set up virtual environment
echo "Setting up Python virtual environment..."
cd "$INSTALL_DIR"
python3 -m venv venv
venv/bin/pip install --upgrade pip
venv/bin/pip install -r requirements.txt

# Set permissions
echo "Setting file permissions..."
chown -R $SERVICE_USER:$SERVICE_USER "$INSTALL_DIR"
chmod 755 "$INSTALL_DIR"

# Install systemd service
echo "Installing systemd service..."
cp deployment/xiangqi.service /etc/systemd/system/

# Update ExecStart to use venv
sed -i "s|ExecStart=/usr/bin/python3|ExecStart=$INSTALL_DIR/venv/bin/python3|g" \
    /etc/systemd/system/xiangqi.service

# Reload systemd
systemctl daemon-reload

echo ""
echo "====================================="
echo "Installation complete!"
echo "====================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Start the service:"
echo "   sudo systemctl start xiangqi"
echo "   sudo systemctl enable xiangqi"
echo ""
echo "2. Check status:"
echo "   sudo systemctl status xiangqi"
echo ""
echo "3. Configure Caddy:"
echo "   - Edit /etc/caddy/Caddyfile"
echo "   - Add the configuration from deployment/Caddyfile"
echo "   - Run: sudo systemctl reload caddy"
echo ""
echo "4. Access the game:"
echo "   http://your-server-ip"
echo ""
echo "For detailed instructions, see DEPLOYMENT.md"
