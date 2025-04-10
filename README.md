#BTL1 Mang May tinh
1. Run trên local: Mô phỏng với mỗi thư mục là 1 máy<br>
**lưu ý: <br>- phải run đúng thư mục để code tạo folder đúng nơi<br>
         - muốn run client phải run monitor trước vì client giao tiếp với moniter lấy dữ liệu**
  - vd muốn run peer1  
    `cd peer1/`  
    `py server.py`  
2. Run bằng docker: run peer1/peer2/peer3 bằng docker <br> 
  `cd docker`<br>
  `docker build -t <ten_image_tu_dat> .`<br>
  `docker network create <ten_network_tu_dat>`<br>
  `docker run -it -p 5001:5000 --name peer1 --network <ten_network_o_tren> <ten_image_o_tren>`<br>
  `docker run -it -p 5002:5000 --name peer2 --network <ten_network_o_tren> <ten_image_o_tren>`<br>
  `docker run -it -p 5003:5000 --name peer3 --network <ten_network_o_tren> <ten_image_o_tren>`<br>
**còn monitor vs client thì vẫn chạy trên local mục đích muốn thể hiện chạy được trên đa nên tảng**<br>

3. Các chứ năng
   - Các peer1,peer,peer3 có chức năng nhận/gửi yêu cầu upload,download,list file từ các peer khác hoặc client
     - lệnh upload: upload <tên_file> <tên_host> <tên_port>
     - lệnh download: upload <tên_file> <tên_host> <tên_port>
     - <tên_host> là localhost nếu run local; là peer1/peer2/peer3 nếu run docker
     - <tên_port> là 5001/5002/5003 tương ứng peer1/2/3 nếu run local; là 5000 nếu run docker 
   - peer monitor chỉ có chức năng cung cấp ip-port và các file của các peer hoạt động
   - client có chức năng upload,download,list file của/cho các peer đang hoạt động
