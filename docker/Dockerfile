FROM python:3.9-alpine

# 更新 Alpine 套件庫並安裝必要的系統套件 (如果需要)
# RUN apk update && apk add --no-cache <必要系統套件>

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt (如果有的話) 並安裝依賴
# 我們將直接安裝已知依賴，因為 setup.py 可能不完整
COPY . .

# 安裝 Python 依賴
RUN pip install --no-cache-dir couchdb pbkdf2 pymongo ipcalc requests certifi neo4j

# 複製 entrypoint 腳本並設定權限 (保持不變)
COPY docker/entrypoint.sh /tmp/entrypoint.sh
RUN chmod +x /tmp/entrypoint.sh

# 設定進入點 (保持不變)
ENTRYPOINT ["/tmp/entrypoint.sh"]

# 可以選擇性地添加 CMD 來指定預設執行的命令，例如 python nosqlmap.py
# CMD ["python", "nosqlmap.py"]
