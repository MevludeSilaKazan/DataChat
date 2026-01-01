import uuid
from datetime import datetime
from typing import Dict, Optional, List, Any
from app.services.db_service import DatabaseManager

class SessionData:
    """
    Tek bir kullanıcının/sekmenin oturum verilerini tutar.
    
    Attributes:
        db_manager (DatabaseManager): Kullanıcının aktif veritabanı bağlantısı.
        history (List): Konuşma geçmişi (Soru-Cevap çiftleri).
        created_at (datetime): Oturumun oluşturulma zamanı.
        last_accessed (datetime): Son işlem zamanı (Timeout kontrolü için).
    """
    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        self.db_manager = db_manager
        self.history: List[Dict[str, Any]] = []  # Sohbet hafızası burada tutulur
        self.created_at = datetime.now()
        self.last_accessed = datetime.now()

class SessionManager:
    """
    Tüm aktif kullanıcı oturumlarını bellekte yöneten sınıf.
    """
    def __init__(self):
        # {session_id: SessionData} sözlüğü
        self._sessions: Dict[str, SessionData] = {}

    def create_session(self) -> str:
        """Yeni bir benzersiz oturum ID'si oluşturur ve hafızada yer ayırır."""
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = SessionData()
        return session_id

    def get_session(self, session_id: str) -> Optional[SessionData]:
        """
        Verilen ID'ye ait oturum verisini döner.
        Her çağrıldığında 'last_accessed' güncellenir.
        """
        if session_id in self._sessions:
            session = self._sessions[session_id]
            session.last_accessed = datetime.now()
            return session
        return None

    def set_db_for_session(self, session_id: str, db_manager: DatabaseManager):
        """
        Oturuma bir veritabanı yöneticisi (Excel veya SQL) atar.
        Eğer önceki bir bağlantı varsa onu güvenli bir şekilde kapatır.
        """
        if session_id in self._sessions:
            session = self._sessions[session_id]
            
            # Eğer zaten açık bir bağlantı varsa, önce onu temizle (Resource Leak önleme)
            if session.db_manager:
                try:
                    session.db_manager.dispose()
                except Exception as e:
                    print(f"Uyarı: Eski DB kapatılırken hata oluştu: {e}")
            
            session.db_manager = db_manager
            session.last_accessed = datetime.now()

    def close_session(self, session_id: str):
        """
        Oturumu tamamen sonlandırır, DB bağlantısını keser ve listeden siler.
        """
        if session_id in self._sessions:
            session = self._sessions[session_id]
            
            # SQLAlchemy bağlantısını kapat
            if session.db_manager:
                session.db_manager.dispose()
            
            # Oturumu sözlükten sil
            del self._sessions[session_id]

# Singleton Instance (Uygulama boyunca tek bir yönetici olacak)
session_store = SessionManager()