# Quick Start - Deploy to Proxmox with Caddy

This is a simplified deployment guide. For full details, see [DEPLOYMENT.md](../DEPLOYMENT.md).

## Prerequisites

- Ubuntu/Debian server on Proxmox
- Caddy installed
- SSH access

## 1. Prepare Files

On your local machine:

```bash
cd /home/rex/Projects/BoardGames/Xiangqi

# Create deployment package (excludes unnecessary files)
tar -czf xiangqi-deploy.tar.gz \
    --exclude='__pycache__' \
    --exclude='.claude' \
    --exclude='src' \
    --exclude='.git' \
    --exclude='*.pyc' \
    .

# Copy to server
scp xiangqi-deploy.tar.gz user@your-server-ip:/tmp/
```

## 2. Deploy on Server

SSH to your server and run:

```bash
# Extract files
sudo mkdir -p /var/www
cd /var/www
sudo tar -xzf /tmp/xiangqi-deploy.tar.gz -C .
sudo mv /var/www/. /var/www/xiangqi 2>/dev/null || true

# Run deployment script
cd /var/www/xiangqi
sudo bash deployment/deploy.sh
```

The script will:
- Set up Python virtual environment
- Install dependencies
- Configure systemd service
- Set permissions

## 3. Start Service

```bash
sudo systemctl start xiangqi
sudo systemctl enable xiangqi
sudo systemctl status xiangqi
```

## 4. Configure Caddy

Edit Caddyfile:

```bash
sudo nano /etc/caddy/Caddyfile
```

Add this configuration:

**With domain:**
```caddy
xiangqi.yourdomain.com {
    reverse_proxy localhost:8000
    encode gzip
}
```

**Without domain (IP only):**
```caddy
:80 {
    reverse_proxy localhost:8000
}
```

Reload Caddy:

```bash
sudo systemctl reload caddy
```

## 5. Test

Open browser:
- With domain: `https://xiangqi.yourdomain.com`
- Without: `http://your-server-ip`

## Troubleshooting

```bash
# Check service
sudo systemctl status xiangqi
sudo journalctl -u xiangqi -f

# Check if port 8000 is listening
sudo netstat -tlnp | grep 8000

# Test API directly
curl http://localhost:8000/

# Check Caddy
sudo systemctl status caddy
```

## Update Application

```bash
# Upload new tarball, then:
cd /var/www/xiangqi
sudo systemctl stop xiangqi
# Extract new files
sudo systemctl start xiangqi
```

## Done!

Your game should now be accessible via your domain or IP address.

For advanced configuration, monitoring, and troubleshooting, see [DEPLOYMENT.md](../DEPLOYMENT.md).
