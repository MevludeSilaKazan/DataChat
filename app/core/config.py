import os
from dotenv import load_dotenv

# .env dosyasını ortam değişkenlerine yükle
load_dotenv()

class Settings:
    """
    Tüm uygulama yapılandırması burada toplanır.
    Kodun içinde sihirli stringler ('llama3...') kullanmak yerine burası referans alınır.
    """
    
    # 1. API Anahtarları
    # Eğer .env dosyasında yoksa None döner, uygulama başlarken hata verebilir.
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # 2. LLM (Yapay Zeka) Ayarları
    # SQL yazma konusunda en başarılı ve Groq üzerinde en hızlı model: Llama 3 70B
    LLM_MODEL = "llama-3.3-70b-versatile"
    
    # Ajanın yaratıcılık seviyesi (SQL için 0'a yakın olmalı)
    TEMPERATURE = 0.0
    
    # 3. Uygulama Bilgileri
    PROJECT_NAME = "DataChat Enterprise"
    VERSION = "1.0.0"
    
    # 4. Güvenlik ve Limitler
    # Kullanıcının yanlışlıkla tüm veritabanını çekmesini önlemek için varsayılan limit
    DEFAULT_SQL_LIMIT = 100
    
    # Veritabanı sorgusu için zaman aşımı (saniye)
    SQL_EXECUTION_TIMEOUT = 30

# Ayarları başlat
settings = Settings()

# Basit bir güvenlik kontrolü (Docker loglarında görünmesi için)
if not settings.GROQ_API_KEY:
    print("⚠️  UYARI: GROQ_API_KEY ortam değişkeni bulunamadı! Uygulama düzgün çalışmayabilir.")