# app/services/db_service.py
import pandas as pd
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError
import io
from typing import List, Dict, Any, Optional

class DatabaseManager:
    def __init__(self, connection_string: str = "sqlite:///:memory:"):
        """
        Veritabanı bağlantısını başlatır.
        Varsayılan olarak in-memory SQLite kullanır.
        """
        self.engine = create_engine(connection_string)

    @classmethod
    def from_file(cls, file_content: bytes, filename: str):
        """
        Excel veya CSV dosyasını alır, bellekte geçici bir SQLite veritabanına çevirir
        ve DatabaseManager örneği döndürür.
        """
        # Bellek tabanlı geçici bir engine oluştur
        temp_engine = create_engine("sqlite:///:memory:")
        
        try:
            if filename.endswith(".csv"):
                # CSV okuma
                df = pd.read_csv(io.BytesIO(file_content))
            elif filename.endswith((".xls", ".xlsx")):
                # Excel okuma
                df = pd.read_excel(io.BytesIO(file_content))
            else:
                raise ValueError("Desteklenmeyen dosya formatı. Sadece .csv ve .xlsx kabul edilir.")
            
            # Tablo adını dosya adından türet (boşlukları _ yap, küçük harfe çevir)
            table_name = filename.split('.')[0].replace(" ", "_").lower()
            
            # Veriyi SQL tablosuna yaz
            df.to_sql(table_name, temp_engine, index=False)
            
            # Yeni bir instance oluştur ve engine'i set et
            instance = cls(connection_string="sqlite:///:memory:")
            instance.engine = temp_engine # Oluşturduğumuz dolu engine'i kullan
            return instance, temp_engine
            
        except Exception as e:
            raise ValueError(f"Dosya işlenirken hata oluştu: {str(e)}")

    def get_schema_info(self) -> str:
        """
        LLM'in veriyi anlaması için veritabanı şemasını özetler.
        Akıllı özellik: Az sayıda benzersiz değeri olan (kategorik) string sütunların
        içeriğini de listeler (Örn: Status sütunu için ['Active', 'Passive'] gibi).
        """
        inspector = inspect(self.engine)
        schema_text = []
        
        for table_name in inspector.get_table_names():
            columns_info = []
            columns = inspector.get_columns(table_name)
            
            for col in columns:
                col_name = col['name']
                col_type = str(col['type'])
                extra_info = ""
                
                # Zenginleştirme: Eğer string/text ise ve benzersiz değer sayısı azsa, örnekleri ekle
                if "VARCHAR" in col_type or "TEXT" in col_type or "String" in col_type:
                    try:
                        with self.engine.connect() as conn:
                            # Benzersiz değer sayısını kontrol et
                            count_query = text(f"SELECT COUNT(DISTINCT \"{col_name}\") FROM \"{table_name}\"")
                            unique_count = conn.execute(count_query).scalar()
                            
                            # Eğer 15'ten az çeşit varsa bunları listeye ekle (LLM için ipucu)
                            if unique_count and unique_count < 15:
                                values_query = text(f"SELECT DISTINCT \"{col_name}\" FROM \"{table_name}\" LIMIT 15")
                                values = [str(row[0]) for row in conn.execute(values_query).fetchall() if row[0] is not None]
                                extra_info = f" (Olası Değerler: {', '.join(values)})"
                    except:
                        pass # Şema çıkarırken hata olursa akışı bozma, sadece ekstra bilgiyi geç
                
                columns_info.append(f"- {col_name} ({col_type}){extra_info}")
            
            # Tablo bloğunu oluştur
            schema_text.append(f"TABLO: {table_name}")
            schema_text.append("SÜTUNLAR:")
            schema_text.append("\n".join(columns_info))
            schema_text.append("-" * 30)
            
        return "\n".join(schema_text)

    def execute_safe_query(self, sql: str) -> Dict[str, Any]:
        """
        SQL sorgusunu çalıştırır ve sonuçları JSON formatında döndürür.
        Not: Güvenlik kontrolleri (Validation) çağıran katmanda yapılmalıdır.
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(sql))
                
                # Veri varsa çek
                if result.returns_rows:
                    keys = result.keys()
                    data = [dict(zip(keys, row)) for row in result.fetchall()]
                    return {"data": data, "count": len(data)}
                else:
                    # Insert/Update gibi işlemse (gerçi izin vermiyoruz ama)
                    return {"message": "İşlem başarılı", "rows_affected": result.rowcount}
                    
        except SQLAlchemyError as e:
            # Veritabanı hatasını temiz bir şekilde döndür
            return {"error": str(e)}
        except Exception as e:
            return {"error": f"Beklenmeyen hata: {str(e)}"}

    def dispose(self):
        """
        Session Manager tarafından çağrılır. 
        Bağlantı havuzunu ve kaynakları temizler.
        """
        if self.engine:
            self.engine.dispose()