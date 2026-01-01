# app/services/security.py
import sqlglot
from sqlglot import exp

class SQLValidator:
    @staticmethod
    def validate_and_fix(sql: str) -> str:
        """
        SQL sorgusunu analiz eder, zararlı komutları reddeder 
        ve otomatik olarak LIMIT ekler.
        """
        try:
            # 1. SQL'i Parse Et
            parsed = sqlglot.parse_one(sql)
        except Exception as e:
            raise ValueError(f"Geçersiz SQL sözdizimi: {str(e)}")

        # 2. Yasaklı Komut Kontrolü (Whitelist Yaklaşımı)
        # Sadece SELECT komutuna izin veriyoruz.
        if not isinstance(parsed, exp.Select):
            raise ValueError("Güvenlik İhlali: Sadece SELECT sorguları çalıştırılabilir.")

        # 3. Daha Derin Analiz (Alt sorgularda INSERT/DELETE/DROP var mı?)
        # HATA DÜZELTİLDİ: exp.Truncate listeden çıkarıldı.
        for node in parsed.walk():
            if isinstance(node, (exp.Insert, exp.Update, exp.Delete, exp.Drop, exp.Alter, exp.Create)):
                raise ValueError(f"Güvenlik İhlali: Yasaklı komut tespit edildi ({node.key}).")

        # 4. Otomatik LIMIT Ekleme
        if not parsed.args.get("limit"):
            parsed = parsed.limit(100) # Varsayılan limit

        return parsed.sql()