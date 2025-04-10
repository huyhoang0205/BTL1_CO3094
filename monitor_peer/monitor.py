# monitor_peer/monitor_service.py
import socket
import threading
import time

PEERS = {
    5001: "Peer1",
    5002: "Peer2",
    5003: "Peer3",
}

HOST = 'localhost'
MONITOR_PORT = 6000

active_peers = {}  # {port: timestamp}

def check_peer_loop():
    while True:
        for port in PEERS.keys():
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1.0)
                    s.connect((HOST, port))
                    s.sendall(b"LIST_FILES")
                    _ = s.recv(1024)
                    active_peers[port] = time.time()
            except:
                if port in active_peers:
                    del active_peers[port]
        time.sleep(5)

def handle_client(conn, addr):
    data = conn.recv(1024).decode()
    if data == "GET_ACTIVE_PEERS":
        response = ""
        for port in active_peers:
            response += f"{HOST}:{port}\n"
        conn.send(response.encode())
    conn.close()

def start_monitor():
    threading.Thread(target=check_peer_loop, daemon=True).start()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, MONITOR_PORT))
        s.listen()
        print(f"🛰️ Monitor Service đang chạy tại {HOST}:{MONITOR_PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_monitor()
