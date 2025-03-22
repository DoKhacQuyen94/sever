# Sử dụng Python 3.11
FROM python:3.11

# Cập nhật và cài đặt Tesseract OCR
RUN apt-get update && apt-get install -y tesseract-ocr

# Tạo thư mục làm việc
WORKDIR /app

# Copy code vào container
COPY . .

# Cài đặt thư viện từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Chạy server
CMD ["gunicorn", "-b", "0.0.0.0:5000", "server:app"]
