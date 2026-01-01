import pandas as pd
from typing import List, Dict, Any, Union

class VisualizationService:
    @staticmethod
    def suggest_chart(data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Verilen veri setini analiz eder ve Frontend için en uygun grafik türünü önerir.
        
        Döndürdüğü format:
        {
            "type":Str ("bar", "line", "pie", "table"),
            "x_key": Str (Grafik ekseni için kolon adı),
            "y_key": Str (Değerler için kolon adı),
            "title": Str (Otomatik başlık önerisi),
            "explanation": Str (Neden bu grafiğin seçildiği)
        }
        """
        
        # 1. Veri Yoksa veya Boşsa -> Tablo
        if not data or len(data) == 0:
            return {"type": "table", "explanation": "Veri yok."}

        try:
            df = pd.DataFrame(data)
        except Exception:
            return {"type": "table", "explanation": "Veri yapısı bozuk."}

        # Sütun tiplerini ayır
        num_cols = df.select_dtypes(include=['number']).columns.tolist()
        # Object (String) ve Category tiplerini al
        cat_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
        
        # Tarih tespiti (Pandas bazen tarihleri 'object' olarak görür, kontrol edelim)
        date_cols = []
        for col in cat_cols:
            try:
                # İlk 10 satıra bakarak tarih mi diye kontrol et (Hız için)
                if pd.to_datetime(df[col].dropna().head(10), errors='coerce').notna().all():
                    date_cols.append(col)
            except:
                pass
        
        # Tarih olarak tespit edilenleri kategorik listeden çıkar (Çakışmayı önle)
        cat_cols = [c for c in cat_cols if c not in date_cols]

        row_count = len(df)

        # --- HEURISTICS (KARAR MEKANİZMASI) ---

        # SENARYO 1: Çizgi Grafiği (Line Chart)
        # Kural: En az 1 tarih kolonu ve 1 sayısal kolon varsa.
        # Genellikle zaman içindeki değişimi (trend) göstermek için idealdir.
        if len(date_cols) >= 1 and len(num_cols) >= 1:
            return {
                "type": "line",
                "x_key": date_cols[0],
                "y_key": num_cols[0],
                "title": f"{date_cols[0]} bazında {num_cols[0]} Değişimi",
                "explanation": "Zaman serisi tespit edildiği için Çizgi Grafik seçildi."
            }

        # SENARYO 2: Pasta Grafiği (Pie Chart)
        # Kural: 1 Kategorik + 1 Sayısal kolon var VE kategori sayısı az (<= 7).
        # Parça-Bütün ilişkisi için idealdir. Çok fazla dilim olursa okunmaz.
        if len(cat_cols) >= 1 and len(num_cols) >= 1:
            unique_vals = df[cat_cols[0]].nunique()
            if 1 < unique_vals <= 7 and (df[num_cols[0]] > 0).all():
                return {
                    "type": "pie",
                    "label_key": cat_cols[0],
                    "value_key": num_cols[0],
                    "title": f"{cat_cols[0]} Dağılımı",
                    "explanation": "Kategori sayısı az olduğu için Pasta Grafik uygundur."
                }

        # SENARYO 3: Çubuk Grafiği (Bar Chart)
        # Kural: 1 Kategorik + 1 Sayısal kolon.
        # Karşılaştırma yapmak için standarttır.
        if len(cat_cols) >= 1 and len(num_cols) >= 1:
            return {
                "type": "bar",
                "x_key": cat_cols[0],
                "y_key": num_cols[0],
                "title": f"{cat_cols[0]} ve {num_cols[0]} Karşılaştırması",
                "explanation": "Kategorik verileri karşılaştırmak için Çubuk Grafik seçildi."
            }
            
        # SENARYO 4: Sadece Sayısal Veri (Bar Chart varsayımı)
        # Örn: Sadece "Yıl" ve "Satış" var ama Yıl sayısal görünüyor.
        if len(num_cols) >= 2:
             return {
                "type": "bar",
                "x_key": num_cols[0], # İlk sayıyı x ekseni varsayıyoruz (Genellikle ID veya Yıl olur)
                "y_key": num_cols[1],
                "title": f"{num_cols[0]} vs {num_cols[1]}",
                "explanation": "İki sayısal veri seti bulundu."
            }

        # HİÇBİR KALIB UYMAZSA -> TABLO
        return {
            "type": "table",
            "explanation": "Veri yapısı görselleştirme için belirgin bir desen içermiyor."
        }