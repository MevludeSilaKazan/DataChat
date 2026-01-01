# 📊 DataChat - Yapay Zeka Destekli Veri Analisti

**DataChat**, veritabanlarınızla (PostgreSQL, MySQL) veya Excel/CSV dosyalarınızla **doğal dilde (Türkçe/İngilizce)** konuşarak analiz yapmanızı sağlayan modern bir İş Zekası (BI) aracıdır. Karmaşık SQL sorguları yazmak yerine, sadece soru sorarsınız.

👉 **[DataChat'i Dene](https://datachat-frontend-u1ta.onrender.com)**

> ⚠️ İlk açılışta 30-60 saniye bekleyebilir (free hosting)


![Project Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-blue)
![Tech](https://img.shields.io/badge/Stack-Fullstack-orange)

## 🚀 Özellikler

* **📁 Çoklu Kaynak Desteği:** Excel (.xlsx) ve CSV dosyalarını yükleyin veya canlı veritabanlarına bağlanın.
* **🔗 Canlı Veritabanı Bağlantısı:** PostgreSQL (Supabase, Neon.tech) ve MySQL veritabanlarına güvenli bağlantı.
* **🧠 Akıllı SQL Üretimi:** LLM (Yapay Zeka) desteği ile doğal dili otomatik olarak optimize edilmiş SQL sorgularına çevirir.
* **🛡️ Güvenlik Katmanı:** `sqlglot` ve özel whitelist mimarisi ile sadece güvenli (SELECT) sorguların çalışmasına izin verir. Verilerinizi silinmeye karşı korur.
* **⚡ İlişkisel Analiz:** Tablolar arasındaki ilişkileri (JOIN) otomatik algılar ve karmaşık analizler yapar.
* **🎨 Modern Arayüz:** Next.js 14 ve Shadcn/UI ile geliştirilmiş kullanıcı dostu, responsive tasarım.
* **⬇️ Dışa Aktarım:** Analiz sonuçlarını tek tıkla Excel formatında indirme.

## 🛠️ Teknoloji Yığını (Tech Stack)

Bu proje, modern ve ölçeklenebilir teknolojiler kullanılarak geliştirilmiştir:

| Alan | Teknolojiler |
| :--- | :--- |
| **Frontend** | Next.js 14 (App Router), TypeScript, Tailwind CSS, Shadcn/UI, Axios |
| **Backend** | Python, FastAPI, Pandas, SQLAlchemy, Sqlglot |
| **Database** | PostgreSQL, MySQL (Drivers: psycopg2, pymysql) |
| **AI / LLM** | OpenAI API / Groq (SQL Generation) |
| **DevOps** | Docker, Docker Compose |

## 📸 Ekran Görüntüleri

* **Analiz için hangi dosya yüklenebilir ya da direkt olarak veritabanına bağlanılabilir**

<img width="1470" height="835" alt="Ekran Resmi 2026-01-02 00 52 50" src="https://github.com/user-attachments/assets/855f2f41-688b-4b1e-b431-691962621e26" />

* **Bu örnekte direkt olarak bir veritabanına bağlanıldı.**

<img width="1453" height="828" alt="Ekran Resmi 2026-01-02 00 45 45" src="https://github.com/user-attachments/assets/04590937-2414-44d3-97fe-299a909179e6" />

<img width="1454" height="827" alt="Ekran Resmi 2026-01-02 00 45 56" src="https://github.com/user-attachments/assets/b17ca660-28f0-4d4a-8098-5d33083705af" />


* **Kullanılan iki adet tabloyu ilişkilendiren sorular sorulabilir.**

<img width="1426" height="834" alt="Ekran Resmi 2026-01-02 00 46 38" src="https://github.com/user-attachments/assets/6fcbcfbb-6471-4038-8a30-7dfeaaec3bb9" />

<img width="1429" height="833" alt="Ekran Resmi 2026-01-02 00 46 59" src="https://github.com/user-attachments/assets/c8b4c272-3a2b-4bae-a529-3d1aa5c2ee97" />


## ⚙️ Kurulum (Local Installation)

Projeyi yerel bilgisayarınızda çalıştırmak için **Docker** kullanmanız önerilir.

### Gereksinimler
* [Git](https://git-scm.com/)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Önerilen)
* *Veya Docker yoksa:* Python 3.9+ ve Node.js 18+

### 1. Projeyi Klonlayın
Terminali açın ve projeyi indirin:

```bash
git clone [https://github.com/MevludeSilaKazan/DataChat.git](https://github.com/MevludeSilaKazan/DataChat.git)
cd DataChat
```
### 2. Çevresel Değişkenleri Ayarlayın (.env)
```bash
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. Yöntem 1: Docker ile Kurulum (Önerilen)
Tek bir komutla tüm sistemi ayağa kaldırın:
```bash
docker-compose up --build
```

Kurulum tamamlandığında:

Uygulama: http://localhost:3000

Backend için Swagger UI: http://localhost:8000/docs

### 4. Yöntem 2: Manuel Kurulum (Docker Olmadan)

* **A. Backend'i Başlatma** Ana dizinde (DataChat klasöründe) terminali açın:

```bash 
# Sanal ortam oluşturun
python -m venv venv

# Sanal ortamı aktif edin
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Paketleri yükleyin
pip install -r requirements.txt

# Sunucuyu başlatın
uvicorn app.main:app --reload --port 8000
```
* **B. Frontend'i Başlatma** Yeni bir terminal açın ve frontend klasörüne gidin:

```bash 
cd frontend

# Paketleri yükleyin
npm install

# Uygulamayı başlatın
npm run dev
```

### Lisans
Bu proje MIT lisansı altında lisanslanmıştır.

Geliştirici: [Mevlüde Sıla Kazan]
