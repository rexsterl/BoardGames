# Xiangqi Deployment Guide

This guide explains how to deploy the Xiangqi game to a Proxmox server with Caddy webserver.

## Prerequisites

- Proxmox VM or LXC container with Ubuntu/Debian
- Caddy webserver installed
- Python 3.8+ installed
- Domain name pointed to your server (optional, can use IP)
- SSH access to the server

## Deployment Steps

### 1. Prepare the Server

SSH into your Proxmox server:

```bash
ssh user@your-server-ip
```

Install required packages:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git
```

### 2. Deploy the Application

#### Option A: Clone from Git (if you have a repo)

```bash
sudo mkdir -p /var/www
cd /var/www
sudo git clone <your-repo-url> xiangqi
```

#### Option B: Upload Files Directly

From your local machine:

```bash
# Create a tarball of the project
cd /home/rex/Projects/BoardGames
tar -czf xiangqi.tar.gz Xiangqi/ --exclude='Xiangqi/__pycache__' --exclude='Xiangqi/*/__pycache__' --exclude='Xiangqi/src' --exclude='Xiangqi/.claude'

# Copy to server
scp xiangqi.tar.gz user@your-server-ip:/tmp/

# On the server
ssh user@your-server-ip
sudo mkdir -p /var/www
cd /var/www
sudo tar -xzf /tmp/xiangqi.tar.gz
sudo mv Xiangqi xiangqi
```

### 3. Set Up Python Environment

```bash
cd /var/www/xiangqi

# Create virtual environment
sudo python3 -m venv venv

# Activate and install dependencies
sudo venv/bin/pip install --upgrade pip
sudo venv/bin/pip install -r requirements.txt
```

### 4. Test the Application

Test the FastAPI server locally:

```bash
cd /var/www/xiangqi
sudo PYTHONPATH=/var/www/xiangqi venv/bin/python3 -m uvicorn server.api:app --host 127.0.0.1 --port 8000
```

Open another terminal and test:

```bash
curl http://localhost:8000/
```

You should see the API information. Press Ctrl+C to stop the server.

### 5. Set Up Systemd Service

Copy the service file:

```bash
sudo cp /var/www/xiangqi/deployment/xiangqi.service /etc/systemd/system/
```

Edit the service file to use the virtual environment:

```bash
sudo nano /etc/systemd/system/xiangqi.service
```

Update the `ExecStart` line:

```ini
ExecStart=/var/www/xiangqi/venv/bin/python3 -m uvicorn server.api:app --host 0.0.0.0 --port 8000
```

Set proper permissions:

```bash
sudo chown -R www-data:www-data /var/www/xiangqi
sudo chmod 755 /var/www/xiangqi
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable xiangqi
sudo systemctl start xiangqi
```

Check service status:

```bash
sudo systemctl status xiangqi
```

View logs:

```bash
sudo journalctl -u xiangqi -f
```

### 6. Configure Caddy

#### Option A: With Domain Name

Edit your Caddyfile (usually at `/etc/caddy/Caddyfile`):

```bash
sudo nano /etc/caddy/Caddyfile
```

Add this configuration (replace with your domain):

```caddy
xiangqi.yourdomain.com {
    reverse_proxy localhost:8000

    @websockets {
        header Connection *Upgrade*
        header Upgrade websocket
    }
    reverse_proxy @websockets localhost:8000

    log {
        output file /var/log/caddy/xiangqi.log
        format json
    }

    encode gzip
}
```

#### Option B: Without Domain (IP only)

```caddy
:80 {
    reverse_proxy localhost:8000
}
```

Or for a specific port:

```caddy
:8080 {
    reverse_proxy localhost:8000
}
```

Reload Caddy:

```bash
sudo systemctl reload caddy
```

Check Caddy status:

```bash
sudo systemctl status caddy
```

### 7. Configure Firewall

If using UFW:

```bash
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS (if using domain)
sudo ufw status
```

### 8. Test the Deployment

Open your browser and navigate to:

- With domain: `https://xiangqi.yourdomain.com`
- Without domain: `http://your-server-ip`
- Custom port: `http://your-server-ip:8080`

You should see the Xiangqi web interface!

## Updating the Application

### Method 1: Using Git

```bash
cd /var/www/xiangqi
sudo git pull
sudo systemctl restart xiangqi
```

### Method 2: Manual Upload

```bash
# On local machine
cd /home/rex/Projects/BoardGames
tar -czf xiangqi-update.tar.gz Xiangqi/ --exclude='__pycache__'
scp xiangqi-update.tar.gz user@your-server-ip:/tmp/

# On server
cd /var/www
sudo systemctl stop xiangqi
sudo tar -xzf /tmp/xiangqi-update.tar.gz
sudo mv Xiangqi xiangqi
sudo chown -R www-data:www-data /var/www/xiangqi
sudo systemctl start xiangqi
```

## Troubleshooting

### Check Service Logs

```bash
# Xiangqi service logs
sudo journalctl -u xiangqi -f

# Caddy logs
sudo journalctl -u caddy -f
sudo cat /var/log/caddy/xiangqi.log
```

### Service Won't Start

```bash
# Check for Python errors
cd /var/www/xiangqi
sudo PYTHONPATH=/var/www/xiangqi venv/bin/python3 -m uvicorn server.api:app --host 127.0.0.1 --port 8000

# Check if port 8000 is already in use
sudo netstat -tlnp | grep 8000
```

### Permission Issues

```bash
sudo chown -R www-data:www-data /var/www/xiangqi
sudo chmod -R 755 /var/www/xiangqi
```

### Caddy Not Proxying

```bash
# Test Caddy configuration
sudo caddy validate --config /etc/caddy/Caddyfile

# Reload Caddy
sudo systemctl reload caddy

# Check if FastAPI is running
curl http://localhost:8000/
```

## Security Considerations

1. **Firewall**: Only open ports 80 and 443
2. **HTTPS**: Use a domain name for automatic HTTPS with Caddy
3. **Updates**: Regularly update system packages and Python dependencies
4. **Monitoring**: Set up monitoring for the systemd service
5. **Backups**: Backup `/var/www/xiangqi` regularly

## Performance Tuning

For high traffic, consider:

1. **Multiple workers**:
   ```ini
   # In xiangqi.service
   ExecStart=/var/www/xiangqi/venv/bin/python3 -m uvicorn server.api:app --host 0.0.0.0 --port 8000 --workers 4
   ```

2. **Use Gunicorn instead of Uvicorn**:
   ```bash
   sudo venv/bin/pip install gunicorn
   ```

   Update service:
   ```ini
   ExecStart=/var/www/xiangqi/venv/bin/gunicorn server.api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
   ```

3. **Enable caching in Caddy**

## Quick Reference Commands

```bash
# Restart service
sudo systemctl restart xiangqi

# View logs
sudo journalctl -u xiangqi -f

# Reload Caddy
sudo systemctl reload caddy

# Check status
sudo systemctl status xiangqi
sudo systemctl status caddy
```

## Support

For issues or questions, check the logs first:
- Xiangqi: `sudo journalctl -u xiangqi -n 100`
- Caddy: `sudo journalctl -u caddy -n 100`
