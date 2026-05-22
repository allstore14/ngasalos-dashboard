#!/usr/bin/env python3
from flask import Flask, jsonify, send_file, request
from flask_cors import CORS
import psutil
import time
import os
import subprocess
import threading
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return send_file('/opt/ngasalos/web/dashboard.html')

@app.route('/api/metrics')
def metrics():
    temp = 45
    if os.path.exists('/sys/class/thermal/thermal_zone0/temp'):
        with open('/sys/class/thermal/thermal_zone0/temp') as f:
            temp = int(f.read().strip()) / 1000
    net = psutil.net_io_counters()
    load = os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0]
    return jsonify({
        'cpu': psutil.cpu_percent(),
        'cpu_freq': round(psutil.cpu_freq().current / 1000, 1) if psutil.cpu_freq() else 0,
        'ram': {
            'used': round(psutil.virtual_memory().used / 1024 / 1024),
            'total': round(psutil.virtual_memory().total / 1024 / 1024),
            'percent': psutil.virtual_memory().percent
        },
        'swap': {
            'used': round(psutil.swap_memory().used / 1024 / 1024),
            'total': round(psutil.swap_memory().total / 1024 / 1024),
            'percent': psutil.swap_memory().percent
        },
        'uptime': time.time() - psutil.boot_time(),
        'temperature': round(temp, 1),
        'load': [round(l, 2) for l in load],
        'network': {
            'rx': round(net.bytes_recv / 1024 / 1024, 2),
            'tx': round(net.bytes_sent / 1024 / 1024, 2)
        }
    })

@app.route('/api/services')
def services():
    result = []
    try:
        output = subprocess.check_output(['systemctl', 'list-units', '--type=service', '--all', '--no-legend'])
        for line in output.decode().split('\n'):
            parts = line.split()
            if len(parts) >= 4:
                result.append({'name': parts[0].replace('.service', ''), 'status': parts[3], 'description': ' '.join(parts[4:])[:80]})
    except:
        result = [{'name': 'ngasalos-api', 'status': 'running', 'description': 'API Server'}]
    return jsonify(result[:50])

@app.route('/api/services/<name>/start', methods=['POST'])
def service_start(name):
    subprocess.run(['systemctl', 'start', name], capture_output=True)
    return jsonify({'success': True})

@app.route('/api/services/<name>/stop', methods=['POST'])
def service_stop(name):
    subprocess.run(['systemctl', 'stop', name], capture_output=True)
    return jsonify({'success': True})

@app.route('/api/services/<name>/restart', methods=['POST'])
def service_restart(name):
    subprocess.run(['systemctl', 'restart', name], capture_output=True)
    return jsonify({'success': True})

@app.route('/api/services/<name>/logs')
def service_logs(name):
    try:
        output = subprocess.check_output(['journalctl', '-u', name, '-n', '30', '--no-pager'])
        return jsonify({'logs': output.decode().split('\n')})
    except:
        return jsonify({'logs': ['No logs available']})

@app.route('/api/disk')
def disk():
    disks = []
    for path in ['/', '/boot', '/data', '/var/log']:
        if os.path.exists(path):
            usage = psutil.disk_usage(path)
            disks.append({'path': path, 'total': round(usage.total / 1024 / 1024 / 1024, 1), 'used': round(usage.used / 1024 / 1024 / 1024, 1), 'free': round(usage.free / 1024 / 1024 / 1024, 1), 'percent': usage.percent})
    return jsonify(disks)

@app.route('/api/firewall/rules')
def firewall_rules():
    rules = []
    try:
        output = subprocess.check_output(['iptables', '-L', 'INPUT', '-n', '--line-numbers'])
        for line in output.decode().split('\n'):
            if line and not line.startswith('Chain') and not line.startswith('target'):
                rules.append(line.strip())
    except:
        rules = ['No firewall rules found']
    return jsonify({'rules': rules})

@app.route('/api/firewall/rules', methods=['POST'])
def firewall_add():
    rule = request.json.get('rule')
    try:
        subprocess.run(['iptables'] + rule.split(), check=True)
        subprocess.run(['iptables-save', '-c', '/etc/iptables/rules.v4'])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/firewall/rules/<chain>/<num>', methods=['DELETE'])
def firewall_delete(chain, num):
    try:
        subprocess.run(['iptables', '-D', chain, num], check=True)
        subprocess.run(['iptables-save', '-c', '/etc/iptables/rules.v4'])
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/docker/containers')
def docker_containers():
    containers = []
    try:
        output = subprocess.check_output(['docker', 'ps', '-a', '--format', 'json'], stderr=subprocess.DEVNULL)
        for line in output.decode().split('\n'):
            if line.strip():
                c = json.loads(line)
                containers.append({'id': c.get('ID', '')[:12], 'name': c.get('Names', ''), 'image': c.get('Image', ''), 'status': c.get('Status', ''), 'state': c.get('State', '')})
    except:
        containers = []
    return jsonify(containers)

@app.route('/api/docker/containers/<name>/start', methods=['POST'])
def docker_start(name):
    subprocess.run(['docker', 'start', name], check=True, capture_output=True)
    return jsonify({'success': True})

@app.route('/api/docker/containers/<name>/stop', methods=['POST'])
def docker_stop(name):
    subprocess.run(['docker', 'stop', name], check=True, capture_output=True)
    return jsonify({'success': True})

@app.route('/api/docker/containers/<name>/restart', methods=['POST'])
def docker_restart(name):
    subprocess.run(['docker', 'restart', name], check=True, capture_output=True)
    return jsonify({'success': True})

@app.route('/api/docker/containers/<name>/remove', methods=['DELETE'])
def docker_remove(name):
    subprocess.run(['docker', 'rm', '-f', name], check=True, capture_output=True)
    return jsonify({'success': True})

@app.route('/api/docker/containers/<name>/logs')
def docker_logs(name):
    try:
        output = subprocess.check_output(['docker', 'logs', '--tail', '50', name], stderr=subprocess.STDOUT)
        return jsonify({'logs': output.decode().split('\n')})
    except Exception as e:
        return jsonify({'logs': [str(e)]})

@app.route('/api/docker/exec', methods=['POST'])
def docker_exec():
    cmd = request.json.get('cmd', '')
    try:
        output = subprocess.check_output(['docker'] + cmd.split(), stderr=subprocess.STDOUT)
        return jsonify({'output': output.decode()})
    except subprocess.CalledProcessError as e:
        return jsonify({'output': e.output.decode()})

@app.route('/api/system/info')
def system_info():
    return jsonify({'hostname': os.uname().nodename, 'kernel': os.uname().release, 'arch': os.uname().machine, 'os': 'Armbian', 'ip': subprocess.getoutput("hostname -I").strip(), 'users': subprocess.getoutput("who | wc -l").strip()})

@app.route('/api/system/reboot', methods=['POST'])
def system_reboot():
    threading.Thread(target=lambda: (time.sleep(1), os.system('reboot'))).start()
    return jsonify({'success': True})

@app.route('/api/system/shutdown', methods=['POST'])
def system_shutdown():
    threading.Thread(target=lambda: (time.sleep(1), os.system('shutdown now'))).start()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
