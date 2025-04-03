FROM python:3.10-slim

# Cài thư viện cần thiết
RUN pip install pandas

# Thư mục làm việc
WORKDIR /app

# Copy script vào
COPY transfer_to_text.py .

# Cấu hình mặc định khi chạy container
ENTRYPOINT ["python", "transfer_to_text.py"]
