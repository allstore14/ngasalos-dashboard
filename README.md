# 🚀 NgasalOS Dashboard

**Full-featured web dashboard for ARM STB (Set Top Box) running Armbian**

[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Armbian-orange.svg)](https://armbian.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)

---

## 📌 Features

| Feature | Description |
|---------|-------------|
| 📊 **Real-time Metrics** | CPU, RAM, Swap, Load Average, Network, Temperature |
| 📈 **Live Charts** | CPU and RAM graphs with Chart.js |
| 📋 **Service Manager** | Start, stop, restart, view logs of systemd services |
| 💾 **Disk Monitor** | Track storage usage (/, /boot, /data, /var/log) |
| 🔥 **Firewall Manager** | View, add, delete iptables rules |
| 🐳 **Docker Manager** | List, start, stop, restart, delete containers |
| 🐚 **Docker CLI** | Run any docker command from dashboard |
| ⚙️ **System Control** | Reboot and shutdown from browser |
| 📱 **Responsive Design** | Works on desktop, tablet, mobile |

---

## 🚀 Quick Install (One Line)

```bash
bash <(curl -s https://raw.githubusercontent.com/allstore14/ngasalos-dashboard/main/install.sh)
```

---

## 📋 Requirements

| Requirement | Minimum |
|-------------|---------|
| OS | Armbian / Ubuntu 22.04+ |
| Python | 3.10+ |
| RAM | 512 MB |
| Storage | 100 MB free |
| Docker | Optional |

---

## 🔧 Manual Installation

```bash
# Clone repository
git clone https://github.com/allstore14/ngasalos-dashboard.git /opt/ngasalos
cd /opt/ngasalos

# Install dependencies
apt update
apt install -y python3 python3-pip python3-flask python3-psutil iptables curl
pip install flask-cors --break-system-packages

# Setup systemd service
cat > /etc/systemd/system/ngasalos-api.service << 'EOL'
[Unit]
Description=NgasalOS API Server
After=network.target

[Service]
ExecStart=/usr/bin/python3 /opt/ngasalos/api/server.py
Restart=always
WorkingDirectory=/opt/ngasalos/api

[Install]
WantedBy=multi-user.target
EOL

# Start service
systemctl daemon-reload
systemctl enable ngasalos-api
systemctl start ngasalos-api
```

---

## 🖥️ Access Dashboard

```
http://YOUR_STB_IP:5000
```

Example: `http://192.168.1.100:5000`

> 💡 Find your IP with `hostname -I`

---

## 📁 Project Structure

```
/opt/ngasalos/
├── api/
│   └── server.py          # Flask backend API
├── web/
│   └── dashboard.html     # Frontend UI (6 tabs)
└── install.sh             # One-line installer
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/metrics` | System metrics |
| GET | `/api/services` | List services |
| POST | `/api/services/{name}/start` | Start service |
| POST | `/api/services/{name}/stop` | Stop service |
| POST | `/api/services/{name}/restart` | Restart service |
| GET | `/api/services/{name}/logs` | Service logs |
| GET | `/api/disk` | Disk usage |
| GET | `/api/firewall/rules` | Firewall rules |
| POST | `/api/firewall/rules` | Add rule |
| DELETE | `/api/firewall/rules/{chain}/{num}` | Delete rule |
| GET | `/api/docker/containers` | List containers |
| POST | `/api/docker/containers/{name}/start` | Start container |
| POST | `/api/docker/containers/{name}/stop` | Stop container |
| POST | `/api/docker/containers/{name}/restart` | Restart container |
| DELETE | `/api/docker/containers/{name}/remove` | Delete container |
| GET | `/api/docker/containers/{name}/logs` | Container logs |
| POST | `/api/docker/exec` | Run docker command |
| GET | `/api/system/info` | System info |
| POST | `/api/system/reboot` | Reboot system |
| POST | `/api/system/shutdown` | Shutdown system |

---

## 🛠️ Commands

```bash
systemctl status ngasalos-api   # Check status
systemctl restart ngasalos-api  # Restart service
journalctl -u ngasalos-api -f   # View real-time logs
systemctl stop ngasalos-api     # Stop service
systemctl start ngasalos-api    # Start service
```

---

## 🐛 Troubleshooting

**Dashboard not loading?**
```bash
systemctl status ngasalos-api
netstat -tlnp | grep 5000
iptables -L INPUT -n | grep 5000
```

**Metrics not updating?**
```bash
systemctl restart ngasalos-api
curl http://localhost:5000/api/metrics
journalctl -u ngasalos-api -n 50
```

**Docker features not working?**
```bash
docker --version
systemctl status docker
```

---

## 🔄 Uninstall

```bash
systemctl stop ngasalos-api
systemctl disable ngasalos-api
rm -rf /opt/ngasalos
rm -f /etc/systemd/system/ngasalos-api.service
systemctl daemon-reload
```

---

## 📝 License

MIT

---

## 🙏 Credits

Built with [Flask](https://flask.palletsprojects.com/), [Chart.js](https://www.chartjs.org/), and [psutil](https://github.com/giampaolo/psutil)

---

<div align="center">

**Made with ❤️ for ARM STB Community 🇮🇩**

[![GitHub stars](https://img.shields.io/github/stars/allstore14/ngasalos-dashboard?style=social)](https://github.com/allstore14/ngasalos-dashboard/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/allstore14/ngasalos-dashboard?style=social)](https://github.com/allstore14/ngasalos-dashboard/network/members)

**[Report Bug](https://github.com/allstore14/ngasalos-dashboard/issues) · [Request Feature](https://github.com/allstore14/ngasalos-dashboard/issues)**

</div>
