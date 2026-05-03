from flask import Flask, render_template, request, jsonify
import pandas as pd
import threading
import csv
import os
from datetime import datetime
from scapy.all import sniff, IP, TCP, UDP, ICMP
app = Flask(__name__)
CSV_FILE = 'traffic_data.csv'
monitoring_active = False
sniff_thread = None
PORT_SERVICES = {
    80: 'HTTP', 443: 'HTTPS', 53: 'DNS',
    22: 'SSH', 21: 'FTP', 25: 'SMTP',
    110: 'POP3', 3306: 'MySQL', 8080: 'HTTP-ALT', 0: 'ICMP'
}
def get_service(port):
    return PORT_SERVICES.get(port, f'Port-{port}')
def init_csv():
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Time', 'Source_IP', 'Destination_IP',
                         'Protocol', 'Packet_Size', 'Source_Port',
                         'Destination_Port', 'Service'])

def packet_handler(packet):
    if not monitoring_active:
        return
    if IP not in packet:
        return
    time = datetime.now().strftime('%H:%M:%S')
    src_ip = packet[IP].src
    dst_ip = packet[IP].dst
    size = len(packet)
    if TCP in packet:
        proto = 'TCP'
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
    elif UDP in packet:
        proto = 'UDP'
        src_port = packet[UDP].sport
        dst_port = packet[UDP].dport
    elif ICMP in packet:
        proto = 'ICMP'
        src_port = 0
        dst_port = 0
    else:
        return
    service = get_service(dst_port)
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([time, src_ip, dst_ip, proto,
                         size, src_port, dst_port, service])
def start_sniffing():
    sniff(prn=packet_handler, store=False,
          stop_filter=lambda x: not monitoring_active)

def get_data(protocol=None, src_ip=None, dst_ip=None):
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame(columns=['Time', 'Source_IP', 'Destination_IP',
                                     'Protocol', 'Packet_Size', 'Source_Port',
                                     'Destination_Port', 'Service'])
    df = pd.read_csv(CSV_FILE)
    if protocol and protocol != 'ALL':
        df = df[df['Protocol'] == protocol]
    if src_ip:
        df = df[df['Source_IP'].str.contains(src_ip, na=False)]
    if dst_ip:
        df = df[df['Destination_IP'].str.contains(dst_ip, na=False)]
    return df
def get_stats(df):
    return {
        'total_packets': len(df),
        'tcp_count': len(df[df['Protocol'] == 'TCP']),
        'udp_count': len(df[df['Protocol'] == 'UDP']),
        'icmp_count': len(df[df['Protocol'] == 'ICMP']),
        'avg_packet_size': round(df['Packet_Size'].mean(), 2) if len(df) > 0 else 0
    }
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    global monitoring_active, sniff_thread
    monitoring_active = True
    init_csv()
    sniff_thread = threading.Thread(target=start_sniffing, daemon=True)
    sniff_thread.start()
    return jsonify({'status': 'Monitoring Started'})

@app.route('/stop', methods=['POST'])
def stop():
    global monitoring_active
    monitoring_active = False
    return jsonify({'status': 'Monitoring Stopped'})

@app.route('/data', methods=['GET'])
def data():
    protocol = request.args.get('protocol', 'ALL')
    src_ip = request.args.get('src_ip', '')
    dst_ip = request.args.get('dst_ip', '')
    df = get_data(protocol, src_ip, dst_ip)
    stats = get_stats(df)
    records = df.to_dict(orient='records')
    return jsonify({
        'monitoring': monitoring_active,
        'data': records,
        'stats': stats
    })

if __name__ == '__main__':
    app.run(debug=True)