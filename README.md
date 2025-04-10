#BTL1 Mang May tinh
1. Run trên local: Mô phỏng với mỗi thư mục là 1 máy
**lưu ý: - phải run đúng thư mục để code tạo folder đúng nơi
         - muốn run client phải run monitor trước vì client giao tiếp với moniter lấy dữ liệu**
  - vd muốn run peer1  
    `cd peer1/`  
    `py server.py`  
2. Run bằng docker: 
  `cd docker`
  `docker build -t <ten_image_tu_dat>`
  `docker network create <ten_network_tu_dat>`
  `docker run -it -p 5001:5000 --name peer1 --network <ten_network_o_tren> <ten_image_o_tren>`
  `docker run -it -p 5002:5000 --name peer2 --network <ten_network_o_tren> <ten_image_o_tren>`
  `docker run -it -p 5003:5000 --name peer3 --network <ten_network_o_tren> <ten_image_o_tren>`
**còn monitor vs client thì vẫn chạy trên local mục đích muốn thể hiện chạy được trên đa nên tảng**
