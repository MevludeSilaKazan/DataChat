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


<img width="1470" height="919" alt="Ekran Resmi 2026-01-02 00 45 56" src="https://github.com/user-attachments/assets/dece0666-b6c3-44a7-8494-475269902699" />

* **Kullanılan iki adet tabloyu ilişkilendiren sorular sorulabilir.**

<img width="1470" height="919" alt="Ekran Resmi 2026-01-02 00 46 38" src="https://github.com/user-attachments/assets/1f2fde59-a99a-45c3-8bc9-45d77ea384a4" />


<img width="1470" height="919" alt="Ekran Resmi 2026-01-02 00 46 59" src="https://github.com/user-attachments/assets/a3036bb6-b7e3-4171-a9e5-6640e00b3fde" />


## ⚙️ Kurulum (Local)

Projeyi bilgisayarınızda en kolay şekilde çalıştırmak için **Docker** kullanmanızı öneririm.

### Gereksinimler
* Docker & Docker Compose
* Git
