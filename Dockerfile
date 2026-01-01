# Hafif bir Python sürümü kullan
FROM python:3.9-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Önce gereksinimleri kopyala ve kur (Cache avantajı için)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kalan kodları kopyala
COPY . .

# Konteynerın dinleyeceği port
EXPOSE 8000

# Başlatma komutu (Prod için. Dev için docker-compose ezecek)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]