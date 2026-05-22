# 🚀 NgasalOS Dashboard
**Full-featured web dashboard for ARM STB (Set Top Box) running Armbian**

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Armbian-orange.svg)](https://armbian.com)

---

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

---

## 🚀 Quick Install
```bash
bash <(curl -s [https://raw.githubusercontent.com/allstore14/ngasalos-dashboard/main/install.sh](https://raw.githubusercontent.com/allstore14/ngasalos-dashboard/main/install.sh))

#📋 Requirements
Requirement	Minimum
OS	Armbian / Ubuntu 22.04+
Python	3.10+
RAM	512 MB
Storage	100 MB free
Docker	Optional

#🔧 Manual Installation
git clone [https://github.com/allstore14/ngasalos-dashboard.git](https://github.com/allstore14/ngasalos-dashboard.git) /opt/ngasalos
cd /opt/ngasalos
apt install -y python3 python3-pip python3-flask python3-psutil iptables curl
pip install flask-cors --break-system-packages
systemctl enable ngasalos-api
systemctl start ngasalos-api

#🖥️ Access Dashboard
http://YOUR_STB_IP:5000
Example: [http://192.168.1.100:5000](http://192.168.1.100:5000)

#📁 Project StructurePlaintext/opt/ngasalos/
├── api/server.py      # Backend API
├── web/dashboard.html # Frontend UI
└── install.sh         # Installer

#🛠️ Commands
systemctl status ngasalos-api   # Check status
systemctl restart ngasalos-api  # Restart service
journalctl -u ngasalos-api -f   # View logs

#🐛 TroubleshootingDashboard not loading?Bashsystemctl status ngasalos-api
netstat -tlnp | grep 5000
Metrics not updating?Bashsystemctl restart ngasalos-api
curl http://localhost:5000/api/metrics

#🔄 UninstallBashsystemctl stop ngasalos-api
systemctl disable ngasalos-api
rm -rf /opt/ngasalos
rm -f /etc/systemd/system/ngasalos-api.service
systemctl daemon-reload

#📝 License
MIT

#🙏 Credits
Built with Flask, Chart.js, psutil

For ARM STB Community 🇮🇩
https://github.com/allstore14/ngasalos-dashboard
