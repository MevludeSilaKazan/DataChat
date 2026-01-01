from autogen import ConversableAgent, UserProxyAgent
from app.core.config import settings
from app.services.db_service import DatabaseManager
from app.services.security import SQLValidator
from app.services.viz_service import VisualizationService # Yeni eklenen servis
import json

class SQLAgentService:
    def __init__(self, db_manager: DatabaseManager, history: list = None):
        self.db_manager = db_manager
        self.history = history or [] # Sohbet geçmişi
        
        self.llm_config = {
            "config_list": [{
                "model": settings.LLM_MODEL,
                "api_key": settings.GROQ_API_KEY,
                "api_type": "groq"
            }],
            "temperature": 0, # Sıfır yaratıcılık, Maksimum tutarlılık
        }

    def _create_agent(self, schema_context: str):
        """Ajanı her seferinde taze context ile oluşturur."""
        return ConversableAgent(
            name="sql_expert",
            llm_config=self.llm_config,
            system_message=f"""
            Sen uzman bir Veri Analisti ve SQL geliştiricisisin.
            
            VERİTABANI ŞEMASI:
            {schema_context}
            
            GÖREVİN:
            Kullanıcının sorusunu yanıtlayan, SQLite uyumlu, verimli bir SQL sorgusu yaz.
            
            KURALLAR:
            1. SADECE SQL kodu döndür. Markdown (```sql) kullanma. Açıklama yazma.
            2. Eğer önceki deneme hatalıysa, hata mesajını analiz et ve sorguyu düzelt.
            3. Tablo ve kolon isimleri şemadakiyle BİREBİR aynı olmalı.
            4. Asla veri silme veya değiştirme komutu yazma.
            """,
            human_input_mode="NEVER"
        )

    def process_request(self, user_question: str):
        """
        Kullanıcı sorusunu alır, SQL üretir, çalıştırır, güvenliği kontrol eder,
        hata varsa düzeltir ve en sonunda grafik önerisiyle birlikte döner.
        """
        schema = self.db_manager.get_schema_info()
        agent = self._create_agent(schema)
        
        # Kullanıcı (Sanal Yönetici)
        user_proxy = UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,
            code_execution_config=False
        )

        # --- Self-Correction Loop (Kendi Kendini Düzeltme Döngüsü) ---
        max_retries = 3
        current_error = None
        
        # Geçmiş konuşmaları prompt'a ekle (Context Awareness)
        context_msg = ""
        if self.history:
            # Son 3 mesajı alarak bağlam oluştur
            context_msg = "\nGEÇMİŞ KONUŞMALAR:\n" + "\n".join([f"Soru: {h['q']} -> SQL: {h['sql']}" for h in self.history[-3:]])

        # İlk mesajı hazırla
        message_content = f"SORU: {user_question}{context_msg}\nSadece SQL sorgusunu yaz."

        for attempt in range(max_retries):
            # print(f"DEBUG: Deneme {attempt + 1}/{max_retries}")
            
            # 1. Ajan SQL Üretsin
            chat_result = user_proxy.initiate_chat(agent, message=message_content, clear_history=False)
            
            # AutoGen bazen sözlük bazen string dönebilir, güvenli erişim:
            if isinstance(chat_result.chat_history[-1]['content'], str):
                raw_sql = chat_result.chat_history[-1]['content']
            else:
                raw_sql = str(chat_result.chat_history[-1]['content'])
            
            # Temizlik
            cleaned_sql = raw_sql.replace("```sql", "").replace("```", "").strip()
            
            # 2. Güvenlik Kontrolü ve Düzenleme (Validator)
            try:
                safe_sql = SQLValidator.validate_and_fix(cleaned_sql)
            except ValueError as ve:
                current_error = str(ve)
                # Hatayı LLM'e geri besle
                message_content = f"Yazdığın SQL şu güvenlik/sözdizimi hatasını verdi: {current_error}. Lütfen kurallara uyarak düzelt."
                continue

            # 3. Veritabanında Çalıştırma (Execution)
            result = self.db_manager.execute_safe_query(safe_sql)
            
            if "error" in result:
                current_error = result['error']
                # Hatayı LLM'e geri besle
                message_content = f"Sorgu çalışırken veritabanı şu hatayı döndürdü: {current_error}. Şemayı tekrar kontrol et ve sorguyu düzelt."
                continue
            else:
                # --- BAŞARI (SUCCESS) ---
                
                # Sonucu ve sorguyu geçmişe kaydet
                self.history.append({"q": user_question, "sql": safe_sql})
                
                # Görselleştirme Önerisi Al (YENİ EKLENEN KISIM)
                data = result.get("data", [])
                chart_suggestion = VisualizationService.suggest_chart(data)

                return {
                    "sql": safe_sql,
                    "result": result,
                    "visualization": chart_suggestion, # Frontend burayı okuyacak
                    "history_update": self.history
                }

        # Döngü bitti ama başarı yok
        return {
            "error": f"Sorgu {max_retries} denemede oluşturulamadı. Son hata: {current_error}",
            "last_sql_attempt": cleaned_sql if 'cleaned_sql' in locals() else None
        }