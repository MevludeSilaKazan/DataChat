# 📊 DataChat - Yapay Zeka Destekli Veri Analisti

**DataChat**, veritabanlarınızla (PostgreSQL, MySQL) veya Excel/CSV dosyalarınızla **doğal dilde (Türkçe/İngilizce)** konuşarak analiz yapmanızı sağlayan modern bir İş Zekası (BI) aracıdır. Karmaşık SQL sorguları yazmak yerine, sadece soru sorarsınız.

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

*(Buraya projenin ekran görüntüler eklenecek)*

## ⚙️ Kurulum (Local)

Projeyi bilgisayarınızda en kolay şekilde çalıştırmak için **Docker** kullanmanızı öneririm.

### Gereksinimler
* Docker & Docker Compose
* Git
