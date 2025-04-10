# Sử dụng Python 3.11.4 với Alpine làm base image
FROM python:3.11.4-alpine

# Thiết lập thư mục làm việc trong container
WORKDIR /app
# Sao chép toàn bộ mã nguồn vào container
COPY . .
# Cấu hình cổng mà ứng dụng sẽ lắng nghe (tùy vào ứng dụng của bạn)
EXPOSE 5000
# Chạy ứng dụng Python (chỉnh sửa lại theo ứng dụng của bạn)
CMD ["python", "server.py"]
