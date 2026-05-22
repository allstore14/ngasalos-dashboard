#!/bin/bash
set -e

echo "🚀 Installing NgasalOS Dashboard..."

apt update
apt install -y python3 python3-pip python3-flask python3-psutil iptables curl
pip install flask-cors --break-system-packages

mkdir -p /opt/ngasalos/api /opt/ngasalos/web

curl -s https://raw.githubusercontent.com/allstore14/ngasalos-dashboard/main/api/server.py -o /opt/ngasalos/api/server.py
curl -s https://raw.githubusercontent.com/allstore14/ngasalos-dashboard/main/web/dashboard.html -o /opt/ngasalos/web/dashboard.html

cat > /etc/systemd/system/ngasalos-api.service << 'EOL'
[Unit]
Description=NgasalOS API Server
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/ngasalos/api/server.py
Restart=always
RestartSec=5
WorkingDirectory=/opt/ngasalos/api

[Install]
WantedBy=multi-user.target
EOL

systemctl daemon-reload
systemctl enable ngasalos-api
systemctl start ngasalos-api

IP=$(hostname -I | awk '{print $1}')
echo ""
echo "✅ Installation complete!"
echo "📱 Dashboard: http://$IP:5000"
echo ""
echo "Commands:"
echo "  systemctl status ngasalos-api  - Check status"
echo "  systemctl restart ngasalos-api - Restart service"
echo "  journalctl -u ngasalos-api -f  - View logs"
