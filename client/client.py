import socket
import os

MONITOR_HOST = 'localhost'
MONITOR_PORT = 6000
DOWNLOAD_FOLDER = 'downloaded_files'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# ID -> (host, port)


def get_active_peer_map():
    """
    Trả về dict: { "1": (ip, port), "2": (ip, port), ... }
    Dựa vào port của peer (5001 → peer1 = ID 1)
    """
    active = {}
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((MONITOR_HOST, MONITOR_PORT))
            s.sendall(b"GET_ACTIVE_PEERS")
            data = s.recv(4096).decode().strip()
            lines = data.split('\n')
            for line in lines:
                ip, port = line.split(':')
                port = int(port)
                peer_id = str(port - 5000)  # 5001 → 1
                active[peer_id] = (ip, port)
    except Exception as e:
        print("⚠️ Lỗi khi kết nối monitor:", e)
    return active


peer_map = {}


def get_active_peers():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((MONITOR_HOST, MONITOR_PORT))
        s.sendall(b"GET_ACTIVE_PEERS")
        data = s.recv(4096).decode()
        lines = data.strip().split('\n')
        return [tuple(line.split(':')) for line in lines]


def get_files_from_peer(ip, port):
    port = int(port)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2.0)
            s.connect((ip, port))
            s.sendall(b"LIST_FILES")
            files = s.recv(4096).decode().strip().split('\n')
            return files
    except:
        return []


def download_file_from_peer(peer_id, filename, peer_map):
    if peer_id not in peer_map:
        print("❌ ID peer không hợp lệ.")
        return
    ip, port = peer_map[peer_id]
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            s.sendall(f"DOWNLOAD {filename}".encode())
            response = s.recv(4096)
            if response == b"FILE_NOT_FOUND":
                print("❌ File không tồn tại trên peer.")
            else:
                with open(os.path.join(DOWNLOAD_FOLDER, filename), 'wb') as f:
                    f.write(response)
                print(f"✅ Đã tải file về: {DOWNLOAD_FOLDER}/{filename}")
    except Exception as e:
        print("❌ Lỗi khi tải file:", e)


def upload_file_to_peer(peer_id, filepath, peer_map):
    if peer_id not in peer_map:
        print("❌ ID peer không hợp lệ.")
        return
    ip, port = peer_map[peer_id]
    if not os.path.exists(filepath):
        print("❌ File không tồn tại.")
        return
    filename = os.path.basename(filepath)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((ip, port))
            s.sendall(f"UPLOAD {filename}".encode())
            ack = s.recv(1024)
            if ack != b"READY":
                print("❌ Peer không sẵn sàng nhận file.")
                return
            with open(filepath, 'rb') as f:
                data = f.read()
            s.sendall(data)
            print(f"✅ Đã upload {filename} lên peer {peer_id}")
    except Exception as e:
        print("❌ Lỗi khi upload file:", e)


def menu():
    while True:
        print("\n📋 MENU:")
        print("1. Xem các peer đang hoạt động và danh sách file")
        print("2. Tải file từ peer (theo ID)")
        print("3. Gửi file lên peer (theo ID)")
        print("0. Thoát")
        choice = input("👉 Chọn chức năng: ").strip()

        peer_map = get_active_peer_map()  # lấy lại danh sách mới mỗi vòng lặp

        if choice == '1':
            if not peer_map:
                print("⚠️ Không có peer nào đang hoạt động.")
            else:
                for peer_id, (ip, port) in peer_map.items():
                    print(f"\n🔗 Peer{peer_id} ({ip}:{port}) [Hoạt động]")
                    files = get_files_from_peer(ip, port)
                    if files:
                        for f in files:
                            print(f"   - {f}")
                    else:
                        print("   (trống)")
        elif choice == '2':
            if not peer_map:
                print("⚠️ Không có peer nào để tải file.")
                continue
            peer_id = input("Nhập ID của peer (1–3): ").strip()
            filename = input("Tên file cần tải: ").strip()
            if peer_id in peer_map:
                ip, port = peer_map[peer_id]
                download_file_from_peer(peer_id, filename, peer_map)
            else:
                print("❌ Peer không hoạt động hoặc ID sai.")
        elif choice == '3':
            if not peer_map:
                print("⚠️ Không có peer nào để upload.")
                continue
            peer_id = input("Nhập ID của peer (1–3): ").strip()
            filepath = input("Nhập đường dẫn file cần gửi: ").strip()
            if peer_id in peer_map:
                ip, port = peer_map[peer_id]
                upload_file_to_peer(peer_id, filepath, peer_map)
            else:
                print("❌ Peer không hoạt động hoặc ID sai.")
        elif choice == '0':
            break
        else:
            print("❗ Lựa chọn không hợp lệ.")


if __name__ == "__main__":
    menu()
