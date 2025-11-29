FROM python:3.11-slim

# 工作目錄
WORKDIR /app

# 先複製 requirements，利用 cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 再複製整個專案
COPY . .

# 確保 feature 資料夾存在
RUN mkdir -p /app/static/database/feature

# 開啟 9000 port
EXPOSE 9000

# 啟動 Flask app
CMD ["python", "server.py"]
