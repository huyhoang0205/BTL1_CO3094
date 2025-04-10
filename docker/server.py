import socket
import threading
import os

HOST = '0.0.0.0' 
PORT = 5000  

MY_FILES_FOLDER = 'my_files'   # nơi chứa file nội bộ để upload

os.makedirs(MY_FILES_FOLDER, exist_ok=True)

def handle_client(conn, addr):
    try:
        command = conn.recv(1024).decode()
        if command.startswith("UPLOAD"):
            filename = command.split()[1]
            with open(os.path.join(MY_FILES_FOLDER, filename), 'wb') as f:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    f.write(data)
            print(f"[+] Nhận file '{filename}' từ {addr}, lưu vào 'my_files/'")

        elif command.startswith("DOWNLOAD"):
            filename = command.split()[1]
            filepath = os.path.join(MY_FILES_FOLDER, filename)
            if os.path.exists(filepath):
                with open(filepath, 'rb') as f:
                    conn.sendfile(f)
                print(f"[+] Gửi file '{filename}' từ 'my_files/' tới {addr}")
            else:
                conn.send(b'')
                print(f"[!] Không tìm thấy file '{filename}' trong 'my_files/'")
        
        elif command == "LIST_FILES":
            files = os.listdir(MY_FILES_FOLDER)
            response = "\n".join(files)
            conn.send(response.encode())
    except Exception as e:
        print(f"[!] Lỗi xử lý client: {e}")
    finally:
        conn.close()


def start_server():
    def server_thread():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print(f"[SERVER] Đang lắng nghe trên {HOST}:{PORT}")
            while True:
                conn, addr = s.accept()
                threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
    threading.Thread(target=server_thread, daemon=True).start()


def upload_file(peer_port, filename,peer_host):
    filepath = os.path.join(MY_FILES_FOLDER, filename)
    if not os.path.exists(filepath):
        print("[!] File không tồn tại trong thư mục 'my_files'")
        return
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((peer_host, peer_port))
        s.sendall(f"UPLOAD {filename}".encode())
        with open(filepath, 'rb') as f:
            s.sendfile(f)
    print(f"[>] Đã gửi file '{filename}' từ 'my_files/' tới peer {peer_port}")


def download_file(peer_port, filename,peer_host):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((peer_host, peer_port))
        s.sendall(f"DOWNLOAD {filename}".encode())
        filepath = os.path.join(MY_FILES_FOLDER, filename)
        with open(filepath, 'wb') as f:
            while True:
                data = s.recv(1024)
                if not data:
                    break
                f.write(data)
    print(f"[<] Đã tải file '{filename}' từ peer {peer_port} và lưu vào 'my_files/'")


def command_loop():
    while True:
        cmd = input("\n[CMD] Nhập lệnh (upload/download/list_files/exit): ").strip()
        if cmd == 'exit':
            break
        elif cmd.startswith('upload'):
            try:
                _, filename, peer_host , peer = cmd.split()
                upload_file(int(peer), filename , peer_host)
            except:
                print("❌ Cú pháp: upload <filename> <peer_host> <peer_port>")
        elif cmd.startswith('download'):
            try:
                _, filename, peer_host , peer = cmd.split()
                download_file(int(peer), filename , peer_host)
            except:
                print("❌ Cú pháp: download <filename> <peer_host> <peer_port>")
        elif cmd == 'list_files':
            files = os.listdir(MY_FILES_FOLDER)
            print("[📂] File trong 'my_files/':", files)
        else:
            print("[!] Lệnh không hợp lệ")


if __name__ == "__main__":
    print(f"[+] Peer khởi động tại port {PORT}")
    start_server()
    command_loop()
