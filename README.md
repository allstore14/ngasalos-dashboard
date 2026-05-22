# 🚀 NgasalOS Dashboard

**Full-featured web dashboard for ARM STB (Set Top Box) running Armbian**

## 📌 Features

| Feature | Description |
|---------|-------------|
| 📊 Real-time Metrics | CPU, RAM, Swap, Load Average, Network, Temperature |
| 📈 Live Charts | CPU and RAM graphs with Chart.js |
| 📋 Service Manager | Start, stop, restart, view logs of systemd services |
| 💾 Disk Monitor | Track storage usage |
| 🔥 Firewall Manager | View, add, delete iptables rules |
| 🐳 Docker Manager | List, start, stop, restart, delete containers |
| 🐚 Docker CLI | Run docker commands from dashboard |
| ⚙️ System Control | Reboot and shutdown from browser |

## 🚀 Quick Install (One Line)
bash <(curl -s https://raw.githubusercontent.com/allstore14/ngasalos-dashboard/main/install.sh)


## 📋 Requirements

- Armbian / Ubuntu 22.04+
- Python 3.10+
- 512MB RAM minimum
- Docker (optional)

## 🔧 Manual Installation

```bash
git clone https://github.com/allstore14/ngasalos-dashboard.git /opt/ngasalos
cd /opt/ngasalos
apt install -y python3 python3-pip python3-flask python3-psutil iptables curl
pip install flask-cors --break-system-packages
systemctl enable ngasalos-api
systemctl start ngasalos-api

🖥️ Access Dashboard
http://YOUR_STB_IP:5000
Example: http://192.168.1.100:5000

📁 Project Structure
/opt/ngasalos/
├── api/server.py      # Backend API
├── web/dashboard.html # Frontend UI
└── install.sh         # Installer

🛠️ Commands
systemctl status ngasalos-api   # Check status
systemctl restart ngasalos-api  # Restart service
journalctl -u ngasalos-api -f   # View logs

📝 License
MIT

🙏 Credits
For ARM STB community 🇮🇩
